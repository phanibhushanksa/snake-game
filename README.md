# Snake Game

A classic Snake game built in Python using Pygame with modern UI and smooth controls.

## Features

- 🐍 Classic Snake gameplay
- 🎮 Smooth arrow key controls
- 🎯 Score tracking
- ⏸️ Pause functionality
- 🔄 Restart capability
- 🎨 Modern visual design with gradient effects
- 📱 Responsive game window (640x480)

## Installation

1. Make sure you have Python 3.6+ installed on your system
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install pygame directly:

```bash
pip install pygame
```

## How to Play

Run the game:

```bash
python snake_game.py
```

### Controls

- **Arrow Keys**: Move the snake
- **Space**: Pause/Unpause the game
- **R**: Restart the game (when game over)
- **ESC**: Quit the game

### Game Rules

1. Control the snake to eat the red food
2. Each food eaten increases your score by 1
3. The snake grows longer with each food eaten
4. Avoid hitting the walls or your own tail
5. Try to get the highest score possible!

## Game Features

- **Visual Design**: The snake has a gradient blue body with a green head
- **Food System**: Red food appears randomly on the screen
- **Collision Detection**: Game ends when snake hits walls or itself
- **Score Display**: Current score shown in top-left corner
- **Instructions**: On-screen help for controls
- **Pause System**: Can pause at any time during gameplay
- **Restart**: Easy restart when game over

## Technical Details

- Built with Python 3.6+
- Uses Pygame for graphics and input handling
- Object-oriented design with clean code structure
- Efficient collision detection
- Smooth 10 FPS gameplay

## File Structure

```
├── snake_game.py      # Main game file
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

Enjoy playing! 🎮 