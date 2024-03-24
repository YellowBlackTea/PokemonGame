import re
from utils import save_data

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
        return f"{self.name:<13} (Attack, {self.type}, Cost: {self.cost:<2}): {self.description}"
    
    def attack_success(self):
        pass
        

class Defense:    
    def __init__(self, defense_dict) -> None:
        self.name = defense_dict.get('Name')
        self.description = defense_dict.get('Description')
        self.type = defense_dict.get('Element')
        self.healing_range = defense_dict.get('Healing')
        self.energy_range_range = defense_dict.get('Energy')
        self.cost = int(defense_dict.get('Cost'))
        
        # Extract min-max of the healing range, and set the energy_range to 0
        try:
            self.healing_min, self.healing_max = map(int, re.search(r"([0-9]+)?(?:\s+)?-(?:\s+)?([0-9]+)?", self.healing_range).groups())
            self.energy_range_range = 0
        except (AttributeError, TypeError):
            self.healing_min, self.healing_max = None, None
        
        # Extract min-max of the energy_range range, and set the healing to 0 
        try:
            self.energy_range_min, self.energy_range_max = map(int, re.search(r"([0-9]+)?(?:\s+)?-(?:\s+)?([0-9]+)?", self.energy_range_range).groups())
            self.healing_range = 0
        except (AttributeError, TypeError):
            self.energy_range_min, self.energy_range_max = None, None
    
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
    def energy_range(self):
        return self._energy_range
    @energy_range.setter
    def energy_range(self, energy_range):
        self._energy_range = energy_range
        
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
    
    # Read access only
    @property
    def energy_min(self):
        return self._energy_min
    @energy_min.setter
    def energy_min(self, energy_min):
        self._energy_min = energy_min
    
    # Read access only
    @property
    def energy_max(self):
        return self._energy_max
    @energy_max.setter
    def energy_max(self, energy_max):
        self._energy_max = energy_max
    
    def __str__(self) -> str:
        return f"{self.name:<13} (Defense, {self.type}, Cost: {self.cost}): {self.description}"