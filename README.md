# Magi: Deck Builder CYOA

A deck builder Choose Your Own Adventure game made with Ren'Py.

## Overview

Magi is a deck building game where you play as a young mage building your deck of spells and abilities while making choices that affect your journey. Battle enemies, collect powerful cards, and overcome challenges to defeat the Dark Sorcerer!

## Features

- **Deck Building Mechanics**: Build and customize your deck with various cards
- **Turn-Based Combat**: Strategic card-based combat system with energy management
- **CYOA Story**: Make meaningful choices that affect your journey
- **Card Types**: 
  - Attack cards (deal damage to enemies)
  - Defense cards (gain block to prevent damage)
  - Skill cards (special effects and abilities)
- **Progressive Difficulty**: Face increasingly challenging enemies
- **Reward System**: Gain new cards after victories

## How to Play

### Requirements
- Ren'Py SDK (version 7.4.0 or higher recommended)
- Python 3.x (included with Ren'Py)

### Running the Game

1. Download and install the [Ren'Py SDK](https://www.renpy.org/latest.html)
2. Clone this repository or download the source code
3. Launch the Ren'Py launcher
4. Click "Add Existing Project" and select the Magi directory
5. Select the project and click "Launch Project"

### Gameplay Basics

- **Energy**: Used to play cards. Resets each turn.
- **Block**: Reduces damage taken. Resets at the start of your turn.
- **Hand**: You draw 5 cards each turn
- **Deck Cycling**: When your draw pile is empty, your discard pile is shuffled back in

### Combat Controls

- Click on cards in your hand to play them
- Click "End Turn" when you're ready to let the enemy act
- Watch the enemy's intent to plan your strategy

## Game Structure

```
game/
├── script.rpy          # Main story and game flow
├── deck_builder.rpy    # Core deck building mechanics
├── screens.rpy         # UI screens and layouts
├── options.rpy         # Game configuration
├── images/            # Background images
└── gui/               # GUI assets
```

## Development

The game is built using Ren'Py's visual novel engine with custom Python classes for the deck building mechanics:

- `Card`: Represents individual cards with properties and effects
- `Deck`: Manages card collections (draw pile, hand, discard pile)
- `Player`: Player character with HP, energy, and deck management
- `Enemy`: Enemy characters with AI behavior

## License

This project is open source and available for educational purposes.

## Credits

Created as a basic deck builder CYOA demonstration in Ren'Py.