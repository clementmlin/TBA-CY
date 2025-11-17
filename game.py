# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        
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

        # Create exits for rooms



        BU.exits = {"N" : histoire, "E" : philosophie, "S" : société, "O" : techno, "U":None, "D":None}
        histoire.exits = {"N" :hist_cont, "E" : None, "S" : BU, "O" : politique,"U":None,"D":None}
        hist_cont.exits = {"N" :None, "E" :None, "S" : histoire, "O" : None,"U": None,"D":préhist}
        politique.exits = {"N" :None, "E" :histoire, "S" : techno, "O" : None,"U":None,"D":None}
        société.exits = {"N" :BU, "E" : None, "S" : environnement, "O" : None,"U":None,"D":None}
        environnement.exits = {"N" :société, "E" :None, "S" : None, "O" : None,"U":None, "D":None}
        philosophie.exits = {"N" :None, "E" : None, "S" : None, "O" :BU ,"U":psycho,"D":None }
        techno.exits = {"N" :politique, "E" : BU, "S" :None, "O" : math,"U":None , "D":None}
        maths.exits = {"N" :None, "E" : techno, "S" : None, "O" : None,"U": None, "D": None}

        #pour monter et descendrre d'étage

        
        préhist.exits = {"N" :, "E" : tower, "S" : castle, "O" : None, "U":hist_cont, "D":None}
        psycho.exits = {"N" :, "E" : tower, "S" : castle, "O" : None,"U":None, "D":philosophie}
        






   

        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = swamp

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def printh_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'énigme !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
