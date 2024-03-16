import csv
import os.path
import random

from data import save_data
from functional import get_int
from pokemon import Pokemon

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.team = []
        self.all_pkms = []
        
    # Read access only
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Invalid Name")
        self._name = name
        
    # Read & write access only
    @property
    def team(self):
        return self._team
    @team.setter
    def team(self, team):
        self._team = team
        
    # Read & write access only
    @property
    def all_pkms(self):
        return self._all_pkms
    @all_pkms.setter
    def all_pkms(self, all_pkms):
        self._all_pkms = all_pkms
    
    def __str__(self) -> str:
        output = ""
        for idx, pkm in enumerate(self.team):
            output += f"{idx}/ {pkm} \n"
            if idx == 2:
                break
        return output
    
    def __len__(self) -> int:
        return len(self.team)
    
    def randomise_team(self, pokemon_data: list[dict]) -> None:
        self.team = [Pokemon(random.choice(pokemon_data)) for _ in range(3)]
        self.all_pkms += self.team
    
    def catch_pokemon(self, wild_pkm: Pokemon) -> bool:
        current_hp = wild_pkm.current_hp
        max_hp = wild_pkm.hp
        
        catch_rate = 4 * (0.2 - (current_hp / max_hp))
        random_rate = random.random()
        if current_hp <= 0.2 * max_hp and random_rate <= catch_rate:
            self.all_pkms.append(wild_pkm)
            print(f"Gotcha! Wild {wild_pkm.name} was caught!")
            return True
        
        print(f"Oh, no! The Pokemon broke free!")
        return False
    
    def change_team(self) -> None:
        change_pkm_team = get_int("Which Pokemon do you want to change? Please choose a number between 0 to 2. ")
        while not (0 <= change_pkm_team <= 2):
            change_pkm_team = get_int("Which Pokemon do you want to change? Please choose a number between 0 to 2. ")
            
        print("This is your remaining Pokemon:")
        output = ""
        for idx, pkm in enumerate(self.all_pkms):
            if idx <= 2:
                pass
            else:
                output += f"{idx}/ {pkm} \n"
        print(f"{output}")
        
        new_pkm_team = get_int("Which Pokemon do you want to replace? Please choose a number between 3 to 5. ")
        while not (3 <= new_pkm_team <= 5):
            new_pkm_team = get_int("Which Pokemon do you want to replace? Please choose a number between 3 to 5. ")
        
        temp_swap = self.team[change_pkm_team]
        self.team[change_pkm_team] = self.all_pkms[new_pkm_team]
        self.all_pkms[new_pkm_team] = temp_swap
        
        #return self.team, self.all_pkms
        
    def search_trainer(self, ennemy: str) -> dict:
        player2 = {}
        try:
            with open("./data/trainer.txt", 'r') as file:
                reader = csv.DictReader(file, delimiter="\t")
                
                for row in reader:
                    if ennemy == row['Name']:
                        player2['Name'] = ennemy
                        player2['Team'] = row['Team']
                        return player2
        except FileNotFoundError:
            print(f"You're the only trainer register for now! Re-run the game to add another player.")
    
    def save_info(self) -> None:
        file_exists = os.path.isfile("./data/trainer.txt")
        header = ['Name', 'Team', 'All Pokemon']
        old_file = []
        
        # Open the file to remove redundant information
        try:
            with open("./data/trainer.txt", 'r+') as file:
                reader = csv.DictReader(file, fieldnames=header, delimiter="\t")
                writer = csv.writer(file, delimiter="\t")
                
                for row in reader:
                    # Remove old trainer info
                    if self.name != row['Name']:
                        old_file.append(row)
        except FileNotFoundError:
            pass
       
        with open("./data/trainer.txt", 'w') as file:
            writer = csv.DictWriter(file, fieldnames=header, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\t")
            
            # Write header only when creating the file
            if not file_exists:
                writer.writeheader()
            
            # Append old save info without same name info
            if old_file != []:
                writer.writerows(old_file)
                
            writer.writerow({'Name': self.name, 'Team': [str(pkm) for pkm in self.team], 'All Pokemon': [str(pkm) for pkm in self.all_pkms]})
        
def main():
    pokemons = save_data("./data/pokemon.txt")
    ash = Player('ash')
    ash.randomise_team(pokemons)
    print(ash)
    ash.randomise_team(pokemons)
    print(ash)
    ash.save_info()
    ash.change_team()
    print(ash)
    """ wild_pkm_full_hp = {'Name': 'Pikachu', 'Before': '', 'After': 'Raichu', 'Element': 'Air','Level': '5', 
                        'HP': '150', 'Energy': '65', 'Regeneration': '9','Resistance': '45', 
                        'Skills': '[Thunderbolt, Thunder, Thunder Shock]'}
    
    wild_pkm_dying_hp = {'Name': 'Pikachu', 'Before': '', 'After': 'Raichu', 'Element': 'Air','Level': '5', 
                        'HP': '20', 'Energy': '65', 'Regeneration': '9','Resistance': '45', 
                        'Skills': '[Thunderbolt, Thunder, Thunder Shock]'}
    """
    
    ennemy = ash.search_trainer('RED')
    print(ennemy)
    ash.save_info()

            
if __name__ == "__main__":
    main()