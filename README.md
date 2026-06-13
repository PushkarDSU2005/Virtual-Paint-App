# Virtual Paint App

Virtual Paint App is an interactive Python application that utilizes your webcam to let you draw on the screen using hand gestures. Powered by **OpenCV** for video processing and **MediaPipe** for real-time hand tracking, this app translates your finger movements into drawing actions on a virtual canvas.

This repository contains:
- `pro.py`: The main Virtual Paint application.
- `song.py`: An additional Python script included in the project.

## Features & Controls

Hold your hand up to your webcam and use the following gestures:
- **Draw:** Raise only your index finger.
- **Erase:** Pinch your thumb and index finger together.
- **Change Color:** Raise both your index and middle fingers. 
- **Clear Canvas:** Open your entire hand (all five fingers).
- **Save Image:** Press the `s` key.
- **Quit:** Press the `q` or `Esc` key (ensure the app window is focused).

## Setup & Running the Project

Follow these steps to run the application on Windows using PowerShell:

**1. Activate the virtual environment:**
```powershell
.\mp_env\Scripts\Activate.ps1
```
*(You should see `(mp_env)` appear at the beginning of your prompt after running this)*

**2. Install dependencies:**
```powershell
python -m pip install -r requirements.txt
```

**3. Run the Virtual Paint application:**
```powershell
python pro.py
```
