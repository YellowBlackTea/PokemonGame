import pyfiglet

def main():
    print(pyfiglet.figlet_format("Welcome to OOP-kemon", font = "slant", width = 250))


def menu_screen(deck):
    name = input("What's your name? ")
    
    # if player exists, show him his pokemon
    
    print(f"Hello {name}, your party has {len(deck)} Pokemon:")
    
    # Print each Pokemon + its specifities (atk, hp, etc)
    ...
    
    # Print Menu option
    print("1/ Change your party Pokemon")
    print("2/ Battle or Catch a wild Pokemon")
    print("3/ Battle another trainer")
    print("")
if __name__ == '__main__':
    main()