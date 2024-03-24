import pyfiglet

from utils import save_data
from player import Player


def main():
    print(pyfiglet.figlet_format("Welcome to OOP-kemon", font = "slant", width = 250))
    pokemons = save_data("./data/pokemon.txt")
    
    menu_screen(pokemons)
    #print(*pokemons[:3])
    #test = Pokemon(pokemons[1])
    #print(test)
    

def menu_screen(pokemon_data: list[dict]):
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
    print(f"{'1/ Random':<10} - Change your Pokemon team")
    print(f"{'2/ PvE':<10} - Battle or Catch a wild Pokemon")
    print(f"{'3/ PvP(AI)':<10} - Battle another trainer")
    #print("4/ Create another trainer")
    
if __name__ == '__main__':
    main()