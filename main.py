import random
import sys

import pyfiglet

from utils import save_data, get_int

from pokemon import Pokemon
from player import Player
from pve import PVE
from pvp import PVP

def main():
    print(pyfiglet.figlet_format("Welcome to OOP-kemon", font = "slant", width = 250))
    pokemons = save_data("./data/pokemon.txt")
    
    menu_screen(pokemons)
    
    
def menu_screen(pokemon_data: list[dict]) -> None:
    """Show the main menu screen.

    Args:
        pokemon_data (list[dict]): list of all Pokemon data read from ./data/pokemon.txt.
    """
    name = input("What's your name? ")
    player = Player(name)
    player.randomise_team(pokemon_data)
    
    # if player exists, show him his pokemon
    print(f"Hello {name}, you have {len(player)} Pokemon. Your current team is: \n")
    
    # Print each Pokemon + its specifities (atk, hp, etc)
    print(player)
    player.save_info()
    print("------------------------------------------------")
    # Print Menu option
    print(f"{'1/ Change Team':<15} - Change your Pokemon team")
    print(f"{'2/ PvE':<15} - Battle or Catch a wild Pokemon")
    print(f"{'3/ PvP':<15} - Battle another trainer")
    print(f"{'4/ Quit':<15}")
    print(f"To create another trainer/player, please quit and re-run the game.")
    print("------------------------------------------------")
    choose_action(player, pokemon_data)


def choose_action(player: Player, pokemon_data: list[dict]) -> None:
    """Choose an action from the different options in the menu screen.

    Args:
        player (Player): Name or player class of the first player.
        pokemon_data (list[dict]): list of all Pokemon data read from ./data/pokemon.txt.
    """
    action = get_int("Choose an action. ")
    play = True
    while play:
        match action:
            case 1:
                player.change_team()
                print(f"\n\nGoing back to main menu...")
                print("------------------------------------------------")
                print(f"{'1/ Change Team':<15} - Change your Pokemon team")
                print(f"{'2/ PvE':<15} - Battle or Catch a wild Pokemon")
                print(f"{'3/ PvP':<15} - Battle another trainer")
                print(f"{'4/ Quit':<15}")
                print(f"To create another trainer/player, please quit and re-run the game.")
                print("------------------------------------------------")
                choose_action(player, pokemon_data)
                
            case 2:
                wild_pkm = Pokemon(random.choice(pokemon_data))
                initial_pkm = player.team[0]
                pve = PVE(initial_pkm, wild_pkm, player)
                pve.start()
                print(f"\n\nGoing back to main menu...")
                print("------------------------------------------------")
                print(f"{'1/ Change Team':<15} - Change your Pokemon team")
                print(f"{'2/ PvE':<15} - Battle or Catch a wild Pokemon")
                print(f"{'3/ PvP':<15} - Battle another trainer")
                print(f"{'4/ Quit':<15}")
                print(f"To create another trainer/player, please quit and re-run the game.")
                print("------------------------------------------------")
                choose_action(player, pokemon_data)
                        
            case 3:
                ennemy = input(f"What's the name of the trainer you want to battle with? ")
                while True:
                    isPlayer = player.search_trainer(ennemy)
                    if not isPlayer:
                        ennemy = input("This trainer does not exist. Please input another name. ")
                    else:
                        break
                    
                print(f"Trainer found!") 
                playbale_ennemy = Player(ennemy)               
                print(f"Initializing...")
                print(f"\n{player.name} team is: \n{player}")
                print(f"{playbale_ennemy.name} team is: \n{playbale_ennemy}")
                initial_p1_pkm = player.team[0]
                initial_p2_pkm = playbale_ennemy.team[0]
                print(f"Preparing...")
                pvp = PVP(initial_p1_pkm, initial_p2_pkm, player, playbale_ennemy)
                pvp.start()
                print(f"\n\nGoing back to main menu...")
                print("------------------------------------------------")
                print(f"{'1/ Change Team':<15} - Change your Pokemon team")
                print(f"{'2/ PvE':<15} - Battle or Catch a wild Pokemon")
                print(f"{'3/ PvP':<15} - Battle another trainer")
                print(f"{'4/ Quit':<15}")
                print(f"To create another trainer/player, please quit and re-run the game.")
                print("------------------------------------------------")
                choose_action(player, pokemon_data)
                        
            case 4:
                sys.exit("Thanks for playing. See you next time!")
          
if __name__ == '__main__':
    main()