import os
from typing import Callable, Tuple
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def getAbsolutePath(folder: str, filename: str) -> None:
    return os.path.abspath(os.path.join(folder, filename))

def getButton(func: Callable[[], None], title: str = None, min_size: Tuple[int, int] = None, max_size: Tuple[int, int] = None) -> QPushButton:
    button = QPushButton(title)
    if min_size:
        button.setMinimumSize(min_size[0], min_size[1])
    if max_size:
        button.setMaximumSize(max_size[0], max_size[1])
    if func:
        button.clicked.connect(func)
    return button

def getSelfButton(func: Callable[[QPushButton], None], title: str = None, min_size: Tuple[int, int] = None, max_size: Tuple[int, int] = None) -> QPushButton:
    button = QPushButton(title)
    if min_size:
        button.setMinimumSize(min_size[0], min_size[1])
    if max_size:
        button.setMaximumSize(max_size[0], max_size[1])
    if func:
        button.clicked.connect(lambda: func(button))
    return button
