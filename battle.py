import random

from utils import get_int

from ability import Attack, Defense
from player import Player
from pokemon import Pokemon

class Battle:
    def __init__(self, self_pokemon: Pokemon, target_pokemon: Pokemon, player: Player) -> None:
        self.self_pokemon = self_pokemon
        self.target_pokemon = target_pokemon
        self.player = player
    
    @property
    def self_pokemon(self):
        return self._self_pokemon
    @self_pokemon.setter
    def self_pokemon(self, self_pokemon):
        self._self_pokemon = self_pokemon
        
    @property
    def target_pokemon(self):
        return self._target_pokemon
    @target_pokemon.setter
    def target_pokemon(self, target_pokemon):
        self._target_pokemon = target_pokemon

    @property
    def player(self):
        return self._player
    @player.setter
    def player(self, player):
        self._player = player

    def calculate_coefficient(self, ability: Attack) -> float:
        """Coefficient used in the formula to calculate damage.

        Args:
            ability (Attack): Ability as defined in the Attack class. It has a name, a description, a type a cost, a power and accuracy.
        
        Returns:
            float: coefficient calulated
        """
        coefficients = {
            "Air": {"Air": 1, "Water": 0.5, "Fire": 1, "Earth": 1.5},
            "Water": {"Air": 1.5, "Water": 1, "Fire": 1, "Earth": 0.5},
            "Fire": {"Air": 0.5, "Water": 1.5, "Fire": 1, "Earth": 1},
            "Earth": {"Air": 1, "Water": 0.5, "Fire": 1.5, "Earth": 1}
        }
        return float(coefficients[self.self_pokemon.type][ability.type])
    
    def calculate_damage(self, ability: Attack) -> float:
        """Calculate damage using the formula provided in the instruction.

        Args:
            ability (Attack): Ability as defined in the Attack class. It has a name, a description, a type a cost, a power and accuracy.
        
        Returns:
            float: damage calulated
        """
        power = ability.power
        coefficient = self.calculate_coefficient(ability)

        damage = round(coefficient * random.uniform(0.85, 1) * (((power * 4 * (self.target_pokemon.level + 2)) / self.target_pokemon.resistance) + 2))
        return damage
        
    def attack(self, ability: Attack) -> None | int:
        """Attack skill is used. 
        If the Pokemon has enough Energy to use the skill, 
        then attack or missed according to the formula in description.
        path=./data/attack.txt to know more about each attack property.

        Args:
            ability (Attack): Ability as defined in the Attack class. It has a name, a description, a type a cost, a power and accuracy.
        """
        damage = 0
        if self.self_pokemon.current_energy >= ability.cost:
            print(f"{self.self_pokemon.name} used {ability.name}!")
            self.self_pokemon.current_energy -= ability.cost
            
            if random.randint(0, 100) < ability.accuracy:
                damage = self.calculate_damage(ability)
                self.target_pokemon.current_hp -= damage
                print(f"{damage:>5} dealt!")
                if self.target_pokemon.current_hp < 0:
                    self.target_pokemon.current_hp = 0
                    print(f"{self.target_pokemon.name} is KO!")
                    return None
            else:
                print(f"{self.self_pokemon.name}'s attack missed!")
                return None
        else:
            print(f"Not enough PP / Energy.")
            return None

    def defense(self, ability: Defense):
        """Defense skill is used. 
        If the Pokemon has enough Energy to use the skill, 
        then restore HP or Energy according to a random int between two values defined in the ./data/defense.txt file.

        Args:
            ability (Defense): Ability as defined in the Defense class. It has a name, a description, a type a cost, and healing and energy range.
        """
        restore_hp = 0
        restore_energy = 0

        if self.self_pokemon.current_energy >= ability.cost:
            print(f"{self.self_pokemon.name} used {ability.name}!")
            
            #print(ability.healing_min, ability.healing_max)
            restore_hp = random.randint(ability.healing_min, ability.healing_max)
            
            # Only restore if health is not max
            if self.self_pokemon.current_hp != self.self_pokemon.hp:
                self.self_pokemon.current_hp += restore_hp
                print(f"{self.self_pokemon.name} regained health!")
            else:
                print(f"{self.self_pokemon.name} health is already at max!")
            
            # Check Energy range does exist
            try:
                restore_energy = random.randint(ability.energy_min, ability.energy_max)
                if self.self_pokemon.current_energy != self.energy:
                    self.current_energy += restore_energy
                    print(f"{self.self_pokemon.name} regained energy!")
                else:
                    print(f"{self.self_pokemon.name} energy is already at max!")
            except Exception:
                pass
        else:
            print(f"Not enough PP / Energy.")
        
    def change_pokemon(self):
        """Change current Pokemon with another in the current team.
        """
        print(self.player)
        changed_pkm = get_int(f"Which Pokemon do you want to change {self.self_pokemon.name} with? ")
           
        while self.self_pokemon.current_hp == 0:
            print(f"{self.self_pokemon.name} is KO!")
            changed_pkm = get_int(f"Which Pokemon to you want to change {self.self_pokemon.name} with? ")
               
        while self.self_pokemon.name == self.player.team[changed_pkm].name:
            print(f"{self.self_pokemon.name} is already in battle!")
            changed_pkm = get_int(f"Which Pokemon to you want to change {self.self_pokemon.name} with? ")
        
        temp_swap = self.self_pokemon
        self.self_pokemon = self.player.team[changed_pkm]
        self.player.team[changed_pkm] = temp_swap
        
        print(f"{temp_swap.name} went back to his Pokeball.\n{self.self_pokemon.name} go!")
        
    def forfeit(self, player: Player, ennemy: Player) -> int:
        """Print result if player has chosen to forfeit.

        Args:
            ennemy (Player): To access name of the ennemy player.
            
        Returns:
            int: Return value 0 means that the player lost his battle.
        """
        print(f"{player.name} forfeited. {ennemy.name} wins!")
        return 0
    
    def get_xp(self, xp_points: float, target: bool = False):
        """Get XP points to the amount of the varoable xp_points.

        Args:
            xp_points (float): xp calulated using formula provided in the instruction.
                - pve: round((10 + wild_pkm_lvl - own_pkm_lvl) / 3)
                - pvp: round(10 + avg_target_lvl - own_pkm_lvl)
            target (bool, optional): If player1 loses, then use target/ennemy formula to gain xp. Defaults to False.
        """
        if target:
            self.target_pokemon.current_exp += xp_points
            if self.target_pokemon.current_exp <= 100:
                self.target_pokemon.level += 1
                self.target_pokemon.hp += random.randint(1, 5)
                self.target_pokemon.energy += random.randint(1, 5) 
                self.target_pokemon.resistance += random.randint(1, 5)
            return
            
        self.self_pokemon.current_exp += xp_points
        if self.self_pokemon.current_exp <= 100:
            self.self_pokemon.level += 1
            self.self_pokemon.hp += random.randint(1, 5)
            self.self_pokemon.energy += random.randint(1, 5) 
            self.self_pokemon.resistance += random.randint(1, 5)
    
    def start_battle_restore(self, target: bool = False):
        """Start each battle with all Pokemon stats restored to its max value.

        Args:
            target (bool, optional): Restore also stats for the ennmy/target Pokemon in case of PvP. Defaults to False.
        """
        self.self_pokemon.current_hp = self.self_pokemon.hp
        self.self_pokemon.current_energy = self.self_pokemon.energy

        if target:
            self.target_pokemon.current_hp = self.target_pokemon.hp
            self.target_pokemon.current_energy = self.target_pokemon.energy
        