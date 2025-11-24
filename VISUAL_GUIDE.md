# Visual Guide

This document describes the visual elements and UI of Magi: Deck Builder CYOA.

## Main Menu

When you start the game, you'll see:
- Title: "Magi: Deck Builder" in large text
- Menu options centered on screen:
  - New Game
  - Continue
  - Options
  - About
  - Quit
- Background: Purple gradient from dark blue to purple

## Story Screens

Story text appears with:
- Character name box (if applicable)
- Dialogue text box at the bottom
- Background images showing the current location
- Choice buttons when decisions are available

### Backgrounds

1. **Black Screen** - For introduction and transitions
2. **Forest** - Green gradient, outdoor atmosphere
3. **Cave** - Dark grey gradient, underground feeling
4. **Boss Room** - Red gradient, intense atmosphere
5. **Victory** - Golden gradient, triumphant feeling

## Combat UI

The combat screen displays:

### Top Section (Enemy Info)
- Enemy name centered at top
- HP bar: "HP: [current]/[max]"
- Block value (if any): "Block: [amount]"
- Intent display: "Intent: attack (X damage)"

### Left Section (Player Info)
- Player name
- HP: "HP: [current]/[max]"
- Block (if any): "Block: [amount]"
- Energy: "Energy: [current]/[max]"
- Pile counts: "Draw: X | Discard: Y"

### Bottom Section (Hand Display)
- 5 cards shown as frames
- Each card displays:
  - Card name (larger text)
  - Cost in energy
  - Card type (attack/defense/skill)
  - Power value (if applicable)
  - Description text
- Cards are clickable to play them
- Width: 150px per card, Height: 200px
- Spaced with 10px gaps

### Right Section (Controls)
- "End Turn" button in bottom-right corner

## Card Visual Layout

Each card frame contains (top to bottom):
```
┌──────────────┐
│  CARD NAME   │  (18pt, centered)
├──────────────┤
│ Cost: 1      │  (14pt)
│ attack       │  (14pt, card type)
│ Power: 6     │  (14pt, if applicable)
├──────────────┤
│ Description  │  (12pt)
│ text here    │
└──────────────┘
```

## Deck View Screen

Shows your entire deck:
- Title: "Your Deck" (40pt)
- Total card count
- Scrollable list of all cards
- Each card listed shows:
  - Name (20pt)
  - Type (16pt)
  - Cost (16pt)
  - Power (16pt)
- "Close" button at bottom

## Reward Screen

After winning a battle:
- Prompt: "Choose a card to add to your deck" (30pt)
- 3 cards displayed horizontally
- Larger card frames (200px x 280px)
- Each card shows full details
- "Skip" button option at bottom
- Choice is permanent

## Choice Screen

For CYOA decisions:
- Prompt text at top (24pt)
- List of choice buttons vertically centered
- Each button shows the choice text
- Buttons are 500px wide
- Choices affect story progression

## Color Scheme

### Primary Colors
- **Background Base**: Dark blue-purple (#1a1a2e)
- **Frame Background**: Semi-transparent dark (#24243e)
- **Text**: White (#ffffff)
- **Textbox**: Dark with transparency (#1a1a2ecc)

### UI Elements
- **Namebox**: Purple-blue (#302b63cc)
- **Buttons Idle**: Grey (#888888)
- **Buttons Hover**: White (#ffffff)
- **Buttons Selected**: Orange (#ffaa00)

### Card Type Colors (Conceptual)
- **Attack Cards**: Red theme
- **Defense Cards**: Blue theme
- **Skill Cards**: Green theme

## Font

All text uses **DejaVuSans** font:
- Default size: 22pt
- Titles: 30-50pt
- Card names: 18-22pt
- Card details: 12-16pt
- UI labels: 14-20pt

## Screen Resolutions

Default resolution: 1920x1080
- Supports window mode and fullscreen
- UI elements scale appropriately

## Interaction Feedback

### Hover States
- Buttons change color on hover (grey → white)
- Cards can have hover highlight (future enhancement)

### Click States
- Cards disappear from hand when played
- UI updates immediately after actions
- Damage/block numbers appear in text

## Combat Flow Visual Sequence

1. **Turn Start**
   - Hand fills with 5 cards
   - Energy resets to 3
   - Block resets to 0

2. **Card Play**
   - Click card
   - Card effect text appears
   - Enemy HP or player block updates
   - Card removed from hand

3. **End Turn**
   - Click "End Turn"
   - Enemy intent displayed in text
   - Enemy action occurs
   - HP updates

4. **Victory/Defeat**
   - Victory text or game over screen
   - Transition to next section or restart

## Accessibility

- Clear text contrast (white on dark)
- Large clickable areas for cards and buttons
- Text-based feedback for all actions
- Keyboard shortcuts available (ESC for menu, etc.)

## Future Visual Enhancements

Not yet implemented but could include:
- Animated card effects
- Particle effects for damage/block
- Card rarity indicators (common, uncommon, rare)
- Health bars instead of text
- Card art/illustrations
- More detailed backgrounds
- Character sprites
- Sound effects and music
- Animated transitions
- Glossy card effects
- Tooltip pop-ups on hover

## UI Flow Diagram

```
Main Menu
    ↓
Story Introduction
    ↓
Specialization Choice
    ↓
[Loop: Encounters]
    ↓
Combat Screen
    ↓
Victory → Card Reward
    ↓
Story Choice
    ↓
[Next Encounter]
    ↓
Final Boss Combat
    ↓
Victory Screen
    ↓
End / Main Menu
```

## Screenshot Equivalents

Since this is a text-based Ren'Py game without actual screenshots, here's what you'd see:

**Combat Example:**
```
╔════════════════════════════════════════════════════════════╗
║                     GOBLIN SCOUT                            ║
║                  HP: 24/30   Block: 0                       ║
║              Intent: attack (6 damage)                      ║
╠════════════════════════════════════════════════════════════╣
║                                                             ║
║  Hero            [FOREST BACKGROUND]                        ║
║  HP: 75/80                                                  ║
║  Block: 5                                                   ║
║  Energy: 2/3                                                ║
║  Draw: 3 | Discard: 2                                       ║
║                                                             ║
║                                             [END TURN]      ║
╠════════════════════════════════════════════════════════════╣
║  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐             ║
║  │ STRIKE │ │ DEFEND │ │ STRIKE │ │FIREBALL│             ║
║  │ Cost:1 │ │ Cost:1 │ │ Cost:1 │ │ Cost:2 │             ║
║  │ attack │ │defense │ │ attack │ │ attack │             ║
║  │Power:6 │ │Power:5 │ │Power:6 │ │Power:9 │             ║
║  └────────┘ └────────┘ └────────┘ └────────┘             ║
╚════════════════════════════════════════════════════════════╝
```

---

This visual guide helps understand the game's appearance without needing to run it!
