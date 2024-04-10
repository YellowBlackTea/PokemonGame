import random
import time

from battle import Battle
from pokemon import Pokemon
from player import Player
from utils import save_data, get_int
from ability import Attack, Defense

class PVE(Battle):
    attack_list = save_data("./data/attack.txt")
    defense_list = save_data("./data/defense.txt")
    
    def __init__(self, self_pokemon: Pokemon, target_pokemon: Pokemon, player: Player) -> None:
        super().__init__(self_pokemon, target_pokemon, player)
    
    def randomize_wild_pokemon(self, pokemon_data: list[dict]):
        """Randomize the wild pokemon's stats.

        Args:
            pokemon_data (list[dict]): Pokemon data file using the ./utils/save_data format.
        """
        self.target_pokemon = Pokemon(random.choice(pokemon_data))
    
    def who_start(self, start: int = None) -> int:
        """Randomize whose turn it is for the round, then lock it into that cycle.

        Args:
            start (int, optional): If the cycle is defined, then this cycle of turn is maintained using this variable. 
            Defaults to None, meaning the cycle is not define yet.

        Returns:
            int: The start variable to know which cycle was chosen randomly.
        """
        if not start:
            start = random.randint(0, 1)
         
        if start == 0:
            self.self_pokemon_turn()
            self.target_pokemon_turn() 

        if start == 1:
            self.target_pokemon_turn()  
            self.self_pokemon_turn()
        
        return start
        
    def save_indexed_skills(self, which_pkm: Pokemon) -> list[dict]:
        """Save a dict of skills in a specific format with their indexes.

        Returns:
            list[dict]: Each row is associated with an Attack or Defense + its index.
        """
        skills = which_pkm.skills.split(', ')  # transform str to Python list
        list_dict = [] 
        
        # For each skill in the Skills List, print its info with the correct index
        for idx, skill in enumerate(skills):
            # Create boolean variables
            isAttack = False
            isDefense = False
            
            for _, atk in enumerate(self.attack_list):
                if not isDefense and Attack(atk).name == skill:
                    #print(f"{idx}/ {Attack(atk)}")
                    list_dict.append({'Index': idx, 'Skill': Attack(atk), 'Type': 'atk'})
                    isAttack = True
                    break
            for _, defs in enumerate(self.defense_list):
                if not isAttack and Defense(defs).name == skill:
                    #print(f"{idx}/ {Defense(defs)}")
                    list_dict.append({'Index': idx, 'Skill': Defense(defs), 'Type': 'def'})
                    isDefense = True
                    break
        
        return list_dict
    
    def do_nothing(self):
        """Print result if player has chosen to do nothing;
        """
        print(f"{self.self_pokemon.name} is staring at you...")
    
    def flee(self) -> int:
        """Print result if player has chosen to flee.

        Returns:
            int: Return value 0 means that the player lost his battle.
        """
        print(f"You got away safely.")
        return 0
    
    def all_ko(self) -> int | None:
        """Check if all 3 Pokemon in the team are KO.
        If not, the KO'd Pokemon is replaced by the next one.

        Returns:
            int: Return value 0 means that the player lost his battle.
            None: Not all 3 Pokemon are KO.
        """
        next = 1
        while self.self_pokemon.current_hp == 0:
            print(f"{self.self_pokemon.name} is KO.")
            self.self_pokemon = self.player.team[next]
            print(f"{self.self_pokemon.name} go!")
            next += 1
            if next > 3:
                print(f"All your Pokemon are KO, you lost!")
                return 0
            else:
                return None
    
    def self_pokemon_turn(self) -> None | int:
        """All different actions defining a player's turn.

        Returns:
            None: The battle is not finished, own Pokemons are still alive.
            int: Return value 0 means that the player lost his battle.
        """
        list_skill_format = self.save_indexed_skills(self.self_pokemon)
        last_index = len(list_skill_format)
        
        print(f"\n{self.self_pokemon.name}'s turn!")
        print(self.self_pokemon)
        print("\n".join([f"{row['Index']}/ {row['Skill']}" for row in list_skill_format]))
        print(f"{last_index}/ Change Pokemon")
        print(f"{last_index + 1}/ Catch Pokemon")
        print(f"{last_index + 2}/ Do nothing")
        print(f"{last_index + 3}/ Flee")
        action = get_int("Choose an action. ")
        
        while True:
            for ability in list_skill_format:
                if action == ability['Index']:
                    if ability['Type'] == 'atk':
                        return self.attack(ability['Skill'])
                    elif ability['Type'] == 'def':
                        self.defense(ability['Skill'])
                        return None  # Nothing is returned for defense()
                        
            if action == last_index:
                self.change_pokemon()
                return None
            elif action == last_index + 1:
                return self.player.add_to_all_pkms(self.target_pokemon)
            elif action == last_index + 2:
                self.do_nothing()
                return None
            elif action == last_index + 3:
                return self.flee()
            else:
                action = get_int(f"Please choose an action between 0 - {last_index + 3}. ")
    
    def target_pokemon_turn(self):
        """Wild Pokemon's turn whose only action is to use a skill. The choice of the skill is randomize.
        """
        # Check if target pkm is not KO
        if self.target_pokemon.current_hp == 0:
            return True
        
        list_skill_format = self.save_indexed_skills(self.target_pokemon)
        
        print(f"Wild {self.target_pokemon.name}'s turn!")
        rand_skill = random.choice(list_skill_format)
        
        # Sleep to slow down the process
        time.sleep(1)

        # Swap to use the Ability class
        temp_swap = self.self_pokemon
        self.self_pokemon = self.target_pokemon
        self.target_pokemon = temp_swap
        
        if rand_skill['Type'] == 'atk':
            self.attack(rand_skill['Skill'])
            
            # Swap back to get ready for next round
            temp_swap = self.self_pokemon
            self.self_pokemon = self.target_pokemon
            self.target_pokemon = temp_swap

        elif rand_skill['Type'] == 'def':
            self.defense(rand_skill['Skill'])
            
            # Swap back to get ready for next round
            temp_swap = self.self_pokemon
            self.self_pokemon = self.target_pokemon
            self.target_pokemon = temp_swap   
     
    def start(self):
        """Start of the battle defining each round.
        """
        print("\n\nBattle begins!\n")
         
        self.start_battle_restore()
        
        round = 1
        end = False
        target_ko = False
        start = random.randint(0, 1)
         
        # End: 
        #   - all 3 pkms KO --> return 0 (no xp)
        #   - target pkm KO --> return 1 + get xp
        #   - target pkm gotcha --> return 0 (no xp)
        #   - flee --> return 0 (no xp)
        while not end:
            print("----------")
            print(f"Round {round}")
            
            if start == 0: 
                # Special case all 3 are KO, if first pkm KO then next one
                end = self.all_ko()
                if end == 0:
                    print(f"\nBATTLE END")
                    end = True
                    break
            
                # Start of a round = my pkm starts
                end = self.self_pokemon_turn()
    
                # End either all 3 KO or caught target pkm or flee
                if end == 0:
                    print(f"\nBATTLE END")
                    end = True
                    break
                
                target_ko = self.target_pokemon_turn() 
                # End KO'd target pkm + get xp
                if target_ko == True:
                    xp_points = (10 + self.target_pokemon.level - self.self_pokemon.level) / 3
                    self.get_xp(xp_points)
                    print(self.self_pokemon)
                
            
            # Start of a round: target starts
            if start == 1:
                # Special case all 3 are KO, if first pkm KO then next one
                end = self.all_ko()
                if end == 0:
                    print(f"\nBATTLE END")
                    end = True
                    break
                target_ko = self.target_pokemon_turn()  
                
                # Start of a round (case 1)
                end = self.self_pokemon_turn()
                
                # End either all 3 KO or caught target pkm or flee
                if end == 0:
                    print(f"\nBATTLE END")
                    end = True
                    break
                
                # End KO'd target pkm + get xp
                if target_ko == True:
                    xp_points = round((10 + self.target_pokemon.level - self.self_pokemon.level) / 3)
                    self.get_xp(xp_points)
                    print(self.self_pokemon)
            
            round += 1
            
        