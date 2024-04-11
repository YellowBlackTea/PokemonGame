import pytest
from unittest.mock import patch, Mock

from project import change_team
from player import Player


@pytest.fixture
def mock_player():
    return Mock(spec=Player)

@patch('builtins.print')
def test_change_team(mock_print, mock_player):
    change_team(mock_player)
    mock_player.change_team.assert_called_once()
    mock_print.assert_called_once_with("\n\nGoing back to main menu...")
