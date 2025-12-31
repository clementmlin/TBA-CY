MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

CHARACTER_MAPPING = {
    'bibliothecaire': 'bibliothécaire',
    'b': 'bibliothécaire',
    'etudiant': 'étudiant',
    'e': 'étudiant',
    'professeur': 'professeur',
    'p': 'professeur',
    'chercheuse': 'chercheuse',
    'c': 'chercheuse',
    'agent': 'agent',
    'a': 'agent',
}

class Actions:

    # ---------- DEPLACEMENT ----------
    def go(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        direction = list_of_words[1].lower()

        directions = {
            'n': 'N', 'nord': 'N',
            's': 'S', 'sud': 'S',
            'e': 'E', 'est': 'E',
            'o': 'O', 'ouest': 'O'
        }

        if direction not in directions:
            print("Direction inconnue.")
            return False

        dir_final = directions[direction]
        room = game.current_room

        if dir_final not in room.exits or room.exits[dir_final] is None:
            print("\nAucune porte dans cette direction.\n")
            return False

        next_room = room.exits[dir_final]

        # déplacement réel
        game.player.move(next_room)
        game.current_room = next_room

        Actions.look(game)
        print(game.player.get_history())
        return True

    # ---------- BACK ----------
    def back(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        if game.player.back():
            game.current_room = game.player.current_room
            Actions.look(game)
            print(game.player.get_history())
            return True

        return False

    # ---------- HISTORY ----------
    def history(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        print(game.player.get_history())
        return True

    # ---------- LOOK ----------
    def look(game, list_of_words=None, number_of_parameters=0):
        room = game.current_room

        print(f"\nVous êtes {room.description}\n")

        # objets
        if room.items:
            print("Objets présents :")
            for item in room.items:
                print(f"  - {item}")
        else:
            print("Aucun objet ici.")

        # personnages
        if room.characters:
            print("\nPersonnes présentes :")
            for char in room.characters:
                print(f"  - {char.name}")

        # sorties
        exits = [d for d, r in room.exits.items() if r is not None]
        print("\nSorties :", ", ".join(exits), "\n")

    # ---------- AUTRES COMMANDES ----------
    def help(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        print("\nCommandes disponibles :")
        for cmd in game.commands.values():
            print(" -", cmd)
        print()
        return True

    def quit(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        print(f"\nMerci {game.player.name} d'avoir joué.\n")
        game.finished = True
        return True

    def talk(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        name = list_of_words[1].lower()
        if name in CHARACTER_MAPPING:
            name = CHARACTER_MAPPING[name]

        for char in game.current_room.characters:
            if char.name.lower() == name:
                print(char.talk())
                return True

        print("Cette personne n'est pas ici.")
        return False

    def alibi(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        name = list_of_words[1].lower()
        if name in CHARACTER_MAPPING:
            name = CHARACTER_MAPPING[name]

        for char in game.current_room.characters:
            if char.name.lower() == name:
                print(char.give_alibi())
                return True

        print("Cette personne n'est pas ici.")
        return False

    def accuse(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        name = list_of_words[1].lower()
        if name in CHARACTER_MAPPING:
            name = CHARACTER_MAPPING[name]

        for char in game.current_room.characters:
            if char.name.lower() == name:
                print(char.accuse())
                if char.guilty:
                    print("\n🎉 Vous avez résolu le meurtre !")
                    game.finished = True
                return True

        print("Cette personne n'est pas ici.")
        return False

def quests(game, list_of_words, number_of_parameters):
    n=len(list_of_words)
    if n != number_of_parameters + 1:
        command_word=list_of_words[0]
        print(MSG0.format(command_word=list_of_words[0]))
        return False
    # Affichage des quêtes
    game.player.quest_manager.show_quests()
    return True
def quest(game, list_of_words, number_of_parameters):
    n=len(list_of_words)
    if n < number_of_parameters + 1:
        command_word=list_of_words[0]
        print(MSG1.format(command_word=command_word))
        return False
    
    quest_title=" ".join(list_of_words[1:])

    current_count={
        "Se déplacer": game.player.move_count
    }

    #afficher les détails des quêtes
    game.player.quest_manager.update_quests(current_count)
    return True
def activate(game, list_of_words, number_of_parameters):
    n = len(list_of_words)
    if n < number_of_parameters + 1:
        command_word = list_of_words[0]
        print(MSG1.format(command_word=command_word))
        return False

        # Get the quest title from the list of words (join all words after command)
    quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
    if game.player.quest_manager.activate_quest(quest_title):
        return True

    msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
    msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
    print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
    return False
def rewards(game, list_of_words, number_of_parameters):
    n = len(list_of_words)
    if n != number_of_parameters + 1:
        command_word = list_of_words[0]
        print(MSG0.format(command_word=command_word))
        return False

        # Show all rewards
    game.player.show_rewards()
    return True