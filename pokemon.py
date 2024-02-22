import pyfiglet

def main():
    print(pyfiglet.figlet_format("Welcome to OOP-kemon", font = "slant", width = 250))
    menu_screen([1,2,3])


def menu_screen(deck):
    name = input("What's your name? ")
    
    # if player exists, show him his pokemon
    print(f"Hello {name}, your party has {len(deck)} Pokemon:")
    
    # Print each Pokemon + its specifities (atk, hp, etc)
    ...
    
    # Print Menu option
    print(f"{'1/ Random' : <10} - Change your Pokemon team")
    print(f"{'2/ PvE' : <10} - Battle or Catch a wild Pokemon")
    print(f"{'3/ PvP(AI)' : <10} - Battle another trainer")
    #print("4/ Create another trainer")
    
if __name__ == '__main__':
    main()