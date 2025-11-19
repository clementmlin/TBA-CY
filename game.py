from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character

class Game:

    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    

    def setup(self):

        # --- COMMANDES ---
        self.commands["help"] = Command("help", ": afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", ": quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", "<direction> : se déplacer (N,E,S,O)", Actions.go, 1)

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
        politique.exits = {"N": None, "E": histoire, "S": techno, "O": None}
        
        # Setup rooms
        #les salles au nord
        BU = Room("Bibliothèque", "Le Hall de la BU, la salle principale.")
        self.rooms.append(BU)
        histoire = Room("salle histoire", ".")
        self.rooms.append(histoire)
        hist_cont = Room("salle histoire contemporaine", ".")
        self.rooms.append(hist_cont)
        politique = Room("politique", ".")
        self.rooms.append(politique)
        préhist = Room("préhist", ".")
        self.rooms.append(préhist)
        # les salles au sud
        société= Room("salle société", ".")
        self.rooms.append(société)
        environnement = Room("salle environnement", ".")
        self.rooms.append(environnement)
        # les salles à l'est
        philosophie = Room("salle philosophie", ".")
        self.rooms.append(philosophie)
        psycho = Room("salle psychologie", ".")
        self.rooms.append(psycho)
        # les salles à l'ouest
        techno = Room("salle technologie", ".")
        self.rooms.append(techno)
        math = Room("salle mathématiques", ".")
        self.rooms.append(math)

        phylosophie.exits = {"N": None, "E": None, "S": None, "O": BU}
        psycho.exits = {"N": None, "E": None, "S": None, "O": None} 
        préhist.exits = {"N": None, "E": None, "S": None, "O": None}  
        techno.exits = {"N": politique, "E": BU, "S": None, "O": math}
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
            "Bibliothécaire",
            "Une femme calme, concentrée sur son travail.",
            dialog="Avez-vous besoin d'aide ?",
            alibi="Je rangeais les livres d'histoire dans la salle au nord.",
            guilty=False
        )

<<<<<<< HEAD
        suspect2 = Character(
            "Étudiant",
            "Un étudiant stressé, regard fuyant.",
            dialog="Hein ? Non, je… je faisais rien !",
            alibi="Je révisais en philosophie.",
            guilty=True  # le meurtrier !
        )
=======
        BU.exits = {"N" : histoire, "E" : philosophie, "S" : société, "O" : techno, "U":None, "D":None}
        histoire.exits = {"N" :hist_cont, "E" : None, "S" : BU, "O" : politique,"U":None,"D":None}
        hist_cont.exits = {"N" :None, "E" :None, "S" : histoire, "O" : None,"U": None,"D":préhist}
        politique.exits = {"N" :None, "E" :histoire, "S" : techno, "O" : None,"U":None,"D":None}
        société.exits = {"N" :BU, "E" : None, "S" : environnement, "O" : None,"U":None,"D":None}
        environnement.exits = {"N" :société, "E" :None, "S" : None, "O" : None,"U":None, "D":None}
        philosophie.exits = {"N" :None, "E" : None, "S" : None, "O" :BU ,"U":psycho,"D":None }
        techno.exits = {"N" :politique, "E" : BU, "S" :None, "O" : math,"U":None , "D":None}
        maths.exits = {"N" :None, "E" : techno, "S" : None, "O" : None,"U": None, "D": None}
>>>>>>> 0b09d69d414021633e710f7ce369544e0c58337e

        suspect3 = Character(
            "Professeur",
            "Un professeur passionné de politique.",
            dialog="On ne respecte plus rien de nos jours…",
            alibi="Je débattais en salle de politique.",
            guilty=False
        )

<<<<<<< HEAD
        suspect4 = Character(
            "Chercheuse",
            "Une scientifique en quête d’un ouvrage rare.",
            dialog="Je cherchais un manuel en technologie.",
            alibi="J’étais dans la salle techno.",
            guilty=False
        )

        suspect5 = Character(
            "Agent",
            "Le gardien de la bibliothèque.",
            dialog="Tout me semblait calme…",
            alibi="Je surveillais la zone sud.",
            guilty=False
        )

        # Placement des PNJ
        BU.add_character(suspect1)           # bibliothécaire
        phylosophie.add_character(suspect2)  # étudiant (meurtrier)
        politique.add_character(suspect3)    # professeur
        techno.add_character(suspect4)       # chercheuse
        société.add_character(suspect5)      # agent
=======
        
        préhist.exits = {"N" :, "E" : tower, "S" : castle, "O" : None, "U":hist_cont, "D":None}
        psycho.exits = {"N" :, "E" : tower, "S" : castle, "O" : None,"U":None, "D":philosophie}
        
>>>>>>> 0b09d69d414021633e710f7ce369544e0c58337e


        # --- JOUEUR ---
        self.player = Player(input("\nEntrez votre nom : "))
        self.player.current_room = BU


    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans cette enquête mystérieuse !")
        print("Entrez 'help' pour voir les commandes.")
        print(self.player.current_room.get_long_description())


    def play(self):
        self.setup()
        self.print_welcome()
        
        while not self.finished:
            self.process_command(input("> "))


    def process_command(self, command_string):
        words = command_string.split(" ")
        cmd = words[0]

        if cmd not in self.commands:
            print("\nCommande inconnue. Tape 'help'.\n")
        else:
            command = self.commands[cmd]
            command.action(self, words, command.number_of_parameters)


<<<<<<< HEAD
=======
    # Print the welcome message
    def printh_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'énigme !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    
>>>>>>> 0b09d69d414021633e710f7ce369544e0c58337e

def main():
    Game().play()

if __name__ == "__main__":
    main()