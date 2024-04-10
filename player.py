import ast
import csv
import os.path
import random
import sys

from utils import get_int
from pokemon import Pokemon

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.team = []
        self.all_pkms = []
        try:
            with open("./data/trainer.txt", 'r') as file:
                reader = csv.DictReader(file, delimiter="\t")
                for row in reader:
                    if row['Name'] == name:
                        self.name = name
                        self.team = self.convert_to_list(row['Team'])
                        self.all_pkms = self.convert_to_list(row['All Pokemon'])
                        break
                else:
                   self.name = name
                   self.team = []
                   self.all_pkms = [] 
        except FileNotFoundError:
            self.name = name
            self.team = []
            self.all_pkms = []
            
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Invalid Name")
        self._name = name
        
    @property
    def team(self):
        return self._team
    @team.setter
    def team(self, team):
        self._team = team
        
    @property
    def all_pkms(self):
        return self._all_pkms
    @all_pkms.setter
    def all_pkms(self, all_pkms):
        self._all_pkms = all_pkms
    
    def __str__(self) -> str:
        """Print string of a Player class.
        It uses the Pokemon class with an additional index.

        Returns:
            str: String of the definition of all Team Pokemon of the Player.
        """
        output = ""
        for idx, pkm in enumerate(self.team):
            output += f"{idx}/ {pkm} \n"
            if idx == 2:
                break
        return output
    
    def __len__(self) -> int:
        """Get number of Pokemon in a team. The max should be set to 3.

        Returns:
            int: The length value of the Pokemon Team list.
        """
        return len(self.team)
    
    def convert_to_list(self, string_list: str) -> list[Pokemon]:
        """Convert a Pokemon string list to an actual Pokemon list.
        E.g. "[Pikachu(Lv 8, ...)..., Pidgeot(Lv1, ...)]" -> [pokemon object, pokemon object]
        Args:
            string_list (str): The Pokemon Team in a string format.

        Returns:
            list[Pokemon]: The Pokemon Team in the correct format of a list of Pokemons.
        """
        return [Pokemon.from_string(item) for item in ast.literal_eval(string_list)]  
    
    def randomise_team(self, pokemon_data: list[dict]) -> None:
        """Randomise the first team of the player.

        Args:
            pokemon_data (list[dict]): list of all Pokemon data read from ./data/pokemon.txt.
        """
        self.team = [Pokemon(random.choice(pokemon_data)) for _ in range(3)]
        if len(self.all_pkms) < 6:
            self.all_pkms += self.team
    
    def catch_pokemon(self, wild_pkm: Pokemon) -> bool:
        """Check if the Pokemon was successfully caught or not.

        Args:
            wild_pkm (Pokemon): Pokemon class of the wild pokemon.

        Returns:
            bool: flag if caught (True) or not (False).
        """
        current_hp = wild_pkm.current_hp
        max_hp = wild_pkm.hp
        
        catch_rate = 4 * (0.2 - (current_hp / max_hp))
        random_rate = random.random()
        if current_hp <= 0.2 * max_hp and random_rate <= catch_rate:
            print(f"Gotcha! Wild {wild_pkm.name} was caught!")
            return True
        
        print(f"Oh, no! The Pokemon broke free!")
        return False
    
    def add_to_all_pkms(self, wild_pkm: Pokemon) -> int | None:
        """Add the wild Pokemon caught to a PC/box where all Pokemon are stored.
        A maximum of 6 Pokemon can be stored.

        Args:
            wild_pkm (Pokemon): The Pokemon caught.

        Returns:
            int: Returns value 0 means that the player successfully caught the Pokemon.
            None: Did not catch the Pokemon.
        """
        bool_gotcha = self.catch_pokemon(wild_pkm)
        # Add Wild Pkm if enough storage
        if bool_gotcha:
            if len(self.all_pkms) < 6:
                self.all_pkms.extend([wild_pkm])
                self.save_info()
                return 0
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
                self.save_info()
                return 0
        else:
            return None
            
    def change_team(self) -> None:
        """In the case the player wants to change its current team before battling.
        """
        if len(self.all_pkms) <= 3:
            print(f"No Pokemon in your PC / box.")
            return None
        
        print(self.__str__())
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
           
    def search_trainer(self, ennemy: str) -> bool:
        """Search for an ennemy player in the ./data/trainer.txt file.

        Args:
            ennemy (str): the name of the ennemy player

        Returns:
            bool: returns True if succesfully found, False otherwise.
        """
        total = sum(1 for _ in open('./data/trainer.txt'))
        with open("./data/trainer.txt", 'r') as file:
            reader = csv.DictReader(file, delimiter="\t")
            if total <= 2:
                sys.exit("You're the only trainer register for now! Game is re-starting to add another player.")
            
            for row in reader:
                if ennemy == row['Name']:
                    return True
            return False
    
    def save_info(self) -> None:
        """Save the info regarding the player in a ./data/trainer.txt file.
        A same name player cannot exist, only the latest player would be kept.
        """
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
        