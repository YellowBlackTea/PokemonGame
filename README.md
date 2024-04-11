<h1 align="center">Welcome to OOP-kemon Game</h1>
<p>
  <a href="https://github.com/YellowBlackTea/PokemonGame" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://github.com/YellowBlackTea/PokemonGame/blob/main/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

> An interactive terminal / CLI Pokemon turn-based battle system.

### ✨ [Demo](https://github.com/YellowBlackTea/PokemonGame)

## Description
A Pokemon turn-based battle game implemented in Python using OOP. This game is exclusively interactive with the CLI. 

### Background
This project is part of Havard/edX CS50P Final Project. The instruction and the formula for computing the catch rate or the effectiveness of an attack was greatly inspired by Sorbonne Université MU4RBI01 course.

### Future Features
Not in any soon, but it would be great to have a GUI instead of using the CLI.

## Table of Content
[Demo](#✨-demo)
1. [Description](#description)
    - [Backgtound](#background)
    - [Future Features](#future-features)
2. [Table of Content](#table-of-content)
3. [Install](#install)
4. [Usage](#usage)
5. [Run tests](#run-tests)
6. [Code Overview](#code-overview)

## Install
The easiest way to install the game is to clone this repository:
```sh
git clone https://github.com/YellowBlackTea/PokemonGame
pip install requirements.txt
```
For any update:
```sh
git pull
```

## Usage
The main program is in the `project.py`file. Run this file to start the game.
```sh
python project.py
```

## Run tests
Tests functions are in the `test/` directory. 

All tests should run without failing. However, since the whole program depends on the user input, some liberties were taken to run sucessfully each test.
```sh
pytest test/
```

## Code Overview
This project contains **3 main parts**:
- The `root` or current directory, containing all important files to make the game works.
- The `data/` directory where all data regarding a Pokemon is stored. The `trainer.txt`created when running for the first time the game will also be stored here.
- The `test/` directory, as explaining in the [test section](#run-tests), it contains the test file of different functions.

### Root
In the `root` directory, the `main` function is in the `project.py` file. This file calls multiple classes which are defined here.

#### Pokemon Class
The `Pokemon` class: essential to create a random (or not) Pokemon from a list of Pokemon initially in a dict. As the information read from `data/pokemon.txt` is in a `list[doc]` format, it was used as an initial input to the `Pokemon` class. A `str` method is defined to be able to output the `Pokemon` class as a `str` in the format expected by the instruction.

2 methods:
- `generate_random_stats()`: Generate random stats to define a Pokemon.
- `from_string()`: Transform a string to a Pokemon class.

#### Player Class
The 


### Data

## Author

👤 **EstelleZheng**

* Github: [@YellowBlackTea](https://github.com/YellowBlackTea)

## 📝 License

Copyright © 2024 [EstelleZheng](https://github.com/YellowBlackTea).<br />
This project is [MIT](https://github.com/YellowBlackTea/PokemonGame/blob/main/LICENSE) licensed.
