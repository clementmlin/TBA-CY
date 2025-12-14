# Define the Room class.
from item import Item
class Room:

    def add_character(self, character):
        self.characters.append(character)

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.characters = []
        self.inventory={}
        self.items = []

    def add_item(self, item):
        self.items.append(item)
    
    
    def get_inventory(self):
        if not self.inventory:
            return "votre inventaire est vide"
        
        inventory_str = "Vous disposez des items suivants :\n"
        for item in self.inventory:
            inventory_str += f"    - {item}\n"
        return inventory_str.rstrip()
    
    
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"


    def get_long_description(self):
        text = f"\nVous êtes {self.description}\n"

    # --- Affichage des PNJ ---
        if self.characters:
            text += "\nPersonnes présentes :\n"
            for c in self.characters:
                text += f" - {c.name} : {c.description}\n"

    # --- Affichage des sorties ---
        text += "\n" + self.get_exit_string() + "\n"

        return text