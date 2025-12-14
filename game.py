from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from item import Item


class Game:

    def __init__(self,current_room):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.current_room = None
    def play(self):
        print(self.current_room.name)
    

    def setup(self):

        # --- COMMANDES ---
        self.commands["help"] = Command("help", ": afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", ": quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", "<direction> : se déplacer (N,E,S,O)", Actions.go, 1)

        self.commands["history"] = Command("history", ": afficher l'historique des salles visitées", Actions.history, 0)
        self.commands["back"] = Command("back", ": revenir à la salle précédente", Actions.back, 0)

        self.commands["talk"] = Command("talk", "<nom> : parler à une personne", Actions.talk, 1)
        self.commands["alibi"] = Command("alibi", "<nom> : demander l’alibi", Actions.alibi, 1)
        self.commands["accuse"] = Command("accuse", "<nom> : accuser le suspect", Actions.accuse, 1)


        # --- SALLES ---
        BU = Room("Bibliothèque", "dans le hall principal de la BU.")
        histoire = Room("Salle Histoire", "dans la salle d’histoire.")
        hist_cont = Room("Histoire contemporaine", "dans la salle d'histoire contemporaine.")
        politique = Room("Politique", "dans la salle politique.")
        préhist = Room("Préhistoire", "dans la salle de préhistoire.")

        société = Room("Société", "dans la salle société.")
        environnement = Room("Environnement", "dans la salle environnement.")

        phylosophie = Room("Philosophie", "dans la salle philosophie.")
        psycho = Room("Psychologie", "dans la salle psychologie.")

        techno = Room("Technologie", "dans la salle technologie.")
        math = Room("Mathématiques", "dans la salle mathématiques.")


        # --- SORTIES ---
        BU.exits = {"N": histoire, "E": phylosophie, "S": société, "O": techno}

        histoire.exits = {"N": hist_cont, "E": None, "S": BU, "O": politique}
        hist_cont.exits = {"N": None, "E": None, "S": histoire, "O": None}
        politique.exits = {"N": None, "E": None, "S": techno, "O": None}
        techno.exits = {"N": None, "E": BU, "S": None, "O": math}
        société.exits = {"N": BU, "E": None, "S": environnement, "O": None}
        environnement.exits = {"N": société, "E": None, "S": None, "O": None}

        phylosophie.exits = {"N": None, "E": None, "S": None, "O": BU}
        psycho.exits = {"N": None, "E": None, "S": None, "O": None}
        préhist.exits = {"N": None, "E": None, "S": None, "O": None}

        
        math.exits = {"N": None, "E": techno, "S": None, "O": None}

        # Enregistrer les salles
        self.rooms = [
            BU, histoire, hist_cont, politique, préhist,
            société, environnement,
            phylosophie, psycho,
            techno, math
        ]

        # --- PNJ / SUSPECTS ---
        suspect1 = Character(
            "bibliothécaire",
            "Une femme calme, concentrée sur son travail.",
            dialog="Avez-vous besoin d'aide ?",
            alibi="Je rangeais les livres d'histoire dans la salle au nord.",
            guilty=False
        )

        suspect2 = Character(
            "étudiant",
            "Un étudiant stressé, regard fuyant.",
            dialog="Hein ? Non, je… je faisais rien !",
            alibi="Je révisais en philosophie.",
            guilty=True  # le meurtrier !
        )

        suspect3 = Character(
            "professeur",
            "Un professeur passionné de politique.",
            dialog="On ne respecte plus rien de nos jours…",
            alibi="Je débattais en salle de politique.",
            guilty=False
        )

        suspect4 = Character(
            "chercheuse",
            "Une scientifique en quête d’un ouvrage rare.",
            dialog="Je cherchais un manuel en technologie.",
            alibi="J’étais dans la salle techno.",
            guilty=False
        )

        suspect5 = Character(
            "agent",
            "Le gardien de la bibliothèque.",
            dialog="Tout me semblait calme…",
            alibi="Je surveillais la zone sud.",
            guilty=False
        )

                    #  Objets à placer
        arme_crime = Item(
            "Arme du crime",
            "Une lourde sculpture en métal, ensanglantée. Indice majeur."
        )

        livre_enigme = Item(
            "Livre ancien",
            "Un livre poussiéreux dont certaines pages semblent annotées à la main."
        )

        cle_usb = Item(
            "Clé USB",
            "Une clé USB contenant des fichiers suspects."
        )

        ordinateur = Item(
            "Ordinateur",
            "Un ordinateur allumé sur lequel tu peux tenter de lire la clé USB."
        )
                # 📍 Ajouter les objets dans les salles correspondantes
        psycho.add_item(arme_crime)
        histoire.add_item(livre_enigme)
        techno.add_item(cle_usb)
        techno.add_item(ordinateur)


        # Placement des PNJ
        BU.add_character(suspect1)           # bibliothécaire
        phylosophie.add_character(suspect2)  # étudiant (meurtrier)
        politique.add_character(suspect3)    # professeur
        techno.add_character(suspect4)       # chercheuse
        société.add_character(suspect5)      # agent


        # --- JOUEUR ---
        self.player = Player(input("\nEntrez votre nom : "))
        self.player.current_room = BU
        return BU

    def print_welcome(self):
        print ("Cette nuit-là, au cœur d’un hiver glacial de 1999, la bibliothèque Hogward s’apprêtait enfin à fermer ses portes après une journée interminable.\n Pourtant, alors que le silence retombait lentement sur les lieux, un événement tragique vint déchirer la quiétude de la BU.\n Dans l’une des salles les plus froides, le corps sans vie d’un homme d’une soixantaine d’années fut découvert.\n")
        print(f"\nBienvenue {self.player.name} dans cette enquête mystérieuse !")
        print("Entrez 'help' pour voir les commandes.")
        print(self.player.current_room.get_long_description())


    def play(self):
        self.setup()
        self.print_welcome()
        
        while not self.finished:
            self.process_command(input("> "))

    def process_command(self, command_string):
    # enlever les espaces en début/fin
        command_string = command_string.strip()

    # si l'utilisateur appuie juste sur Entrée (ou tape uniquement des espaces), ne rien faire
        if not command_string:
            return None

    # split sans argument supprime les espaces multiples et évite des mots vides
        # enlever les espaces en début/fin
        command_string = command_string.strip()

        # si l'utilisateur appuie juste sur Entrée (ou tape uniquement des espaces), ne rien faire
        if not command_string:
            return None

        # split sans argument supprime les espaces multiples et évite des mots vides
        words = command_string.split()
        cmd = words[0]

        if cmd not in self.commands:
            print("\nCommande inconnue. Tape 'help'.\n")
        else:
            command = self.commands[cmd]
            command.action(self, words, command.number_of_parameters)




def main():
    game = Game()
    game.current_room = setup()
    game.play()

if __name__ == "__main__":
    main()