class Player:
    def __init__(self, name):
        self.name = name
        self.current_room = None

        # Historique des salles VISITÉES (pile)
        # On n’y met PAS la salle de départ
        self.history = []

        self.inventory = []

    def move(self, next_room):
        """
        Déplacement normal :
        - on empile la salle actuelle
        - on change de salle
        """
        if self.current_room is not None:
            self.history.append(self.current_room)

        self.current_room = next_room
        return True

    def back(self):
        """
        Revenir à la salle précédente
        """
        if not self.history:
            print("\nImpossible de revenir en arrière.\n")
            return False

        self.current_room = self.history.pop()
        return True

    def get_history(self):
        """
        Affichage de l'historique
        """
        if not self.history:
            return "Vous n'avez encore visité aucune autre pièce."

        text = "Vous avez déjà visité les pièces suivantes :\n"
        for room in self.history:
            text += f"    - {room.description}\n"
        return text
    def total_weight(self):
        return sum(item.weight for item in self.inventory.values())