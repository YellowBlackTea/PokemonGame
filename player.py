import csv
import os.path
import random

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
    
    def randomise_team(self, pokemon_data) -> None:
        self.team = [Pokemon(random.choice(pokemon_data)) for _ in range(3)]
        self.all_pkms += self.team
    
    def catch_pokemon(self, wild_pkm):
        current_hp = wild_pkm.current_hp
        
    
    def change_team(self):
        pass
    
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
        
            
    