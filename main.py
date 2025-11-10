from __future__ import annotations

import sys
from typing import Callable, List, Sequence, Tuple

import pygame

from cube import CubeState
from renderer import CubeRenderer
from solver import SolverUnavailable, solve_cube

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
PANEL_WIDTH = 320
BG_COLOR = (18, 20, 26)
PANEL_BG = (30, 33, 47)
PANEL_BORDER = (52, 56, 76)
TEXT_COLOR = (232, 236, 244)
MUTED_TEXT = (170, 176, 188)
BUTTON_BG = (63, 99, 191)
BUTTON_HOVER = (95, 132, 214)
BUTTON_DISABLED = (55, 59, 74)
SWATCH_BORDER = (110, 116, 136)

COLOR_OPTIONS = [
    ("w", "White", (245, 245, 245)),
    ("y", "Yellow", (255, 214, 0)),
    ("g", "Green", (48, 157, 84)),
    ("b", "Blue", (15, 82, 186)),
    ("r", "Red", (196, 30, 58)),
    ("o", "Orange", (222, 105, 16)),
]
COLOR_NAME = {code: name for code, name, _ in COLOR_OPTIONS}

SHORTCUT_TEXT = (
    "E: toggle edit • S: scramble • Space: solve • N: next move\n"
    "R/L/U/D/F/B for manual turns (Shift = inverse, Ctrl = double)."
)


class Button:
    def __init__(self, rect: pygame.Rect, label: str, action: Callable[[], None], hotkey: str | None = None):
        self.rect = rect
        self.label = label
        self.action = action
        self.hotkey = hotkey
        self.enabled = True

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, mouse_pos: Tuple[int, int]) -> None:
        base = BUTTON_DISABLED if not self.enabled else BUTTON_BG
        if self.enabled and self.rect.collidepoint(mouse_pos):
            base = BUTTON_HOVER
        pygame.draw.rect(surface, base, self.rect, border_radius=8)
        label = self.label if not self.hotkey else f"{self.label} ({self.hotkey})"
        text = font.render(label, True, TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            self.action()
            return True
        return False


def wrap_text(font: pygame.font.Font, text: str, width: int) -> List[str]:
    result: List[str] = []
    line = ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if not candidate:
            continue
        if font.size(candidate)[0] <= width:
            line = candidate
        else:
            if line:
                result.append(line)
            line = word
    if line:
        result.append(line)
    return result


def draw_wrapped_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: Tuple[int, int, int],
    rect: pygame.Rect,
) -> None:
    y = rect.top
    for paragraph in text.splitlines():
        lines = wrap_text(font, paragraph, rect.width)
        if not lines:
            y += font.get_linesize()
            continue
        for line in lines:
            if y + font.get_linesize() > rect.bottom:
                return
            surf = font.render(line, True, color)
            surface.blit(surf, (rect.left, y))
            y += font.get_linesize()
        y += 2


def draw_panel_block(
    surface: pygame.Surface,
    header_font: pygame.font.Font,
    body_font: pygame.font.Font,
    title: str,
    text: str,
    rect: pygame.Rect,
) -> None:
    header = header_font.render(title, True, TEXT_COLOR)
    surface.blit(header, (rect.left, rect.top))
    body_rect = rect.copy()
    body_rect.top += header.get_height() + 4
    draw_wrapped_text(surface, body_font, text, MUTED_TEXT, body_rect)


def format_solution_preview(moves: Sequence[str]) -> str:
    if not moves:
        return "Solution queue empty."
    display = moves[:18]
    chunks = [" ".join(display[i : i + 6]) for i in range(0, len(display), 6)]
    remaining = len(moves) - len(display)
    if remaining > 0:
        chunks.append(f"(+{remaining} more)")
    return "\n".join(chunks)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("3D Rubik's Cube Solver")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    cube_rect = pygame.Rect(0, 0, SCREEN_WIDTH - PANEL_WIDTH, SCREEN_HEIGHT)
    panel_rect = pygame.Rect(cube_rect.width, 0, PANEL_WIDTH, SCREEN_HEIGHT)

    title_font = pygame.font.SysFont("Helvetica", 26, bold=True)
    body_font = pygame.font.SysFont("Helvetica", 18)
    small_font = pygame.font.SysFont("Helvetica", 14)

    cube = CubeState()
    renderer = CubeRenderer(cube_rect)

    yaw, pitch = 0.8, -0.5
    dragging = False
    last_mouse = (0, 0)
    edit_mode = False
    selected_color = COLOR_OPTIONS[0][0]
    solution_moves: List[str] = []
    status_message = "Drag to rotate the cube."

    swatches = []
    swatch_size = 46
    padding = 16
    for idx, (code, name, color) in enumerate(COLOR_OPTIONS):
        row = idx // 3
        col = idx % 3
        rect = pygame.Rect(
            panel_rect.left + padding + col * (swatch_size + padding),
            90 + row * (swatch_size + padding),
            swatch_size,
            swatch_size,
        )
        swatches.append((rect, code, name, color))

    buttons: List[Button] = []
    button_width = PANEL_WIDTH - 2 * padding
    button_height = 44
    button_y = 90 + 2 * (swatch_size + padding) + 20

    def reset_cube() -> None:
        nonlocal solution_moves, status_message
        cube.reset()
        solution_moves = []
        status_message = "Cube reset to solved state."

    def scramble_cube() -> None:
        nonlocal solution_moves, status_message
        solution_moves = []
        scramble = cube.scramble()
        status_message = f"Scramble applied: {scramble}"

    def solve_current() -> None:
        nonlocal solution_moves, status_message
        valid, reason = cube.validate()
        if not valid:
            status_message = reason or "Cube configuration invalid."
            return
        try:
            solution = solve_cube(cube)
            solution_moves = solution.split()
            if solution_moves:
                status_message = f"Solution ready ({len(solution_moves)} moves)."
            else:
                status_message = "Cube already solved."
        except SolverUnavailable as err:
            status_message = str(err)
        except Exception as err:  # pragma: no cover
            status_message = f"Solver error: {err}"

    def apply_next_move() -> None:
        nonlocal status_message, solution_moves
        if not solution_moves:
            status_message = "No queued moves."
            return
        move = solution_moves.pop(0)
        cube.apply_move(move)
        status_message = f"Applied {move}. {len(solution_moves)} moves left."

    def toggle_edit_mode() -> None:
        nonlocal edit_mode, status_message, dragging
        edit_mode = not edit_mode
        dragging = False
        mode = "Edit" if edit_mode else "Rotate"
        status_message = f"{mode} mode active."

    button_specs = [
        ("Toggle Edit", toggle_edit_mode, "E"),
        ("Reset Cube", reset_cube, "Bksp"),
        ("Scramble", scramble_cube, "S"),
        ("Solve", solve_current, "Space"),
        ("Apply Next Move", apply_next_move, "N"),
    ]

    step_button: Button | None = None
    for label, action, hotkey in button_specs:
        rect = pygame.Rect(panel_rect.left + padding, button_y, button_width, button_height)
        button = Button(rect, label, action, hotkey)
        buttons.append(button)
        if label.startswith("Apply"):
            step_button = button
        button_y += button_height + 10

    content_top = button_y + 10
    content_width = PANEL_WIDTH - 2 * padding
    solution_rect = pygame.Rect(panel_rect.left + padding, content_top, content_width, 120)
    status_rect = pygame.Rect(panel_rect.left + padding, solution_rect.bottom + 12, content_width, 110)
    shortcut_rect = pygame.Rect(
        panel_rect.left + padding,
        status_rect.bottom + 12,
        content_width,
        max(60, panel_rect.bottom - padding - (status_rect.bottom + 12)),
    )

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_e:
                    toggle_edit_mode()
                elif event.key == pygame.K_s:
                    scramble_cube()
                elif event.key == pygame.K_SPACE:
                    solve_current()
                elif event.key == pygame.K_BACKSPACE:
                    reset_cube()
                elif event.key == pygame.K_n:
                    apply_next_move()
                else:
                    move_map = {
                        pygame.K_r: "R",
                        pygame.K_l: "L",
                        pygame.K_f: "F",
                        pygame.K_b: "B",
                        pygame.K_u: "U",
                        pygame.K_d: "D",
                    }
                    base = move_map.get(event.key)
                    if base:
                        mods = pygame.key.get_mods()
                        suffix = ""
                        if mods & pygame.KMOD_SHIFT:
                            suffix = "'"
                        elif mods & pygame.KMOD_CTRL:
                            suffix = "2"
                        cube.apply_move(base + suffix)
                        status_message = f"Applied {base + suffix}."
                        solution_moves = []
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                consumed = False
                for button in buttons:
                    if button.handle_event(event):
                        consumed = True
                        break
                if consumed:
                    continue
                for rect, code, name, color in swatches:
                    if rect.collidepoint(event.pos):
                        selected_color = code
                        status_message = f"Selected {name}."
                        consumed = True
                        break
                if consumed:
                    continue
                if not edit_mode and cube_rect.collidepoint(event.pos):
                    dragging = True
                    last_mouse = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - last_mouse[0]
                dy = event.pos[1] - last_mouse[1]
                yaw += dx * 0.01
                pitch += dy * 0.01
                pitch = max(-1.2, min(1.2, pitch))
                last_mouse = event.pos

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BG_COLOR)

        hover_point = mouse_pos if edit_mode and cube_rect.collidepoint(mouse_pos) else None
        stickers, hover_target = renderer.draw(
            screen,
            cube,
            yaw,
            pitch,
            highlight=None,
            hover_point=hover_point,
        )

        pygame.draw.rect(screen, PANEL_BG, panel_rect)
        pygame.draw.rect(screen, PANEL_BORDER, panel_rect, width=1)

        title = title_font.render("Cube Solver", True, TEXT_COLOR)
        screen.blit(title, (panel_rect.left + padding, 24))
        mode_text = "EDIT MODE" if edit_mode else "ROTATION MODE"
        mode_surf = small_font.render(mode_text, True, MUTED_TEXT)
        screen.blit(mode_surf, (panel_rect.left + padding, 56))

        for rect, code, _, color in swatches:
            pygame.draw.rect(screen, color, rect, border_radius=8)
            border = BUTTON_BG if code == selected_color else SWATCH_BORDER
            pygame.draw.rect(screen, border, rect, width=2, border_radius=8)

        if step_button:
            step_button.enabled = bool(solution_moves)

        for button in buttons:
            button.draw(screen, body_font, mouse_pos)

        if edit_mode and pygame.mouse.get_pressed()[0] and hover_target:
            try:
                cube.set_color(hover_target[0], hover_target[1], hover_target[2], selected_color)
            except ValueError as err:
                status_message = str(err)
            else:
                status_message = f"Painted {hover_target[0]}[{hover_target[1] + 1},{hover_target[2] + 1}]."
                solution_moves = []
            stickers, hover_target = renderer.draw(
                screen,
                cube,
                yaw,
                pitch,
                highlight=None,
                hover_point=hover_point,
            )

        hover_line = ""
        if edit_mode and hover_target:
            face, row, col = hover_target
            current_color = cube.get_color(face, row, col)
            hover_line = f"Hover: {face} r{row + 1} c{col + 1} ({COLOR_NAME.get(current_color, current_color)})"
        elif edit_mode:
            hover_line = "Hover a sticker to preview it."
        else:
            hover_line = "Hold left mouse to rotate."

        solution_text = format_solution_preview(solution_moves)
        draw_panel_block(screen, body_font, small_font, "Solution", solution_text, solution_rect)
        draw_panel_block(
            screen,
            body_font,
            small_font,
            "Status",
            f"{status_message}\n{hover_line}",
            status_rect,
        )
        draw_panel_block(screen, body_font, small_font, "Shortcuts", SHORTCUT_TEXT, shortcut_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
