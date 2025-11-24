# Installation and Setup Guide

## Prerequisites

To run this Ren'Py game, you need:

1. **Ren'Py SDK** (version 7.4.0 or higher)
   - Download from: https://www.renpy.org/latest.html
   - Available for Windows, macOS, and Linux

## Installation Steps

### Option 1: Using Ren'Py Launcher (Recommended)

1. **Download Ren'Py SDK**
   ```
   Visit https://www.renpy.org/latest.html
   Download the version for your operating system
   Extract the archive to a location of your choice
   ```

2. **Get the Magi Game Files**
   ```bash
   git clone https://github.com/OddHonoR/Magi.git
   ```

3. **Add Project to Ren'Py**
   - Launch the Ren'Py SDK (run renpy.sh on Linux/Mac or renpy.exe on Windows)
   - Click "preferences" at the bottom right
   - Click "Projects Directory" and add the directory containing Magi
   - Or click "Add Existing Project" and navigate to the Magi folder

4. **Launch the Game**
   - Select "Magi" from the project list
   - Click "Launch Project"
   - The game should start!

### Option 2: Command Line

If you have Ren'Py SDK installed, you can run:

```bash
# Navigate to your Ren'Py SDK directory
cd /path/to/renpy-sdk

# Run the game
./renpy.sh /path/to/Magi
```

## Verifying Installation

The game should launch with a main menu showing:
- New Game
- Continue
- Options
- About
- Quit

Click "New Game" to start playing!

## Troubleshooting

### "No module named 'renpy'" error
- This is normal - Ren'Py files (.rpy) must be run through the Ren'Py SDK, not standard Python

### Missing images
- Make sure all files in the `game/` directory are present
- The `game/images/` and `game/gui/` directories should contain PNG files

### Game won't start
- Check that you're using Ren'Py 7.4.0 or higher
- Make sure the `game/` directory is at the root of the project
- Check the Ren'Py launcher's error log for details

## Game Controls

- **Left Click**: Advance dialogue, select options
- **Right Click / ESC**: Open game menu
- **Mouse Wheel**: Scroll through save/load screens
- **F**: Toggle fullscreen
- **S**: Take screenshot
- **H**: Hide text window

## Project Structure

```
Magi/
├── game/               # Game content directory
│   ├── script.rpy      # Main story script
│   ├── deck_builder.rpy # Deck building mechanics
│   ├── screens.rpy     # UI screens
│   ├── options.rpy     # Game settings
│   ├── images/         # Background images
│   │   ├── bg_black.png
│   │   ├── bg_forest.png
│   │   ├── bg_cave.png
│   │   ├── bg_boss_room.png
│   │   └── bg_victory.png
│   └── gui/           # GUI assets
│       ├── frame.png
│       ├── textbox.png
│       ├── namebox.png
│       └── ...
├── README.md          # Project documentation
└── INSTALL.md         # This file
```

## Development

To modify the game:

1. Edit the `.rpy` files in the `game/` directory
2. Ren'Py will automatically detect changes when you launch the game
3. Press Shift+R in-game to reload the script after making changes
4. Use Shift+D to open the developer console

## Additional Resources

- [Ren'Py Documentation](https://www.renpy.org/doc/html/)
- [Ren'Py Quickstart](https://www.renpy.org/doc/html/quickstart.html)
- [Ren'Py Tutorial](https://www.renpy.org/doc/html/tutorial.html)

## Support

For issues with Ren'Py itself, visit:
- [Ren'Py Forums](https://lemmasoft.renai.us/forums/)
- [Ren'Py Discord](https://discord.gg/6ckxWYm)

For issues with this specific game, please open an issue on GitHub.
