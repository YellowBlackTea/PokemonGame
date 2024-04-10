import random
import time

from battle import Battle
from pokemon import Pokemon
from player import Player
from utils import save_data, get_int
from ability import Attack, Defense

class PVP(Battle):
    attack_list = save_data("./data/attack.txt")
    defense_list = save_data("./data/defense.txt")
    
    def __init__(self, self_pokemon: Pokemon, target_pokemon: Pokemon, player: Player, player2: Player) -> None:
        super().__init__(self_pokemon, target_pokemon, player)
        self.player = player  # for consistency I'll still use player to define Player1
        self.player2 = player2
        
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
    
    def all_ko(self, ennemy: Player) -> int | None:
        """Check if all 3 Pokemon in the team are KO.
        If not, the KO'd Pokemon is replaced by the next one.
        
        Args:
            ennemy (Player): To access name of the ennemy player.
            
        Returns:
            int: Return value 0 means that the player lost his battle.
            None: Not all 3 Pokemon are KO.
        """
        next = 1
        while self.self_pokemon.current_hp == 0:
            self.self_pokemon = self.player.team[next]
            print(f"{self.self_pokemon.name} go!")
            next += 1
            if next > 3:
                print(f"All your Pokemon are KO, you lost!")
                print(f"{ennemy.name} won!")
                return 0
            else:
                return None
    
    def self_pokemon_turn(self, player_pkm: Pokemon) -> None | int:
        """All different actions defining a player's turn.

        Returns:
            None: The battle is not finished, own Pokemons are still alive.
            int: Return value 0 means that the player lost his battle.
        """
        swap_flag = False
        return_output = None
        ennemy = self.player2
        playerr = self.player
        
        # Swap to use invert self.pokemon and self.target role defined in all methods
        if player_pkm == self.target_pokemon:
            swap_flag = True
            temp_swap = self.self_pokemon
            self.self_pokemon = self.target_pokemon
            self.target_pokemon = temp_swap
            ennemy = self.player
            playerr = self.player2
        
        list_skill_format = self.save_indexed_skills(player_pkm)
        last_index = len(list_skill_format)
        
        print(f"\n{playerr.name} {player_pkm.name}'s turn!")
        print(player_pkm)
        print("\n".join([f"{row['Index']}/ {row['Skill']}" for row in list_skill_format]))
        print(f"{last_index}/ Change Pokemon")
        print(f"{last_index + 1}/ Do nothing")
        print(f"{last_index + 2}/ Forfeit")
        action = get_int("Choose an action. ")
        
        while True:
            for ability in list_skill_format:
                if action == ability['Index']:
                    if ability['Type'] == 'atk':
                        return_output = self.attack(ability['Skill'])
                        
                        if swap_flag:
                            temp_swap = self.self_pokemon
                            self.self_pokemon = self.target_pokemon
                            self.target_pokemon = temp_swap 
                        return return_output
                    
                    elif ability['Type'] == 'def':
                        self.defense(ability['Skill'])
                        
                        # Swap back to get ready for next round
                        if swap_flag:
                            temp_swap = self.self_pokemon
                            self.self_pokemon = self.target_pokemon
                            self.target_pokemon = temp_swap 
                        
            if action == last_index:
                self.change_pokemon()
                
                # Swap back to get ready for next round
                if swap_flag:
                    temp_swap = self.self_pokemon
                    self.self_pokemon = self.target_pokemon
                    self.target_pokemon = temp_swap 
                    
                return None
            elif action == last_index + 1:
                self.do_nothing()
                
                # Swap back to get ready for next round
                if swap_flag:
                    temp_swap = self.self_pokemon
                    self.self_pokemon = self.target_pokemon
                    self.target_pokemon = temp_swap 
                    
                return None
            elif action == last_index + 2:
                return_output = self.forfeit(playerr, ennemy)
                
                # Swap back to get ready for next round
                if swap_flag:
                    temp_swap = self.self_pokemon
                    self.self_pokemon = self.target_pokemon
                    self.target_pokemon = temp_swap 
                    
                return return_output
            else:
                action = get_int(f"Please choose an action between 0 - {last_index + 2}. ")
    
    def start(self):
        """Start of the battle defining each round.
        """
        print(f"\nBattle begins!\n")
        time.sleep(1) 
        self.start_battle_restore(target=True)
        
        round = 1
        end = False
        same_round_count = 0
        same_round = False
        
        start = random.randint(0, 1)
        if start == 0:
            print(f"{self.player.name} starts!")
        if start == 1:
            print(f"{self.player2.name} starts!")
            
        # End: 
        #   - all 3 pkms KO --> return 0 (player1 lost, player2 get xp)
        #   - forfeit --> return 0 (player1 lost, player2 get xp)
        while not end:
            if not same_round:
                print("----------")
                print(f"Round {round }")
                same_round = True

            # Start of a round: Player1 starts
            if start == 0: 
                # Special case first Pkm is KO or all 3 are KO
                end = self.all_ko(self.player2)
                if end == 0:
                    avg_lvl = (self.player.team[0].level + self.player.team[1].level + self.player.team[2].level) / 3
                    xp_points = (10 + avg_lvl - self.target_pokemon.level)
                    self.get_xp(xp_points, target=True)
                    print(f"\nBATTLE END")
                    end = True
            
                # Actual start of a round if not KO
                end = self.self_pokemon_turn(self.self_pokemon)
                
                # To test again if any pokemon was KO during this round
                end = self.all_ko(self.player2)
                
                temp_swap = self.self_pokemon
                self.self_pokemon = self.target_pokemon
                self.target_pokemon = temp_swap
                temp_swap = self.player
                self.player = self.player2
                self.player2 = temp_swap

                # Just to not print the Round if ennemy has not played yet
                same_round_count += 1
                
                # End either all 3 KO or forfait
                if end == 0:
                    avg_lvl = (self.player.team[0].level + self.player.team[1].level + self.player.team[2].level) / 3
                    xp_points = (10 + avg_lvl - self.target_pokemon.level)
                    self.get_xp(xp_points, target=True)
                    print(f"\nBATTLE END")
                    end = True
                    
            
            # Start of a round: Player2 starts
            if start == 1:
                # Special case first Pkm is KO or all 3 are KO
                end = self.all_ko(self.player)
                if end == 0:
                    avg_lvl = (self.player2.team[0].level + self.player2.team[1].level + self.player2.team[2].level) / 3
                    xp_points = (10 + avg_lvl - self.self_pokemon.level)
                    self.get_xp(xp_points)
                    print(f"\nBATTLE END")
                    end = True
                                  
                # Actual start of a round if not KO
                end = self.self_pokemon_turn(self.target_pokemon)
                
                # To test again if any pokemon was KO during this round
                end = self.all_ko(self.player)
                
                temp_swap = self.self_pokemon
                self.self_pokemon = self.target_pokemon
                self.target_pokemon = temp_swap
                temp_swap = self.player
                self.player = self.player2
                self.player2 = temp_swap

                # Just to not print the Round if ennemy has not played yet
                same_round_count += 1
                
                # End either all 3 KO or forfeit
                if end == 0:
                    avg_lvl = (self.player2.team[0].level + self.player2.team[1].level + self.player2.team[2].level) / 3
                    xp_points = (10 + avg_lvl - self.self_pokemon.level)
                    self.get_xp(xp_points)
                    print(f"\nBATTLE END")
                    end = True
            
            if same_round_count == 2:
                round += 1
                same_round_count = 0
                same_round = False
            else:
                same_round = True
            
        # return main menu???
        