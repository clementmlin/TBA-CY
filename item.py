class Item:
    def __init__(self,name,description,weight=0):
        self.description=description
        self.name = name
        self.weight=weight
        

    def __str__(self):
        return f"{self.name} ({self.weight} kg) : {self.description}"

    """def get_inventory(self):
        if not self.inventory:
            return "Votre inventaire est vide."

        inventory_str = "Vous disposez des items suivants :\n"
        for item in self.inventory:
            inventory_str += f"    - {item}\n"
        return inventory_str.rstrip()"""
