# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
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


    

    def go(game, list_of_words, number_of_parameters):
        # ... (docstring inchangée)

        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        direction = list_of_words[1]
        if direction is None:
            print(f"Direction '{direction}' non reconnue.")
            return False

        nom_direc = {
            'n': 'N', 'nord': 'N','NORD': 'N', 'Nord': 'N',
            's': 'S', 'sud':  'S','SUD': 'S', 'Sud':  'S',
            'e': 'E', 'est':  'E','EST': 'E', 'Est':  'E',
            'o': 'O', 'ouest': 'O','OUEST': 'O', 'Ouest': 'O',
        }

        key = direction.strip().lower()
        if key not in nom_direc:
            print(f"Direction '{direction}' non reconnue.")
            return False

        final_direc = nom_direc[key]
        moved = player.move(final_direc)
        if moved:
            # Afficher l'historique après chaque déplacement
            print(player.get_history())
        return moved


    def back(game, list_of_words, number_of_parameters):
        """
        Revenir à la salle précédente (pop de l'historique).
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        success = player.back()
        if success:
            # Afficher l'historique après retour en arrière
            print(player.get_history())
        return success


    def history(game, list_of_words, number_of_parameters):
        """
        Afficher l'historique des salles visitées.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        print(player.get_history())
        return True



    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True


    def talk(game, list_of_words, number_of_parameters):
        """
        Parler à un personnage présent dans la salle.
        """

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        name = list_of_words[1].lower()

        if name in CHARACTER_MAPPING:
            name = CHARACTER_MAPPING[name]
        else:
            print(f"Personnage '{list_of_words[1]}' non reconnu.")
            return False

        for character in game.player.current_room.characters:
            if character.name.lower() == name:
                print(character.talk())
                return True

        print("Cette personne n'est pas ici.")
        return False


    def alibi(game, list_of_words, number_of_parameters):
        """
        Demander l'alibi d'un suspect.
        """

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        name = list_of_words[1].lower()

        if name in CHARACTER_MAPPING:
            name = CHARACTER_MAPPING[name]
        else:
            print(f"Personnage '{list_of_words[1]}' non reconnu.")
            return False

        for character in game.player.current_room.characters:
            if character.name.lower() == name:
                print(character.give_alibi())
                return True

        print("Cette personne n'est pas ici.")
        return False


    def accuse(game, list_of_words, number_of_parameters):
        """
        Accuser un suspect d'être le meurtrier.
        """

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        name = list_of_words[1].lower()

        if name in CHARACTER_MAPPING:
            name = CHARACTER_MAPPING[name]
        else:
            print(f"Personnage '{list_of_words[1]}' non reconnu.")
            return False

        for character in game.player.current_room.characters:
            if character.name.lower() == name:
                print(character.accuse())

                if character.guilty:
                    print("\n🎉 Vous avez résolu le meurtre !")
                    game.finished = True

                return True

        print("Cette personne n'est pas ici.")
        return False
    
    def __init__(self,room):
        self.room= room
        
    def look(game, list_of_words, number_of_parameters):
        if number_of_parameters != 0:
            return "La commende 'look' ne prend aucun parameters" 
        room =game.current_room

        if not room.items:
            return "il n'y aaucun objet dans cette pièce"
        result = "Vous voyez les objets suivants :\n"
        for item in room.items:
            result += f" - {item}\n"
    
        return result.rstrip()
    

    def inspect(self, game, list_of_words, number_of_parameters):
        # Vérifier qu'on a bien le bon nombre de paramètres
        if number_of_parameters != 1:
            return "Utilise : inspect <objet>"

        room = game.current_room
        cible = list_of_words[0].lower()

        # Chercher l’objet dans la salle
        for item in room.items:
            if item.name.lower() == cible:
                if item.name.lower() == "ordinateur":
                    # Si on inspecte l’ordinateur, et que la clé USB est présente
                    for maybe_usb in room.items:
                        if maybe_usb.name.lower() == "clé usb":
                            return "Tu lis les fichiers de la clé USB… Le contenu est révélateur !"
                    return "Il n’y a pas de clé USB à lire ici."
                return str(item)  # Affiche description
        return "Cet objet n'est pas ici."