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
    # Print Menu option
    choose_action(player, pokemon_data)

def change_team(player: Player) -> None:
    """"Case 1: Change current team before battling.
    
    Args:
        player (Player): Name or player class of the first player.
    """
    player.change_team()
    print(f"\n\nGoing back to main menu...")

def pve_battle(player: Player, pokemon_data: list[dict]) -> None:
    """Case 2: Choose PvE battle with possibility to catch the Pokemon.

    Args:
        player (Player): Name or player class of the first player.
        pokemon_data (list[dict]): list of all Pokemon data read from ./data/pokemon.txt.
    """
    wild_pkm = Pokemon(random.choice(pokemon_data))
    initial_pkm = player.team[0]
    pve = PVE(initial_pkm, wild_pkm, player)
    pve.start()
    print("\n\nGoing back to main menu...")

def pvp_battle(player: Player) -> None:
    """Case 3: Choose PvP battle, battle against another player on the same screen.

    Args:
        player (Player): Name or player class of the first player.
    """
    ennemy = input("What's the name of the trainer you want to battle with? ")
    while True:
        isPlayer = player.search_trainer(ennemy)
        if not isPlayer:
            ennemy = input("This trainer does not exist. Please input another name. ")
        else:
            break
    print("Trainer found!") 
    playable_enemy = Player(ennemy)               
    print("Initializing...")
    print(f"\n{player.name} team is: \n{player}")
    print(f"{playable_enemy.name} team is: \n{playable_enemy}")
    
    if not player.team or not playable_enemy.team:
        raise ValueError("Please re-run the game. Trainer file was modified.")

    initial_p1_pkm = player.team[0]
    initial_p2_pkm = playable_enemy.team[0]
    print("Preparing...")
    pvp = PVP(initial_p1_pkm, initial_p2_pkm, player, playable_enemy)
    pvp.start()
    print("\n\nGoing back to main menu...")

def quit_game(player: Player):
    """Case 4: Choose to quit game with an auto-save just before.
    
    Args:
        player (Player): Name or player class of the first player.
    """
    player.save_info()
    sys.exit("Your progress was sucessfully saved.\nThanks for playing. See you next time!")

def choose_action(player: Player, pokemon_data: list[dict]) -> None:
    """Choose an action from the different options in the menu screen.

    Args:
        player (Player): Name or player class of the first player.
        pokemon_data (list[dict]): list of all Pokemon data read from ./data/pokemon.txt.
    """
    print("------------------------------------------------")
    print(f"{'1/ Change Team':<15} - Change your Pokemon team")
    print(f"{'2/ PvE':<15} - Battle or Catch a wild Pokemon")
    print(f"{'3/ PvP':<15} - Battle another trainer")
    print(f"{'4/ Quit':<15}")
    print(f"To create another trainer/player, please quit and re-run the game.")
    print("------------------------------------------------")
                
    action = get_int("Choose an action. ")
    play = True
    while play:
        match action:
            case 1:
                change_team(player)
                
                choose_action(player, pokemon_data)
                
            case 2:
                pve_battle(player, pokemon_data)
                
                choose_action(player, pokemon_data)
                        
            case 3:
                pvp_battle(player)
                
                choose_action(player, pokemon_data)
                        
            case 4:
                quit_game(player)
          
if __name__ == '__main__':
    main()