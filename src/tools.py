import os
import sys
from random import *
from sudoku import Sudoku
from typing import Callable
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.enums import *

def getAbsolutePath(folder: str, filename: str) -> None:
    """
    Return the absolute file of a file.

    Args:
        folder (str): the folder of the file.
        filename (str): the name of the file.

    Returns:
        str: The absolute path of the file.
    """
    return os.path.abspath(os.path.join(folder, filename))

def getButton(func: Callable[[], any], title: str, w: int, h: int) -> QPushButton:
    """
    Create a QPushButton object.

    Args:
        func[None] (any): Function that will be call when the button is pressed.
        title (str): Text display on the button.
        w (int): width of the button.
        h (int): height of the button.

    Returns:
        QPushButton: Button object.
    """
    button = QPushButton(title)
    button.setFixedSize(w, h)
    if func:
        button.clicked.connect(func)
    return button

def getSelfButton(func: Callable[[QPushButton], None], title: str, w: int, h: int) -> QPushButton:
    """
    Create a QPushButton object.

    Args:
        func[button] (any): Function that will be call when the button is pressed with itself in parameters.
        title (str): Text display on the button.
        w (int): width of the button.
        h (int): height of the button.

    Returns:
        QPushButton: Button object.
    """
    button = QPushButton(title)
    button.setFixedSize(w, h)
    if func:
        button.clicked.connect(lambda: func(button))
    return button

def getCleanedString(text: str) -> (str | None):
    """
    Removes string's duplicate and sorts it.

    Args:
        text (str): a string full of numbers

    Returns:
        str: A sort string without duplicates characters
    """
    try:
        int(text)
    except:
        return None

    unsorted_text = ""
    for c in text:
        if c not in unsorted_text:
            unsorted_text = unsorted_text + c
        else:
            unsorted_text = unsorted_text.replace(c, '')
    return ''.join(sorted(unsorted_text))

def create_grid(difficulty: DifficultyID) -> tuple[list[list[int | None]], list[list[int | None]]]:
    """
    Create a sudoku grid.

    Args:
        difficulty (float): an enum between 0 and 1 to choose the difficulty (0 easy, 1 hardcore)

    Returns:
        tuple[list[list[int | None]], list[list[int | None]]]: the grid and the solved grid
    """
    grid = Sudoku(3, seed=randint(0, sys.maxsize)).difficulty(difficulty.value)
    return grid.board, grid.solve().board

def getBlurEffect(blurRadius: float) -> QGraphicsBlurEffect:
    blur_effect = QGraphicsBlurEffect()
    blur_effect.setBlurRadius(blurRadius)
    return blur_effect

darkColors: dict[str, QColor] = {
    "item-foreground": QColor("white"),
    "item-background": QColor("black"),
    "item-background_selected": QColor(30, 30, 30),
    "item-premade": QColor(65,105,225),
    "item-made": QColor("yellow"),
    "item-false": QColor("red"),
    "item-comment": QColor(128, 128, 128),
    "item-big_border": QColor(220, 220, 220),
    "item-little_border": QColor(55, 65, 79)
}

whiteColors: dict[str, QColor] = {
    "item-foreground": QColor("black"),
    "item-background": QColor("white"),
    "item-background_selected": QColor(240, 240, 240),
    "item-premade": QColor(65, 105, 225),
    "item-made": QColor("yellow"),
    "item-false": QColor("red"),
    "item-comment": QColor(128, 128, 128),
    "item-big_border": QColor(150, 150, 150),
    "item-little_border": QColor(192, 196, 200)
}
