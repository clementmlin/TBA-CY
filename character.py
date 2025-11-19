class Character:
    """
    Personnage non joueur (suspect) pour l'enquête.
    """

    def __init__(self, name, description, dialog=None, alibi=None, guilty=False):
        self.name = name
        self.description = description
        self.dialog = dialog
        self.alibi = alibi
        self.guilty = guilty
        self.current_room = None

    def set_room(self, room):
        self.current_room = room

    def get_description(self):
        return f"{self.name} : {self.description}"

    def talk(self):
        if self.dialog:
            return f"{self.name} dit : « {self.dialog} »"
        return f"{self.name} ne dit rien…"

    def give_alibi(self):
        if self.alibi:
            return f"{self.name} raconte : « {self.alibi} »"
        return f"{self.name} refuse de répondre…"

    def accuse(self):
        if self.guilty:
            return f"{self.name} blêmit… « D’accord… C’est moi. »"
        return f"{self.name} s'indigne : « Moi ? Certainement pas ! »"