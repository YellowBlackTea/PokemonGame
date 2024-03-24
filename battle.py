import random

from utils import save_data, get_int

from ability import Attack, Defense
from player import Player
from pokemon import Pokemon

class Battle:
    def __init__(self, self_pokemon: Pokemon, target_pokemon: Pokemon, player: Player) -> None:
        self.self_pokemon = self_pokemon
        self.target_pokemon = target_pokemon
        self.player = player
    
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

    # Read access only
    @property
    def player(self):
        return self._player
    @player.setter
    def player(self, player):
        self._player = player

    def calculate_coefficient(self, ability: Attack) -> float:
        coefficients = {
            "Air": {"Air": 1, "Water": 0.5, "Fire": 1, "Earth": 1.5},
            "Water": {"Air": 1.5, "Water": 1, "Fire": 1, "Earth": 0.5},
            "Fire": {"Air": 0.5, "Water": 1.5, "Fire": 1, "Earth": 1},
            "Earth": {"Air": 1, "Water": 0.5, "Fire": 1.5, "Earth": 1}
        }
        return float(coefficients[self.self_pokemon.type][ability.type])
    
    def calculate_damage(self, ability: Attack) -> float:
        power = ability.power
        coefficient = self.calculate_coefficient(ability)

        damage = round(coefficient * random.uniform(0.85, 1) * (((power * 4 * (self.target_pokemon.level + 2)) / self.target_pokemon.resistance) + 2))
        return damage
        
    def attack(self, ability: Attack) -> None:
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
                    return 1
            else:
                print(f"{self.self_pokemon.name}'s attack missed!")
                return None
        else:
            print(f"Not enough PP / Energy.")
            return None

    def defense(self, ability: Defense) -> None:
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
        
    def change_pokemon(self) -> None:
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
        
    def forfeit(self, player) -> int:
        print(f"You have forfeited. You lost!")
        return 0
    
    def get_xp(self, xp_points: int) -> None:
        self.self_pokemon.current_exp += xp_points
        if self.self_pokemon.current_exp <= 100:
            self.self_pokemon.level += 1
            self.self_pokemon.hp += random.randint(1, 5)
            self.self_pokemon.energy += random.randint(1, 5) 
            self.self_pokemon.resistance += random.randint(1, 5)
    
    def start_battle_restore(self):
        self.self_pokemon.current_hp = self.self_pokemon.hp
        self.self_pokemon.current_energy = self.self_pokemon.energy
    
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
   
    def target_pokemon_turn(self):
        print(f"{self.target_pokemon.name}'s turn:")
        move_index = random.randint(0, 2)
        self.target_pokemon.attack(self.target_pokemon.skills[move_index], self.self_pokemon)

    def are_pokemons_alive(self, player):
        return player.current_hp > 0
    
if __name__ == "__main__":
    pokemons = save_data("./data/pokemon.txt")
    players = save_data("./data/trainer.txt")
    #self_pokemon_pokemon = Pokemon(pokemons[0])  
    target_pokemon_pokemon = Pokemon(pokemons[1])

    player = Player('Joe')
    player.randomise_team(pokemons)
    self_pokemon_pokemon = player.team[0]
    print(player)
    print(self_pokemon_pokemon)
    print("====")
    battle = Battle(self_pokemon_pokemon, target_pokemon_pokemon, player)
    battle.change_pokemon()