from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from item import Item
from quest import Quest



class Game:

    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.current_room = None
        self.quests = []

    def setup(self):


        # ---------- COMMANDES ----------
        self.commands["help"] = Command("help", ": afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", ": quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", "<direction> : se déplacer (N,E,S,O)", Actions.go, 1)
        self.commands["look"] = Command("look", ": observer la salle", Actions.look, 0)
        self.commands["history"] = Command("history", ": afficher l’historique", Actions.history, 0)
        self.commands["back"] = Command("back", ": revenir à la salle précédente", Actions.back, 0)

        self.commands["talk"] = Command("talk", "<nom> : parler à une personne", Actions.talk, 1)
        self.commands["alibi"] = Command("alibi", "<nom> : demander l’alibi", Actions.alibi, 1)
        self.commands["accuse"] = Command("accuse", "<nom> : accuser le suspect", Actions.accuse, 1)
        #self.commands["inventory"] = Command("inventory", ": afficher l’inventaire", Actions.inventory, 0)
        # ---------- QUÊTES ----------
        self.commands["quests"]= Command("quests", ": afficher les quêtes en cours", Actions.quests, 0)
        self.commands["quest"]= Command("quest", "<numéro> : afficher les détails d’une quête", Actions.quest, 1)
        self.commands["activate"]= Command("activate", ": afficher les objectifs activés", Actions.activate, 1)
        self.commands["rewards"]= Command("rewards", ": afficher les récompenses obtenues", Actions.rewards, 0)
        # ---------- OBJETS ----------
        #self.commands["inventory"] = Command("inventory", ": afficher l’inventaire", Actions.inventory, 0)
        #self.commands["use"] = Command("use", "<nom> : utiliser un objet", Actions.use, 1)
        #self.commands["take"] = Command("take", "<nom> : prendre un objet", Actions.take, 1)
        # ---------- SALLES ----------
        BU = Room("Bibliothèque", "dans le hall principal de la BU.")
        histoire = Room("Salle Histoire", "dans la salle d’histoire.")
        hist_cont = Room("Histoire contemporaine", "dans la salle d'histoire contemporaine.")
        politique = Room("Politique", "dans la salle politique.")
        préhist = Room("Préhistoire", "dans la salle de préhistoire.")
        société = Room("Société", "dans la salle société.")
        environnement = Room("Environnement", "dans la salle environnement.")
        philosophie = Room("Philosophie", "dans la salle philosophie.")
        psycho = Room("Psychologie", "dans la salle psychologie.")
        techno = Room("Technologie", "dans la salle technologie.")
        math = Room("Mathématiques", "dans la salle mathématiques.")

        # ---------- SORTIES ----------
        BU.exits = {"N": histoire, "E": philosophie, "S": société, "O": techno}

        histoire.exits = {"N": hist_cont, "S": BU, "O": politique}
        hist_cont.exits = {"S": histoire}
        politique.exits = {"S": techno}
        techno.exits = {"E": BU, "O": math}
        société.exits = {"N": BU, "S": environnement}
        environnement.exits = {"N": société}

        philosophie.exits = {"O": BU}
        psycho.exits = {}
        préhist.exits = {}
        math.exits = {"E": techno}

        self.rooms = [
            BU, histoire, hist_cont, politique, préhist,
            société, environnement, philosophie, psycho, techno, math
        ]

        # ---------- OBJETS ----------
        arme_crime = Item(
            "Arme du crime",
            "Une lourde sculpture en métal, ensanglantée. Indice majeur.",
            5
        )

        livre_enigme = Item(
            "Livre ancien",
            "Un livre poussiéreux dont certaines pages semblent annotées à la main.",
            2
        )

        cle_usb = Item(
            "Clé USB",
            "Une clé USB contenant des fichiers suspects.",
            0.05
        )

        ordinateur = Item(
            "Ordinateur",
            "Un ordinateur allumé sur lequel tu peux tenter de lire la clé USB.",
            3
        )

        psycho.add_item(arme_crime)
        histoire.add_item(livre_enigme)
        techno.add_item(cle_usb)
        techno.add_item(ordinateur)

        # ---------- PNJ ----------
        suspect1 = Character(
            "bibliothécaire",
            "Une femme calme, concentrée sur son travail.",
            dialog="Avez-vous besoin d'aide ?",
            alibi="Je rangeais les livres d'histoire.",
            guilty=False
        )

        suspect2 = Character(
            "étudiant",
            "Un étudiant stressé, regard fuyant.",
            dialog="Hein ? Non, je… je faisais rien !",
            alibi="Je révisais en philosophie.",
            guilty=True
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

        BU.add_character(suspect1)
        philosophie.add_character(suspect2)
        politique.add_character(suspect3)
        techno.add_character(suspect4)
        société.add_character(suspect5)

        # ---------- JOUEUR ----------
        self.player = Player(input("\nEntrez votre nom : "))
        self.player.current_room = BU
        self.current_room = BU
        self._setup_quests()
    
    
    def _setup_quests(self):

        salles_visited_quest = Quest(
            title="Explorer les salles liées à l'humain",
            description="Visitez toutes les salles liées à l'étude de l'humain.",
            objectives=[
                "Visiter Salle Histoire",
                "Visiter Histoire contemporaine",
                "Visiter Politique",
                "Visiter Société",
                "Visiter Philosophie",
                "Visiter Psychologie"
            ],
            reward="Badge d'explorateur humain"
        )

        questionner_suspects_quest = Quest(
            title="Questionner les suspects",
            description="Parlez à tous les suspects présents dans la bibliothèque.",
            objectives=[
                "parler avec bibliothécaire",
                "parler avec étudiant",
                "parler avec professeur",
                "parler avec chercheuse",
                "parler avec agent"
            ],
            reward="Badge d'enquêteur"
        )

        # Ajouter au jeu
        self.quests.append(salles_visited_quest)
        self.quests.append(questionner_suspects_quest)

        # Ajouter au QuestManager
        self.player.quest_manager.add_quest(salles_visited_quest)
        self.player.quest_manager.add_quest(questionner_suspects_quest)

        # Activer au moins une quête
        self.player.quest_manager.activate_quest("Explorer les salles liées à l'humain")


        
    def print_welcome(self):
        print(
            "Cette nuit-là, au cœur d’un hiver glacial de 1999, "
            "la bibliothèque Hogward s’apprêtait à fermer ses portes.\n"
            "Mais un meurtre vint briser le silence…\n"
        )
        print(f"Bienvenue {self.player.name} dans cette enquête !")
        print("Tape 'help' pour voir les commandes.\n")
        Actions.look(self)

    def play(self):
        self.setup()
        self.print_welcome()

        while not self.finished:
            self.process_command(input("> "))

    def process_command(self, command_string):
        command_string = command_string.strip()
        if not command_string:
            return

        words = command_string.split()
        cmd = words[0]

        if cmd not in self.commands:
            print("Commande inconnue.")
            return

        command = self.commands[cmd]
        command.action(self, words, command.number_of_parameters)


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
