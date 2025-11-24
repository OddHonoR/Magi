# Magi: Pilgrimage Journey Game

A card-driven pilgrimage journey game inspired by Oregon Trail, made with Ren'Py.

## Overview

Magi is a survival journey game where you play as a pilgrim traveling to the holy living city of Magi that wanders the world's rim. Navigate treacherous provinces, manage your resources, make difficult choices, and keep pace with the wandering city. The journey is harsh, and only the faithful, prepared, and resilient will reach their destination.

## Game Modes

### Pilgrimage Journey (NEW)
The main game mode - an Oregon Trail-inspired card-driven journey where you:
- Choose province, season, background, blessing, and starting deck
- Travel node by node through procedurally generated routes
- Manage Sustenance, Health, Spirit, Packweight, and Progress
- Draw cards based on your Spirit stat (low Spirit = fewer options)
- Face encounters from hermits to corrupted pilgrims
- Accumulate corruption or maintain faith
- Race against time to reach the Magi before resources run out

### Combat Deck Builder (Classic)
The original combat-focused mode where you battle enemies in turn-based card combat.

## Pilgrimage Journey Features

- **Five Distinct Provinces**: Salt Plains, Fallen Forests, Clay Wastes, High Pilgrim Road, Storm Frontier
- **Four Seasons**: Each modifying travel speed and hazards differently
- **Four Backgrounds**: Merchant, Warrior, Priest, Scholar - each with unique starting stats
- **Multiple Blessings**: Choose divine protection to aid your journey
- **Three Card Types**:
  - **Action Cards**: Hunt, Navigate, Bargain, Pray, Rest - tools for survival
  - **Condition Cards**: Injuries, curses, fatigue - clog your deck and slow you down
  - **Relic Cards**: Powerful permanent effects, but take up pack weight
- **Six Node Types**: Camp, Crossroads, Shrine, Settlement, Wilderness, Ruins
- **Multiple Endings**: Blessed, Turned Away, Consumed, or become part of the Outer Wall
- **Dynamic Hand Size**: Your Spirit stat determines how many cards you can draw
- **Daily Resource Drain**: Sustenance depletes daily, affecting health and spirit
- **Meaningful Choices**: Every decision leaves a mark on your pilgrimage

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

### Pilgrimage Journey Gameplay

**Core Stats:**
- **Sustenance**: Food and water (drains daily, affected by season)
- **Health**: Physical wellbeing (damaged by encounters, low sustenance)
- **Spirit**: Faith and resolve (determines hand size, lost through hardship)
- **Packweight**: Carrying capacity (relics add weight, excess causes fatigue)
- **Progress**: Distance to Magi (goal: 1000 leagues)

**Journey Flow:**
1. Choose province, season, background, blessing, and starting deck
2. Travel node by node (Camp, Crossroads, Shrine, Settlement, Wilderness, Ruins)
3. Draw hand each node based on Spirit (high Spirit = more cards)
4. Face encounters and make choices using your cards
5. Manage daily resource drain
6. Accumulate or resist corruption
7. Race to reach Magi before dying

**Deck Mechanics:**
- Action cards help you survive (hunt, navigate, bargain, pray)
- Condition cards clog your deck (injuries, curses, fatigue)
- Relics provide powerful effects but take pack space
- Low Spirit means fewer cards each turn - fewer options

**Endings:**
- **Blessed**: High Spirit, low corruption - welcomed into Magi
- **Turned Away**: Spirit too low - sent away to try again
- **Consumed**: Corruption too high - lost to darkness
- **Outer Wall**: Mixed journey - become part of the city's defenses

### Classic Combat Gameplay

- **Energy**: Used to play cards. Resets each turn.
- **Block**: Reduces damage taken. Resets at the start of your turn.
- **Hand**: You draw 5 cards each turn
- Click on cards to play them, end turn to let enemy act

## Game Structure

```
game/
├── script.rpy             # Main menu and game mode selection
├── journey.rpy            # Pilgrimage journey gameplay flow
├── journey_screens.rpy    # UI screens for journey mode
├── deck_builder.rpy       # Core game mechanics (both modes)
├── screens.rpy            # UI screens for combat mode
├── options.rpy            # Game configuration
├── images/               # Background images (provinces, locations)
└── gui/                  # GUI assets
```

## Development

The game is built using Ren'Py's visual novel engine with custom Python classes:

**Pilgrimage Journey Classes:**
- `JourneyCard`: Action/Condition/Relic cards for survival
- `JourneyDeck`: Manages journey cards with permanent relics
- `Pilgrim`: Player with Sustenance, Health, Spirit, Progress stats
- `Province`: Regions with terrain difficulty and travel speed
- `Node`: Stops along the journey (camp, shrine, wilderness, etc.)

**Combat Mode Classes:**
- `Card`: Combat cards with energy costs and effects
- `Deck`: Traditional deck building mechanics
- `Player`: Player with HP, energy, and block
- `Enemy`: Enemy characters with AI behavior

## License

This project is open source and available for educational purposes.

## Credits

Created as a basic deck builder CYOA demonstration in Ren'Py.