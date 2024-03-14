
import random
import re

class Pokemon:
    def __init__(self, pokemon_dict) -> None:
        # Initialize variables from dict
        self.name = pokemon_dict.get('Name')
        #self.before = pokemon_dict.get('Before')
        self.evolve = pokemon_dict.get('After')
        self.type = pokemon_dict.get('Element')
        self.level_range = pokemon_dict.get('Level')
        self.hp_range = pokemon_dict.get('HP')
        self.energy_range = pokemon_dict.get('Energy')
        self.regeneration_range = pokemon_dict.get('Regeneration')
        self.resistance_range = pokemon_dict.get('Resistance')
        self.skills = pokemon_dict.get('Skills')
        
        # Initialize variables from generate_random_stats() method
        self.level, self.level_max, self.hp, self.energy, self.regeneration, self.resistance = self.generate_random_stats()
        
        # Initialize variables from current stats
        self.current_hp = self.hp
        self.current_exp = self.level * 100 + 0
        
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
    def evolve(self):
        return self._evolve
    @evolve.setter
    def evolve(self, evolve):
        self._evolve = evolve
        
    # Read access only
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, type):
        if not type:
            raise ValueError("Invalid Element Type")
        self._type = type
    
    # Read access only
    @property
    def level_range(self):
        return self._level_range
    @level_range.setter
    def level_range(self, level_range):
        if not level_range:
            raise ValueError("Invalid Level range")
        self._level_range = level_range
        
    # Read access only
    @property
    def hp_range(self):
        return self._hp_range
    @hp_range.setter
    def hp_range(self, hp_range):
        if not hp_range:
            raise ValueError("Invalid HP range")
        self._hp_range = hp_range
        
    # Read access only
    @property
    def energy_range(self):
        return self._energy_range
    @energy_range.setter
    def energy_range(self, energy_range):
        if not energy_range:
            raise ValueError("Invalid Energy range")
        self._energy_range = energy_range
        
    # Read access only
    @property
    def regeneration_range(self):
        return self._regeneration_range
    @regeneration_range.setter
    def regeneration_range(self, regeneration_range):
        if not regeneration_range:
            raise ValueError("Invalid Regeneration range")
        self._regeneration_range = regeneration_range
        
    # Read access only
    @property
    def resistance_range(self):
        return self._resistance_range
    @resistance_range.setter
    def resistance_range(self, resistance_range):
        if not resistance_range:
            raise ValueError("Invalid Resistance range")
        self._resistance_range = resistance_range
        
    # Read + write access only
    @property
    def skills(self):
        return self._skills
    @skills.setter
    def skills(self, skills):
        if not skills:
            raise ValueError("Invalid Skills")
        self._skills = skills 
        
    # Read + write access only
    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, level):
        if not level:
            raise ValueError("Invalid Level")
        self._level = level
        
    # Read access only
    @property
    def level_max(self):
        return self._level_max
    @level_max.setter
    def level_max(self, level_max):
        self._level_max = level_max
    
    # Read access only
    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, hp):
        self._hp = hp    
     
    # Read access only
    @property
    def energy(self):
        return self._energy
    @energy.setter
    def energy(self, energy):
        self._energy = energy  
    
    # Read access only
    @property
    def regeneration(self):
        return self._regeneration
    @regeneration.setter
    def regeneration(self, regeneration):
        self._regeneration = regeneration 
        
    # Read access only
    @property
    def resistance(self):
        return self._resistance
    @resistance.setter
    def resistance(self, resistance):
        self._resistance = resistance   
            
    # Read access only
    @property
    def current_hp(self):
        return self._current_hp
    @current_hp.setter
    def current_hp(self, current_hp):
        self._current_hp = current_hp   
    
    # Read access only
    @property
    def current_exp(self):
        return self._current_exp
    @current_exp.setter
    def current_exp(self, current_exp):
        self._current_exp = current_exp   
        
    def __str__(self) -> str:
        return f"{self.name}(Lv {self.level}, {self.current_exp}/{self.level_max*100}, {self.type}): "\
               f"HP {self.current_hp}/{self.hp}, Energy {self.energy}/{self.energy} (+{self.regeneration}), Resistance {self.resistance}"\
               f"\n {self.skills}"
    
    def generate_random_stats(self):
        
        # Find the min and max value for these ranges
        level_min, level_max = map(int, re.match(r"([0-9]+)?\s+-\s+([0-9]+)?", self.level_range).groups())
        hp_min, hp_max = map(int, re.match(r"([0-9]+)?\s+-\s+([0-9]+)?", self.hp_range).groups())
        energy_min, energy_max = map(int, re.match(r"([0-9]+)?\s+-\s+([0-9]+)?", self.energy_range).groups())
        regeneration_min, regeneration_max = map(int, re.match(r"([0-9]+)?\s+-\s+([0-9]+)?", self.regeneration_range).groups())
        resistance_min, resistance_max = map(int, re.match(r"([0-9]+)?\s+-\s+([0-9]+)?", self.resistance_range).groups())

        # Raise an error if value does not exist
        if not level_min or not level_max:
            raise ValueError("Missing appropriate level range")
        if not hp_min or not hp_max:
            raise ValueError("Missing appropriate hp range")
        if not energy_min or not energy_max:
            raise ValueError("Missing appropriate energy range")
        if not regeneration_min or not regeneration_max:
            raise ValueError("Missing appropriate regeneration range")
        if not resistance_min or not resistance_max:
            raise ValueError("Missing appropriate resistance range")
        
        # Generate random stats
        level = random.randint(level_min, level_max)
        regeneration = random.randint(regeneration_min, regeneration_max)
        
        hp = hp_min + random.randint(1, 5) * (level - level_min)
        energy = energy_min + random.randint(1, 5) * (level - level_min)
        resistance = resistance_min + random.randint(1, 5) * (level - level_min)
        
        # Convert Skills variable to Python List
        skills = re.match(r"\[([^\]]+)\]", self.skills)
        if not skills:
            raise ValueError("Missing skills")
        self.skills = skills.group(1)

        return level, level_max, hp, energy, regeneration, resistance
               