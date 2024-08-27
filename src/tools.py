import os
from typing import Callable, Tuple
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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

def getButton(func: Callable[[], any], title: str = None, min_size: Tuple[int, int] = None, max_size: Tuple[int, int] = None) -> QPushButton:
    """
    Create a QPushButton object.

    Args:
        func[None] (any): Function that will be call when the button is pressed.
        title (str): Text display on the button.
        min_size (Tuple[int, int]): Min (x, y) / (width, height) for the button.
        max_size (Tuple[int, int]): Max (x, y) / (width, height) for the button.

    Returns:
        QPushButton: Button object.
    """
    button = QPushButton(title)
    if min_size:
        button.setMinimumSize(min_size[0], min_size[1])
    if max_size:
        button.setMaximumSize(max_size[0], max_size[1])
    if func:
        button.clicked.connect(func)
    return button

def getSelfButton(func: Callable[[QPushButton], None], title: str = None, min_size: Tuple[int, int] = None, max_size: Tuple[int, int] = None) -> QPushButton:
    """
    Create a QPushButton object.

    Args:
        func[button] (any): Function that will be call when the button is pressed with itself in parameters.
        title (str): Text display on the button.
        min_size (Tuple[int, int]): Min (x, y) / (width, height) for the button.
        max_size (Tuple[int, int]): Max (x, y) / (width, height) for the button.

    Returns:
        QPushButton: Button object.
    """
    button = QPushButton(title)
    if min_size:
        button.setMinimumSize(min_size[0], min_size[1])
    if max_size:
        button.setMaximumSize(max_size[0], max_size[1])
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

def getBlurEffect() -> QGraphicsBlurEffect:
    blur_effect = QGraphicsBlurEffect()
    blur_effect.setBlurRadius(5)
    return blur_effect
