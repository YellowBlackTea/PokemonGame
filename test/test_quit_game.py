import sys

import pytest
from unittest.mock import patch, Mock

from main import quit_game
from player import Player


@pytest.fixture
def mock_player():
    return Mock(spec=Player)

@patch('sys.exit')
def test_quit_game(mock_sys_exit, mock_player):
    quit_game(mock_player)
    mock_player.save_info.assert_called_once()
    mock_sys_exit.assert_called_once_with("Your progress was sucessfully saved.\nThanks for playing. See you next time!")

