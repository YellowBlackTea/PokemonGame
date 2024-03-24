import csv
import os.path
import random

from utils import save_data, get_int
from pokemon import Pokemon

class Player:
    def __init__(self, name) -> None:
        try:
            with open("./data/trainer.txt", 'r') as file:
                reader = csv.DictReader(file, delimiter="\t")
                for row in reader:
                    if row['Name'] == name:
                        self.name = name
                        self.team = row['Team']
                        self.all_pkms = row['All Pokemon']
                else:
                   self.name = name
                   self.team = []
                   self.all_pkms = [] 
        except FileNotFoundError:
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
    
    def add_to_all_pkms(self, wild_pkm: Pokemon):
        bool_gotcha = self.catch_pokemon(wild_pkm)
        # Add Wild Pkm if enough storage
        if bool_gotcha:
            if len(self.all_pkms) < 6:
                self.all_pkms += [wild_pkm]
            # Add Wild Pkm by releasing another one
            else:
                print(self.player.all_pkms)
                released_pkm = get_int(f"You have too much Pokemon, who do you want to release? ")
                print(f"7/ {wild_pkm.name}")
                while released_pkm > 8:
                    released_pkm = get_int(f"Please choose a number between 0 - 7, who do you want to release? ")
                if released_pkm == 7:
                    print(f"Bye bye {wild_pkm.name}!")
                    return 0
                print(f"Bye bye {self.player.all_pkms[released_pkm].name}!")
                self.player.all_pkms[released_pkm] = wild_pkm
                return 0
        else:
            return None
            
    def change_team(self) -> None:
        self.__str__()
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
    ash = Player('RED')
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