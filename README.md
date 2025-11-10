# 3D Rubik's Cube Solver

A from-scratch revamp of the original project featuring a real-time, rotatable 3D cube, live editing tools, scrambles, and a Kociemba-based solver queue. Everything now runs inside a single pygame window so you can inspect, edit, and solve without juggling dialogs.

## Features
- **3D viewer** – drag to orbit the cube, with subtle shading to keep orientation obvious.
- **Edit mode** – pick any sticker, recolor it with the palette, or recreate a physical scramble by hand.
- **Keyboard moves** – press `R/L/U/D/F/B`, hold **Shift** for inverses and **Ctrl** for double turns.
- **Scramble + reset** – generate random scrambles or snap back to a solved cube instantly.
- **Solution queue** – call the Kociemba solver, preview every move, and step through them with a button or the `N` key.
- **Clean control panel** – concise sidebar with color swatches, essential buttons, and shortcut hints right beside the cube.

## Requirements
- Python 3.9+
- [pygame](https://www.pygame.org/) for rendering
- [kociemba](https://pypi.org/project/kociemba/) for optimal solutions (optional but recommended)

Install the dependencies with:

```bash
pip3 install pygame kociemba
```

> If `kociemba` is missing the UI will still run, but the "Solve" button will report that the solver backend is unavailable.

## Running the app

```bash
python3 main.py
```

The window opens with the cube in rotation mode. Drag with the left mouse button to orbit the view.

## Controls & Shortcuts

| Action | How |
| --- | --- |
| Toggle edit mode | `E` key or the panel button |
| Scramble cube | `S` key or the "Scramble" button |
| Reset cube | `Backspace` key or the "Reset" button |
| Solve cube | `Space` key or the "Solve" button |
| Apply next solution move | `N` key or the "Apply Next Move" button |
| Manual turns | `R/L/U/D/F/B` (hold **Shift** for `X'`, **Ctrl** for `X2`) |
| Paint stickers | Enter edit mode, select a color swatch, then click stickers |

## Tips
- The solution preview panel shows the queued moves in chunks of six; apply them one-by-one with `N` so you can follow along on a physical cube.
- Hover a sticker while editing to see its face/row/column plus the current color.
- Holding the mouse while editing lets you "paint" multiple stickers quickly.
- Center stickers stay locked to keep the cube mechanically valid; if you need to restore them, use the **Reset** button.

## License
This project is distributed for learning purposes; customize and extend it as you like!
