import pytest
from unittest.mock import patch, MagicMock

from main import pvp_battle
from player import Player
from pokemon import Pokemon

@pytest.fixture
def mock_player():
    player = Player("Ash")  # Assuming Player class has a constructor that accepts a name
    player.search_trainer = MagicMock(return_value=True)
    player.team = [Pokemon({'Name': 'Pikachu', 'Before': '', 'After': 'Raichu', 'Element': 'Air','Level': '5', 
            'HP': '150', 'Energy': '65', 'Regeneration': '9','Resistance': '45', 
            'Skills': str('[Thunderbolt, Thunder, Thunder Shock]')})
            ]  # Assuming the player has a team attribute
    return player

def test_pvp_battle_found_trainer(monkeypatch, capsys, mock_player, mocker):
    with patch('builtins.input', side_effect=["A"]):
        with pytest.raises((RuntimeError, StopIteration)) as pytest_wrapped_e:
            pvp_battle(mock_player)
            captured = capsys.readouterr()
            assert "Trainer found!" in captured.out
            assert "Initializing..." in captured.out
            assert "Ash team is:" in captured.out
            assert "A team is:" in captured.out
            assert "Preparing..." in captured.out
            assert "Going back to main menu..." in captured.out
        assert str(pytest_wrapped_e.value) == RuntimeError or StopIteration 
        # Special case only in case the trainer was sucessfully found and a battle did start

def test_pvp_battle_empty_team(monkeypatch, mock_player):
    mock_player.team = []  # Simulate empty team
    with patch('builtins.input', side_effect=["Gary"]):
        with pytest.raises(ValueError) as pytest_wrapped_e:
            pvp_battle(mock_player)
        assert str(pytest_wrapped_e.value) == "Please re-run the game. Trainer file was modified."  # Check error message

