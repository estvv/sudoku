from enum import Enum

class MenuID(Enum):
    close    = 0
    home     = 1
    settings = 2
    play     = 3

class ThemeID(Enum):
    dark  = 0
    light = 1

class DifficultyID(Enum):
    easy       = 0.5
    medium     = 0.6
    hard       = 0.7
    impossible = 0.8
