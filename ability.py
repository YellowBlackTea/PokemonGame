import re

from data import save_data

class Attack:
    def __init__(self, attack_dict) -> None:
        self.name = attack_dict.get('Name')
        self.description = attack_dict.get('Description')
        self.type = attack_dict.get('Element')
        self.power = int(attack_dict.get('Power'))
        self.accuracy = int(attack_dict.get('Accuracy'))
        self.cost = int(attack_dict.get('Cost'))
    
    # Read access only
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Invalid Name")
        self._name = name
    
    # Read access only
    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, description):
        self._description = description
    
    # Read access only
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, type):
        self._type = type
    
    # Read access only
    @property
    def power(self):
        return self._power
    @power.setter
    def power(self, power):
        self._power = power
        
    # Read access only
    @property
    def accuracy(self):
        return self._accuracy
    @accuracy.setter
    def accuracy(self, accuracy):
        self._accuracy = accuracy
        
    # Read access only
    @property
    def cost(self):
        return self._cost
    @cost.setter
    def cost(self, cost):
        self._cost = cost
        
    def __str__(self) -> str:
        return f"{self.name}(Attack, {self.type}, Cost: {self.cost}): {self.description}"
    

class Defense:    
    def __init__(self, defense_dict) -> None:
        self.name = defense_dict.get('Name')
        self.description = defense_dict.get('Description')
        self.type = defense_dict.get('Type')
        self.healing_range = defense_dict.get('Healing')
        self.accuracy = int(defense_dict.get('Accuracy'))
        self.cost = int(defense_dict.get('Cost'))
        self.healing_min, self.healing_max = map(int, re.match(r"([0-9]+)?\s+-\s+([0-9]+)?", self.healing_range.groups()))
    
    # Read access only
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Invalid Name")
        self._name = name
    
    # Read access only
    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, description):
        self._description = description
    
    # Read access only
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, type):
        self._type = type
    
    # Read access only
    @property
    def healing_range(self):
        return self._healing_range
    @healing_range.setter
    def healing_range(self, healing_range):
        self._healing_range = healing_range
        
    # Read access only
    @property
    def accuracy(self):
        return self._accuracy
    @accuracy.setter
    def accuracy(self, accuracy):
        self._accuracy = accuracy
        
    # Read access only
    @property
    def cost(self):
        return self._cost
    @cost.setter
    def cost(self, cost):
        self._cost = cost
    
    # Read access only
    @property
    def healing_min(self):
        return self._healing_min
    @healing_min.setter
    def healing_min(self, healing_min):
        self._healing_min = healing_min
    
    # Read access only
    @property
    def healing_max(self):
        return self._healing_max
    @healing_max.setter
    def healing_max(self, healing_max):
        self._healing_max = healing_max
    
    def __str__(self) -> str:
        return f"{self.name}(Defense, {self.type}, Cost: {self.cost}): {self.description}"