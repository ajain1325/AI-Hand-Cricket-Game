![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-green)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
# AI Hand Cricket

AI Hand Cricket is a webcam-based desktop game that uses hand-gesture recognition to let a player score runs against an adaptive computer opponent. The project combines OpenCV for camera access, MediaPipe for hand tracking, and a PyQt5 desktop UI for the live scoreboard, ball history, and leaderboard.

## Overview

The player shows a hand gesture in front of the webcam for each ball. The detected gesture is converted into a cricket run value from 0 to 6, and the AI produces its own number. If the player and AI choose the same non-zero value, the player is out. Otherwise, the player's detected value is added to the total score.

The current runtime path is the PyQt5 desktop application started from `main.py`. The repository also contains an older OpenCV-only gameplay flow in `controlled_ball_system.py` that is still useful for understanding the game logic and leaderboard behavior.

## Features

- Webcam-based hand detection using MediaPipe
- Gesture-to-score mapping for values 0 through 6
- Desktop UI built with PyQt5
- Ball-by-ball score tracking across a 6-ball innings
- Adaptive AI that learns from the player's recent run history
- Leaderboard persistence in `leaderboard.txt`
- Restart flow for starting a new match without relaunching the app
- Windows batch files for quick launch and leaderboard reset

## Tech Stack

- Python
- OpenCV
- MediaPipe
- PyQt5
- NumPy
- Matplotlib and pygame are listed in dependencies, though the main desktop gameplay path primarily relies on OpenCV, MediaPipe, and PyQt5

## How The Game Works

Each innings lasts up to 6 balls.

Gesture mapping:

- Closed fist = 0
- Thumb only = 6
- Otherwise, the total number of open fingers = 1 to 5

Match rules:

- The UI starts a 3-second countdown before each ball
- Show a valid gesture clearly inside the camera frame
- The AI generates a run value for the same ball
- If `player == AI` and the value is not `0`, the player is out and the innings ends
- If both sides show `0`, it is treated as a dot ball, not an out
- Otherwise, the player's run value is added to the score
- At the end of the innings, the score is appended to `leaderboard.txt`

## AI Behavior

The AI starts in a random mode and becomes partially adaptive as the match progresses.

- During the early game, it selects a random value from 0 to 6
- After enough player history is available, it tracks the player's most frequent run
- With a 60% chance, it plays the most common player value
- Otherwise, it adds randomness to avoid being fully predictable

This logic lives in the `ai_move()` method in `controlled_ball_system.py` and is used by the active UI flow as well.

## Project Structure

```text
AI-Hand-Cricket-Game/
|-- main.py
|-- controlled_ball_system.py
|-- hand_detector.py
|-- gesture_visualizer.py
|-- leaderboard.txt
|-- requirements.txt
|-- run_game.bat
|-- clear_leaderboard.bat
|-- assests/
|   `-- gestures/
`-- ui/
    |-- main_window.py
    |-- center_panel.py
    |-- ball_panel.py
    `-- leaderboard_panel.py
```

Key files:

- `main.py`: Application entry point, camera selection, and PyQt app startup
- `hand_detector.py`: MediaPipe-based hand landmark detection and finger counting
- `controlled_ball_system.py`: Core game logic, AI move selection, score saving, and legacy OpenCV match flow
- `gesture_visualizer.py`: Builds a simple gesture status overlay for heatmap-style visualization
- `ui/main_window.py`: Top-level desktop window that assembles the full UI
- `ui/center_panel.py`: Live camera preview, countdown, decision text, game loop, and restart behavior
- `ui/ball_panel.py`: Ball-by-ball snapshot display
- `ui/leaderboard_panel.py`: Leaderboard, scoreboard, and AI explanation panel
- `leaderboard.txt`: Persistent score storage in `name,score` format
- `run_game.bat`: Windows helper script to activate the virtual environment and run the app
- `clear_leaderboard.bat`: Windows helper script to erase saved scores after confirmation

## Requirements

- Windows is the primary target environment in the current codebase
- Python 3.10 or newer is recommended
- A working webcam

Install dependencies:

```powershell
pip install -r requirements.txt
pip install PyQt5
```

Note:

- `main.py` imports PyQt5, but PyQt5 is not currently listed in `requirements.txt`
- Camera initialization uses `cv2.CAP_DSHOW`, which is Windows-specific

## Running The Project

### Option 1: Run with Python

```powershell
python main.py
```

### Option 2: Use the batch file on Windows

```powershell
.\run_game.bat
```

The batch file expects a local virtual environment at `venv\Scripts\activate.bat`.

## Camera Selection

The app tries camera indexes in this order:

`1, 2, 0, 3, 4`

You can force a specific camera by setting the `CAMERA_INDEX` environment variable before launch.

Example:

```powershell
$env:CAMERA_INDEX=0
python main.py
```

## Leaderboard

Scores are stored in `leaderboard.txt` as comma-separated values:

```text
PlayerName,18
AnotherPlayer,24
```

Behavior:

- The UI shows the top scores in descending order
- Each finished match appends a new entry
- Names are not deduplicated, so the same player can appear multiple times
- Use `clear_leaderboard.bat` to reset the file safely on Windows

## UI Flow

When the app starts:

1. The player enters a name.
2. The main window opens with three panels.
3. A live webcam preview appears in the center panel.
4. Each ball runs on a timed cycle: countdown, detection, AI response, score update.
5. Captured ball images are shown in the left panel.
6. The live score and top leaderboard entries are shown on the right.
7. When the innings ends, the score is saved and the player can restart.

## Troubleshooting

### PyQt5 import error

If the app fails with a `ModuleNotFoundError` for PyQt5, install it manually:

```powershell
pip install PyQt5
```

### No camera detected

- Make sure no other app is locking the webcam
- Try forcing a camera index with `CAMERA_INDEX`
- Reconnect the webcam and relaunch the app

### Gesture not detected consistently

- Keep your hand fully inside the camera frame
- Use good front lighting
- Avoid cluttered backgrounds if tracking is unstable
- Show one clear hand only, since the detector is configured for a single hand

### Batch file does not work

`run_game.bat` assumes a local `venv` folder exists. If you do not have one, either create a virtual environment first or run `python main.py` directly.

## Development Notes

- The active gameplay loop is handled in `ui/center_panel.py`
- `controlled_ball_system.py` still contains reusable game logic and a legacy OpenCV-only match presentation path
- `assests/gestures/` currently exists but is empty in this workspace
- The repository contains image assets referenced by the UI stylesheets for backgrounds and panel decoration

## Possible Improvements

- Add PyQt5 to `requirements.txt`
- Add screenshots or a short demo GIF to this README
- Normalize leaderboard player names to avoid duplicate variants
- Move hard-coded asset paths into a dedicated resource system
- Add cross-platform camera backend handling

## License

No license file is currently present in this repository.
