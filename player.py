# Define the Player class.
class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        # Historique : liste de Room déjà visitées (dans l'ordre)
        self.history = []
        self.inventory={}

    
    def get_inventory(self):
        if not self.inventory:
            return "Votre inventaire est vide."

        inventory_str = "Vous disposez des items suivants :\n"
        for item in self.inventory:
            inventory_str += f"    - {item}\n"
        return inventory_str.rstrip()

    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits.get(direction)

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        # Avant de changer de salle, ajouter l'ancienne salle à l'historique
        # (on n'ajoute pas la nouvelle salle — history contient les salles "déjà visitées").
        self.history.append(self.current_room)

        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    def back(self):
        """
        Revenir en arrière : retourne à la dernière salle visitée si possible.
        """
        if not self.history:
            print("\nImpossible de revenir en arrière : aucun déplacement précédent.\n")
            return False

        # Récupère la dernière salle visitée
        previous_room = self.history.pop()
        self.current_room = previous_room
        print(self.current_room.get_long_description())
        return True

    def get_history(self):
        """
        Retourne une chaîne représentant l'historique des salles visitées.
        """
        if not self.history:
            return "Vous n'avez encore visité aucune autre pièce."

        text = "Vous avez déja visité les pièces suivantes:\n"
        for room in self.history:
            # Utiliser room.description pour coller à l'exemple
            text += f"    - {room.description}\n"
        return text