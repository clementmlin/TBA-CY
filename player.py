from quest import QuestManager

class Player:
    def __init__(self, name):
        self.name = name
        self.current_room = None

        # Historique des salles VISITÉES (pile)
        self.history = []

        # Compteur de déplacements
        self.move_count = 0

        # Gestionnaire de quêtes
        self.quest_manager = QuestManager(self)

        # Récompenses
        self.rewards = []

        # Inventaire
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

        # Objectifs liés aux salles
        self.quest_manager.check_room_objectives(self.current_room.name)

        # Objectifs liés aux déplacements
        self.move_count += 1
        self.quest_manager.check_counter_objectives(
            "Marcher",               # ✅ NOM du compteur
            current_count=self.move_count
        )

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

    def add_reward(self, reward):
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez reçu une récompense : {reward}\n")

    def show_rewards(self):
        if not self.rewards:
            print("\nVous n'avez reçu aucune récompense pour le moment.\n")
        else:
            print("\n🏆 Récompenses obtenues :")
            for reward in self.rewards:
                print(f" - {reward}")
            print()

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
        return sum(item.weight for item in self.inventory)