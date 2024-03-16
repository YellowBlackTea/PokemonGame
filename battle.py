import random

from data import save_data
from utils import get_int
from pokemon import Pokemon
from ability import Attack, Defense

class Battle:
    def __init__(self, self_pokemon: Pokemon, target_pokemon: Pokemon) -> None:
        self.self_pokemon = self_pokemon
        self.target_pokemon = target_pokemon
    
    # Read access only
    @property
    def self_pokemon(self):
        return self._self_pokemon
    @self_pokemon.setter
    def self_pokemon(self, self_pokemon):
        self._self_pokemon = self_pokemon
        
    # Read & write access only
    @property
    def target_pokemon(self):
        return self._target_pokemon
    @target_pokemon.setter
    def target_pokemon(self, target_pokemon):
        self._target_pokemon = target_pokemon

    def calculate_coefficient(self) -> float:
        coefficients = {
            "Air": {"Air": 1, "Water": 0.5, "Fire": 1, "Earth": 1.5},
            "Water": {"Air": 1.5, "Water": 1, "Fire": 1, "Earth": 0.5},
            "Fire": {"Air": 0.5, "Water": 1.5, "Fire": 1, "Earth": 1},
            "Earth": {"Air": 1, "Water": 0.5, "Fire": 1.5, "Earth": 1}
        }
        return float(coefficients[self.self_pokemon.type][self.self_pokemon.type])
    
    def calculate_damage(self, ability: Attack) -> float:
        power = ability.power
        coefficient = self.calculate_coefficient(self.target_pokemon.type)

        damage = round(coefficient * random.uniform(0.85, 1) * (((power * 4 * (self.self_pokemon + 2)) / self.target_pokemon.resitance) + 2))
        return damage
        
    def attack(self, ability: Attack) -> None:
        damage = 0
        if self.self_pokemon.current_energy >= ability.cost:
            print(f"{self.self_pokemon.name} used {ability}!")
            self.self_pokemon.current_energy -= ability.cost
            
            if random.randint(0, 100) < ability.accuracy:
                damage = self.calculate_damage(ability)
                self.target_pokemon.current_hp -= damage
                
                if self.target_pokemon.current_hp < 0:
                    self.target_pokemon.current_hp = 0
                    print(f"{self.target_pokemon.name} is KO!")
            else:
                print(f"{self.self_pokemon.name}'s attack missed!")
        else:
            print(f"Not enough PP / Energy.")
            
        return self.self_pokemon, self.target_pokemon, damage

    def defense(self, ability: Defense) -> None:
        restore_hp = 0
        restore_energy = 0
        if self.self_pokemon.current_energy >= ability.cost:
            print(f"{self.self_pokemon.name} used {ability}!")
            
            restore_hp = random.randint(ability.healing_min, ability.healing_max)
            self.self_pokemon.current += restore_hp
            print(f"{self.self_pokemon.name} regained health!")
            try:
                restore_energy = random.randint(ability.healing_min, ability.healing_max)
                self.current_energy += restore_energy
                print(f"{self.self_pokemon.name} regained energy!")
            except Exception:
                pass
        else:
            print(f"Not enough PP / Energy.")
        
        return self.self_pokemon, restore_hp, restore_energy
    
    def change_pokemon(self, team) -> None:
        changed_pkm = get_int("Which Pokemon to you want to change {self.self_pokemon} with? ")
        while self.self_pokemon.name != team[changed_pkm].name:
            print(f"{self.self_pokemon} is already in battle!")
            changed_pkm = get_int("Which Pokemon to you want to change {self.self_pokemon} with? ")
        
        temp_swap = self.self_pokemon
        self.self_pokemon = team[changed_pkm]
        team[changed_pkm] = temp_swap
        
    def forfeit(self, player) -> int:
        print(f"You have forfeited. You lost!")
        return 0
    
    def get_xp(self, combat='pvp'):
        if combat == 'pvp':
            levels = [self.target_pokemon.level]
            
            avg_levels = self.target_pokemon
    
    def start_battle_restore(self):
        self.self_pokemon.current_hp = self.hp
        self.target_pokemon.current_energy = self.energy
    
    def start(self):
        print("Battle starts!")
        self.self_pokemon.start_battle_restore()
        self.target_pokemon.start_battle_restore()

        while self.are_pokemons_alive(self.self_pokemon) and self.are_pokemons_alive(self.target_pokemon):
            print("\n" + "="*30)
            print(f"{self.self_pokemon.name}: {self.self_pokemon.current_hp}/{self.self_pokemon.hp}")
            print(f"{self.target_pokemon.name}: {self.target_pokemon.current_hp}/{self.target_pokemon.hp}")
            print("="*30 + "\n")

            self.self_pokemon_turn()
            if not self.are_pokemons_alive(self.target_pokemon):
                print(f"{self.target_pokemon.name} has no more Pokemon left!")
                break

            self.target_pokemon_turn()
            if not self.are_pokemons_alive(self.self_pokemon):
                print(f"{self.self_pokemon.name} has no more Pokemon left!")
                break
        
        print("Battle ended!")
        if self.are_pokemons_alive(self.self_pokemon) and not self.are_pokemons_alive(self.target_pokemon):
            print(f"{self.self_pokemon.name} wins!")
        elif self.are_pokemons_alive(self.target_pokemon) and not self.are_pokemons_alive(self.self_pokemon):
            print(f"{self.target_pokemon.name} wins!")
        else:
            print("It's a tie!")

    def start(self):
        print("Battle starts!")
        self.self_pokemon.start
    
    def self_pokemon_turn(self):
        print(f"{self.self_pokemon.name}'s turn:")
        action = input("Choose an action (attack): ").lower()

        if action == "attack":
            move_index = random.randint(0, 2)
            self.self_pokemon.attack(self.self_pokemon.skills[move_index], self.target_pokemon)
        
    def target_pokemon_turn(self):
        print(f"{self.target_pokemon.name}'s turn:")
        move_index = random.randint(0, 2)
        self.target_pokemon.attack(self.target_pokemon.skills[move_index], self.self_pokemon)

    def are_pokemons_alive(self, player):
        return player.current_hp > 0
    
if __name__ == "__main__":
    pokemons = save_data("./data/pokemon.txt")
    self_pokemon_pokemon = Pokemon(pokemons[0])  # Replace {} with appropriate dictionary for player 1's Pokemon
    target_pokemon_pokemon = Pokemon(pokemons[1])  # Replace {} with appropriate dictionary for player 2's Pokemon

    battle = Battle(self_pokemon_pokemon, target_pokemon_pokemon)
    battle.start()