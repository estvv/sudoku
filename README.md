# Sudoku

## ⚙️ Installation

- **Clone the Repository:**

```bash
git clone https://github.com/yourusername/sudoku.git
cd sudoku
```


## ⚠️ Requirements

- ### Linux

  Make sure you have installed python

  ```bash
  python --version
  ```

  If you don't have python installed :

- Ubuntu

  ```bash
  sudo apt-get update && sudo apt-get install python3.6
  ```

- Fedora

  ```bash
  sudo dnf install python3
  ```

- ### Windows

  ```bash
  python --version
  ```

  If python is not installed, you can download it on the [official python website](https://www.python.org/downloads/windows/).


Whatever OS you use, you will need to install these packages

```bash
pip install -r requirements.txt
```

## 🐍 USAGE

```bash
python main.py
```

## 👾 Executables

- ### Linux

```bash
./build.sh
cd release/linux
./sudoku
```

- ### Windows

```bash
./build.bat
cd release/windows
./sudoku
```

## 💻 Features

- Play sudoku
- Choose the difficulty of the grid (🟢 Easy / 🟡 Medium / 🔴 Hard / ⚫ Impossible)
- Have a 💡 hint on a box if the player is stuck
- Choose your theme (🌑 Dark, 🌕 Light)

## ⚖️ License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the [MIT] License - see the LICENSE.md file for details

Each assets are made by me.
