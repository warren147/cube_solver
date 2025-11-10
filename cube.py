"""Rubik's cube state container and move logic."""
from __future__ import annotations

import random
from typing import Dict, List, Tuple

ColorGrid = List[List[str]]

FACE_TO_COLOR = {
    "white": "w",  # Up
    "red": "r",    # Right
    "green": "g",  # Front
    "yellow": "y", # Down
    "orange": "o", # Left
    "blue": "b",   # Back
}

COLOR_LABELS = {
    "w": "white",
    "r": "red",
    "g": "green",
    "y": "yellow",
    "o": "orange",
    "b": "blue",
}

FACE_ALIAS = {
    "U": "white",
    "R": "red",
    "F": "green",
    "D": "yellow",
    "L": "orange",
    "B": "blue",
}

MOVES = ("R", "L", "U", "D", "F", "B")


def _new_face(color: str) -> ColorGrid:
    return [[color for _ in range(3)] for _ in range(3)]


def _rotate_face_clockwise(face: ColorGrid) -> ColorGrid:
    return [list(row) for row in zip(*face[::-1])]


class CubeState:
    def __init__(self) -> None:
        self.faces: Dict[str, ColorGrid] = {}
        self.reset()

    @classmethod
    def solved(cls) -> "CubeState":
        return cls()

    def reset(self) -> None:
        for name, color in FACE_TO_COLOR.items():
            self.faces[name] = _new_face(color)

    # --- Move helpers -------------------------------------------------
    def _rotate_right(self) -> None:
        self.faces["red"] = _rotate_face_clockwise(self.faces["red"])

        temp_green = [self.faces["green"][0][2], self.faces["green"][1][2], self.faces["green"][2][2]]
        temp_white = [self.faces["white"][0][2], self.faces["white"][1][2], self.faces["white"][2][2]]
        temp_blue = [self.faces["blue"][2][0], self.faces["blue"][1][0], self.faces["blue"][0][0]]
        temp_yellow = [self.faces["yellow"][0][2], self.faces["yellow"][1][2], self.faces["yellow"][2][2]]

        temp_white, temp_blue, temp_yellow, temp_green = temp_green, temp_white, temp_blue, temp_yellow

        self.faces["green"][0][2], self.faces["green"][1][2], self.faces["green"][2][2] = temp_green
        self.faces["white"][0][2], self.faces["white"][1][2], self.faces["white"][2][2] = temp_white
        self.faces["blue"][2][0], self.faces["blue"][1][0], self.faces["blue"][0][0] = temp_blue
        self.faces["yellow"][0][2], self.faces["yellow"][1][2], self.faces["yellow"][2][2] = temp_yellow

    def _rotate_left(self) -> None:
        self.faces["orange"] = _rotate_face_clockwise(self.faces["orange"])

        temp_green = [self.faces["green"][0][0], self.faces["green"][1][0], self.faces["green"][2][0]]
        temp_white = [self.faces["white"][0][0], self.faces["white"][1][0], self.faces["white"][2][0]]
        temp_blue = [self.faces["blue"][2][2], self.faces["blue"][1][2], self.faces["blue"][0][2]]
        temp_yellow = [self.faces["yellow"][0][0], self.faces["yellow"][1][0], self.faces["yellow"][2][0]]

        temp_white, temp_blue, temp_yellow, temp_green = temp_blue, temp_yellow, temp_green, temp_white

        self.faces["green"][0][0], self.faces["green"][1][0], self.faces["green"][2][0] = temp_green
        self.faces["white"][0][0], self.faces["white"][1][0], self.faces["white"][2][0] = temp_white
        self.faces["blue"][2][2], self.faces["blue"][1][2], self.faces["blue"][0][2] = temp_blue
        self.faces["yellow"][0][0], self.faces["yellow"][1][0], self.faces["yellow"][2][0] = temp_yellow

    def _rotate_up(self) -> None:
        self.faces["white"] = _rotate_face_clockwise(self.faces["white"])

        temp_green = list(self.faces["green"][0])
        temp_orange = list(self.faces["orange"][0])
        temp_blue = list(self.faces["blue"][0])
        temp_red = list(self.faces["red"][0])

        temp_green, temp_orange, temp_blue, temp_red = temp_red, temp_green, temp_orange, temp_blue

        self.faces["green"][0] = temp_green
        self.faces["orange"][0] = temp_orange
        self.faces["blue"][0] = temp_blue
        self.faces["red"][0] = temp_red

    def _rotate_down(self) -> None:
        self.faces["yellow"] = _rotate_face_clockwise(self.faces["yellow"])

        temp_green = list(self.faces["green"][2])
        temp_orange = list(self.faces["orange"][2])
        temp_blue = list(self.faces["blue"][2])
        temp_red = list(self.faces["red"][2])

        temp_green, temp_orange, temp_blue, temp_red = temp_orange, temp_blue, temp_red, temp_green

        self.faces["green"][2] = temp_green
        self.faces["orange"][2] = temp_orange
        self.faces["blue"][2] = temp_blue
        self.faces["red"][2] = temp_red

    def _rotate_front(self) -> None:
        self.faces["green"] = _rotate_face_clockwise(self.faces["green"])

        temp_white = [self.faces["white"][2][0], self.faces["white"][2][1], self.faces["white"][2][2]]
        temp_orange = [self.faces["orange"][2][2], self.faces["orange"][1][2], self.faces["orange"][0][2]]
        temp_yellow = [self.faces["yellow"][0][0], self.faces["yellow"][0][1], self.faces["yellow"][0][2]]
        temp_red = [self.faces["red"][0][0], self.faces["red"][1][0], self.faces["red"][2][0]]

        temp_white, temp_orange, temp_yellow, temp_red = temp_orange, temp_yellow, temp_red, temp_white

        self.faces["white"][2][0], self.faces["white"][2][1], self.faces["white"][2][2] = temp_white
        self.faces["orange"][0][2], self.faces["orange"][1][2], self.faces["orange"][2][2] = temp_orange
        self.faces["yellow"][0][2], self.faces["yellow"][0][1], self.faces["yellow"][0][0] = temp_yellow
        self.faces["red"][0][0], self.faces["red"][1][0], self.faces["red"][2][0] = temp_red

    def _rotate_back(self) -> None:
        self.faces["blue"] = _rotate_face_clockwise(self.faces["blue"])

        temp_white = [self.faces["white"][0][0], self.faces["white"][0][1], self.faces["white"][0][2]]
        temp_orange = [self.faces["orange"][0][0], self.faces["orange"][1][0], self.faces["orange"][2][0]]
        temp_yellow = [self.faces["yellow"][2][2], self.faces["yellow"][2][1], self.faces["yellow"][2][0]]
        temp_red = [self.faces["red"][0][2], self.faces["red"][1][2], self.faces["red"][2][2]]

        temp_white, temp_orange, temp_yellow, temp_red = temp_red, temp_white, temp_orange, temp_yellow

        self.faces["white"][0][0], self.faces["white"][0][1], self.faces["white"][0][2] = temp_white
        self.faces["orange"][2][0], self.faces["orange"][1][0], self.faces["orange"][0][0] = temp_orange
        self.faces["yellow"][2][0], self.faces["yellow"][2][1], self.faces["yellow"][2][2] = temp_yellow
        self.faces["red"][0][2], self.faces["red"][1][2], self.faces["red"][2][2] = temp_red

    MOVE_MAP = {
        "R": _rotate_right,
        "L": _rotate_left,
        "U": _rotate_up,
        "D": _rotate_down,
        "F": _rotate_front,
        "B": _rotate_back,
    }

    def apply_move(self, move: str) -> None:
        move = move.strip()
        if not move:
            return
        base = move[0]
        if base not in self.MOVE_MAP:
            raise ValueError(f"Unknown move '{move}'")
        suffix = move[1:]
        turns = 1
        if suffix == "2":
            turns = 2
        elif suffix == "'":
            turns = 3
        elif suffix not in ("",):
            raise ValueError(f"Unsupported move suffix '{suffix}'")
        for _ in range(turns):
            self.MOVE_MAP[base](self)

    def apply_sequence(self, sequence: str) -> None:
        for token in sequence.split():
            self.apply_move(token)

    def scramble(self, length: int = 25) -> str:
        last_move = None
        result = []
        for _ in range(length):
            candidates = [m for m in MOVES if not last_move or m[0] != last_move[0]]
            move = random.choice(candidates)
            suffix = random.choice(["", "2", "'"])
            token = f"{move}{suffix}".strip()
            result.append(token)
            self.apply_move(token)
            last_move = move
        return " ".join(result)

    # --- Editing helpers ---------------------------------------------
    def set_color(self, face: str, row: int, col: int, color: str) -> None:
        internal = FACE_ALIAS.get(face, face)
        if internal not in self.faces:
            raise ValueError(f"Unknown face '{face}'")
        if row == 1 and col == 1:
            raise ValueError("Center stickers are fixed and cannot be painted.")
        if color not in COLOR_LABELS:
            raise ValueError(f"Unknown color '{color}'")
        self.faces[internal][row][col] = color

    def get_color(self, face: str, row: int, col: int) -> str:
        internal = FACE_ALIAS.get(face, face)
        return self.faces[internal][row][col]

    def get_face(self, face: str) -> ColorGrid:
        internal = FACE_ALIAS.get(face, face)
        return self.faces[internal]

    def to_kociemba_string(self) -> str:
        order = ["white", "red", "green", "yellow", "orange", "blue"]
        result = []
        mapping = {
            "w": "U",
            "r": "R",
            "g": "F",
            "y": "D",
            "o": "L",
            "b": "B",
        }
        for face in order:
            for row in self.faces[face]:
                for value in row:
                    result.append(mapping[value])
        return "".join(result)

    def as_dict(self) -> Dict[str, ColorGrid]:
        return {k: [row[:] for row in v] for k, v in self.faces.items()}

    def validate(self) -> Tuple[bool, str | None]:
        counts = {color: 0 for color in COLOR_LABELS}
        for face_name, grid in self.faces.items():
            for row in grid:
                for sticker in row:
                    if sticker not in counts:
                        return False, f"Unknown color '{sticker}' on {face_name} face."
                    counts[sticker] += 1

        for color, expected in counts.items():
            if expected != 9:
                label = COLOR_LABELS[color]
                return False, f"A valid cube needs 9 {label} stickers; found {expected}."

        for face, color in FACE_TO_COLOR.items():
            if self.faces[face][1][1] != color:
                label = COLOR_LABELS[color]
                return False, f"The center of the {face} face must stay {label}."

        return True, None
