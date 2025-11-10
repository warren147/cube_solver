"""Wrapper around the kociemba solver with graceful fallbacks."""
from __future__ import annotations

from cube import CubeState

try:
    import kociemba  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    kociemba = None


class SolverUnavailable(RuntimeError):
    """Raised when the optional solver backend is missing."""


def solve_cube(cube: CubeState) -> str:
    if not kociemba:
        raise SolverUnavailable(
            "kociemba is not installed. Install it with 'pip install kociemba' to enable solving."
        )
    state = cube.to_kociemba_string()
    return kociemba.solve(state)
