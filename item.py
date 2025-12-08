class Items:
    def _init_(self,name,description,weight):
        self.description=description
        self.name = name
        self.weight=weight
        

    def _str_(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"
""" 
    def get_inventory():
          if not self.inventory:
            return "Votre inventaire est vide."

        inventory_str = "Vous disposez des items suivants :\n"
        for item in self.inventory:
            inventory_str += f"    - {item}\n"
        return inventory_str.rstrip()
"""