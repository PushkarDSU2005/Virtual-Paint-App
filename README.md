# Python Gesture Projects

This repository contains:

- `pro.py`: Virtual Paint app using OpenCV + MediaPipe hand tracking.
- `song.py`: Additional Python script.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run Virtual Paint

```bash
python pro.py
```

Controls:

- Index finger: draw
- Pinch (thumb + index): erase
- Index + middle: change color
- Five fingers: clear canvas
- `s`: save image
- `q` or `Esc`: quit (with app window focused)
