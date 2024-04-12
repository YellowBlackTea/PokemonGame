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
A Pokemon turn-based battle game implemented in Python using OOP. This game is exclusively interactive with the CLI. Two different modes can be played: a Player versus Player (PvP) and a Player versus Environnment (PvE).

- In the **PvP** mode, the first Player is the one who start the game, s/he then has the ability to search for a registered trainer name. Once found, the battle starts by taking turns. Each player has a team composed of 3 Pokemons, and the possibilities to change the Pokemon in a PC / box storage of a maximum of 6 Pokemons. Whoever wins the battle get XP.
- In the **PvE** mode, the Player battles against a wild Pokemon, and s/he has the possibility to catch it.

A trainer is automatically registered in a file when a game starts and the user input a name. A same name cannot be registered, so only the newest one will be saved.

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
    - [Root Directory](#root)
    - [Data Directory](#data)

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
The `Pokemon` class is essential to create a random (or not) Pokemon from a list of Pokemon initially in a dict. As the information read from `data/pokemon.txt` is in a `list[doc]` format, it was used as an initial input to the `Pokemon` class. A `str` method is defined to be able to output the `Pokemon` class as a `str` in the format expected by the instruction.

#### Player Class
The `Player` class creates a Player by its name. Each player is unique with an automatic randomized team associated.

#### Battle Class
The `Battle` class creates all actions used in a battle whether it is against another player or a wild Pokemon. Thus, `PVE` class and `PVP` class were created as inheritence of this parent class.

If the Pokemon chooses to defend itself, then a random number is chosen from the range of the regeneration ability.

If the Pokemon chooses to launch an Attack, then a random number is chosen between 0 and 100. And if that number is greater than the accuracy of the attack, the Pokemon can sucessfully launch the attack using the following formula to calculate the **damage taken**:

$damage\_taken = round(b * rand(0.85, 1) * \frac{power(4 *  target\_pokemon\_level + 2)}{target\_pokemon\_resistance} + 2)$

with b, the coefficient defined in the following table. 
|   | Air | Water | Fire | Earth |
|---|-----|-------|------|-------|
| **Air**   | 1   | 0.5   | 1    | 1.5   |
| **Water** | 1.5 | 1     | 1    | 0.5   |
| **Fire**  | 0.5 | 1.5   | 1    | 1     |
| **Earth** | 1   | 0.5   | 1.5  | 1     |


As soon as the wild Pokemon HP falls below 20%, then the Player has the possibility to **catch the Pokemon** using this catch_rate formula.

$catch\_rate = 4 * (0.2 - \frac{target\_current\_hp}{target\_max\_hp})$

The **XP gain formula** depends on the type of battle mode. Each time the XP exceeds 100 of the total XP, then the Pokemon levels up and each stats is randomly increased between 1 to 5 stats point. For all 3 Pokemon in a team, the amount of XP gained is as follow: 
- In PvP: 

$ pokemon\_won = 10 + avg\_lvl\_lost\_pokemons - pokemon\_won\_lvl$
- In PvE: 

$ pokemon = \frac{10 + lvl\_wild\_pokemon - pokemon\_lvl}{3}$

### Ability 
The `Ability` file is composed of two classes: `Attack` and `Defense` classes. Those classes are pretty straightforward as they define the extraction of information in an attack.txt and defense.txt files (both in the data directory).

### Data
The data directory contains 3 main files defining a Pokemon: an attack.txt file, a defense.txt file and a pokemon.txt file. As soon as an name is input, the trainer.txt file is created to register and save it.

## 📝 License

Copyright © 2024 [EstelleZheng](https://github.com/YellowBlackTea).<br />
This project is [MIT](https://github.com/YellowBlackTea/PokemonGame/blob/main/LICENSE) licensed.
