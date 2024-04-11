import pytest
from unittest.mock import patch

from main import pve_battle
from player import Player
from pokemon import Pokemon
from pve import PVE

@pytest.fixture
def mock_player():
    player = Player("Ash")  # Assuming Player class has a constructor that accepts a name
    player.team = [Pokemon({'Name': 'Pikachu', 'Before': '', 'After': 'Raichu', 'Element': 'Air','Level': '5', 
            'HP': '150', 'Energy': '65', 'Regeneration': '9','Resistance': '45', 
            'Skills': str('[Thunderbolt, Thunder, Thunder Shock]')})
            ]  # Assuming the player has a team attribute
    return player

@pytest.fixture
def mock_pokemon_data():
    return [{'Name': 'Wartortle', 'Before': 'Squirtle', 'After': 'Blastoise','Element': 'Water','Level': '7', 
            'HP': '185', 'Energy': '85', 'Regeneration': '11','Resistance': '75', 
            'Skills': str('[Bubble Beam, Bubble, Surf, Waterfall]')}
            ]

def test_pve_battle(mock_player, mock_pokemon_data, capsys):
    # Special case because I need user input for each action
    with pytest.raises(OSError):
        # Call the pve_battle function with the mock player and Pokemon data
        pve_battle(mock_player, mock_pokemon_data)
        
        # Assert that the battle was initiated correctly
        captured = capsys.readouterr()
        assert "Battle begins!" in captured.out
        assert "Going back to main menu..." in captured.out