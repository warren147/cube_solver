"""3D-ish Rubik's cube renderer built on pygame."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import pygame

from cube import CubeState

Vec3 = Tuple[float, float, float]
Point = Tuple[float, float]

FACE_AXES: Dict[str, Dict[str, Vec3]] = {
    "F": {"normal": (0.0, 0.0, 1.0), "row": (0.0, 1.0, 0.0), "col": (1.0, 0.0, 0.0)},
    "B": {"normal": (0.0, 0.0, -1.0), "row": (0.0, 1.0, 0.0), "col": (-1.0, 0.0, 0.0)},
    "U": {"normal": (0.0, 1.0, 0.0), "row": (0.0, 0.0, -1.0), "col": (1.0, 0.0, 0.0)},
    "D": {"normal": (0.0, -1.0, 0.0), "row": (0.0, 0.0, 1.0), "col": (1.0, 0.0, 0.0)},
    "R": {"normal": (1.0, 0.0, 0.0), "row": (0.0, 1.0, 0.0), "col": (0.0, 0.0, -1.0)},
    "L": {"normal": (-1.0, 0.0, 0.0), "row": (0.0, 1.0, 0.0), "col": (0.0, 0.0, 1.0)},
}

COLOR_RGB = {
    "w": (245, 245, 245),
    "y": (255, 214, 0),
    "g": (48, 157, 84),
    "b": (15, 82, 186),
    "r": (196, 30, 58),
    "o": (222, 105, 16),
}

PICKING_FACES = ["F", "U", "R", "L", "B", "D"]


@dataclass
class StickerProjection:
    face: str
    row: int
    col: int
    polygon: List[Point]
    depth: float


class CubeRenderer:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.scale = min(rect.width, rect.height) * 0.23
        self.offset = (rect.left + rect.width / 2.0, rect.top + rect.height / 2.0)
        self.tile = 0.62
        self.spacing = 0.68

    # --- Math helpers -------------------------------------------------
    def _rotate(self, point: Vec3, yaw: float, pitch: float) -> Vec3:
        x, y, z = point
        cy, sy = math.cos(yaw), math.sin(yaw)
        cp, sp = math.cos(pitch), math.sin(pitch)

        xz_x = x * cy + z * sy
        xz_z = -x * sy + z * cy

        y2 = y * cp - xz_z * sp
        z2 = y * sp + xz_z * cp
        return (xz_x, y2, z2)

    def _project(self, point: Vec3) -> Point:
        x = point[0] * self.scale + self.offset[0]
        y = -point[1] * self.scale + self.offset[1]
        return (x, y)

    def _banner_center(self, axes: Dict[str, Vec3], row: int, col: int) -> Vec3:
        offsets = [-self.spacing, 0.0, self.spacing]
        normal = axes["normal"]
        row_axis = axes["row"]
        col_axis = axes["col"]
        center = _add(_add(normal, _scale(row_axis, offsets[row])), _scale(col_axis, offsets[col]))
        return center

    def _quad(self, face: str, row: int, col: int) -> List[Vec3]:
        axes = FACE_AXES[face]
        center = self._banner_center(axes, row, col)
        row_axis = axes["row"]
        col_axis = axes["col"]
        half = self.tile / 2.0
        corners = [
            _add(_add(center, _scale(col_axis, -half)), _scale(row_axis, -half)),
            _add(_add(center, _scale(col_axis, half)), _scale(row_axis, -half)),
            _add(_add(center, _scale(col_axis, half)), _scale(row_axis, half)),
            _add(_add(center, _scale(col_axis, -half)), _scale(row_axis, half)),
        ]
        return corners

    # --- Public API ---------------------------------------------------
    def draw(
        self,
        surface: pygame.Surface,
        cube: CubeState,
        yaw: float,
        pitch: float,
        highlight: Tuple[str, int, int] | None = None,
        hover_point: Point | None = None,
    ) -> Tuple[List[StickerProjection], Tuple[str, int, int] | None]:
        patches: List[Tuple[float, Tuple[int, int, int], List[Point], Tuple[str, int, int]]] = []
        for face_key in PICKING_FACES:
            face = cube.get_face(face_key)
            axes = FACE_AXES[face_key]
            rotated_normal = self._rotate(axes["normal"], yaw, pitch)
            brightness = 0.25 + 0.75 * max(rotated_normal[2], -0.2)
            for row in range(3):
                for col in range(3):
                    corners = self._quad(face_key, row, col)
                    rotated = [self._rotate(pt, yaw, pitch) for pt in corners]
                    depth = sum(pt[2] for pt in rotated) / len(rotated)
                    polygon = [self._project(pt) for pt in rotated]
                    base_color = COLOR_RGB[face[row][col]]
                    shaded = tuple(
                        max(0, min(255, int(component * brightness))) for component in base_color
                    )
                    patches.append((depth, shaded, polygon, (face_key, row, col)))

        patches.sort(key=lambda item: item[0])
        hover_target: Tuple[str, int, int] | None = None
        if hover_point:
            for depth, _, polygon, meta in reversed(patches):
                if self.polygon_contains(hover_point, polygon):
                    hover_target = meta
                    break

        stickers: List[StickerProjection] = []
        for depth, color, polygon, meta in patches:
            pygame.draw.polygon(surface, color, polygon)
            border_color = (30, 30, 30)
            if meta == highlight or meta == hover_target:
                width = 3
            else:
                width = 1
            pygame.draw.polygon(surface, border_color, polygon, width)
            stickers.append(
                StickerProjection(
                    face=meta[0],
                    row=meta[1],
                    col=meta[2],
                    polygon=polygon,
                    depth=depth,
                )
            )

        stickers.sort(key=lambda item: item.depth, reverse=True)
        return stickers, hover_target

    @staticmethod
    def polygon_contains(point: Point, polygon: Sequence[Point]) -> bool:
        x, y = point
        inside = False
        n = len(polygon)
        for i in range(n):
            j = (i - 1) % n
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            intersect = ((yi > y) != (yj > y)) and (
                x < (xj - xi) * (y - yi) / (yj - yi + 1e-6) + xi
            )
            if intersect:
                inside = not inside
        return inside


def _add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _scale(a: Vec3, scalar: float) -> Vec3:
    return (a[0] * scalar, a[1] * scalar, a[2] * scalar)
