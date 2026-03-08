from typing import Dict, List, Tuple, Union
import time
import shutil
import re
import sys


def visible_len(text: str) -> int:
    """Return length of string ignoring ANSI escape codes"""
    pattern = re.compile(r'\x1b\[[0-9;]*m')
    return len(pattern.sub('', text))


def get_terminal_width() -> int:
    try:
        return shutil.get_terminal_size().columns
    except OSError:
        return 80


def center_text(text: str, width: int) -> str:
    try:
        width = int(width)
        term_width = get_terminal_width()
        if width > term_width:
            print("tha maze width is is bigr than width of tirmnal")
            sys.exit()
        padding = max((term_width - visible_len(text)) // 2, 0)
        return " " * padding + text
    except Exception as e:
        print(e)
        return text


def loading(tmie: float = 0, file_name: str = "ami-ascii.txt") -> None:
    data = None
    try:
        tmie = float(tmie)
    except ValueError:
        tmie = 0
    try:
        with open(file_name, 'r') as file:
            data = [line.rstrip('\n') for line in file]
    except Exception as e:
        print(e)
    if not data:
        print("No loading file name data")
    else:
        print('\n\n\n\n\n\n')
        print("\033[38;2;0;255;0m")  # Green
        for line in data:
            print(center_text(line, 75))
            time.sleep(tmie)
        print("\033[0m")


def decode_cell(value: str) -> Dict[str, bool]:
    """Decode hex cell value into wall directions."""
    try:
        int_value = int(value, 16)
        bits = format(int_value, "04b")
        return {
            'N': bits[3] == '1',
            'E': bits[2] == '1',
            'S': bits[1] == '1',
            'W': bits[0] == '1',
        }
    except Exception as e:
        print(e)
        return {'N': False, 'E': False, 'S': False, 'W': False}


def decode_cell_for_animate(value: str, index: int) -> Dict[str, bool]:
    """Decode hex cell value into wall directions."""
    try:
        index = int(index)
        if index >= 4 or index < 0:
            index = 0
        int_value = int(value, 16)
        bits = format(int_value, "04b")
        return {
            'N': bits[index] == '1',
            'E': bits[index] == '1',
            'S': bits[index] == '1',
            'W': bits[index] == '1',
        }
    except Exception as e:
        print(e)
        return {'N': False, 'E': False, 'S': False, 'W': False}


directions: Dict[str, Tuple[int, int]] = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1),
}


def fetch_path(path: Union[str, List[str]],
               start: Tuple[int, int]
               ) -> List[Union[Tuple[int, int], Tuple[int, int, int]]]:
    if not path or not start:
        print("Path not found or start missing")
        sys.exit()

    path_solve: List[Union[Tuple[int, int], Tuple[int, int, int]]] = []
    start_point: Union[Tuple[int, int], Tuple[int, int, int]] = start
    if isinstance(path, str):
        for x in path:
            dy, dx = directions[x]
            assert isinstance(start_point, tuple) and len(start_point) >= 2
            start_point = (start_point[0] + dy, start_point[1] + dx)
            path_solve.append(start_point)
        return path_solve
    elif isinstance(path, list):
        indx = 0
        for x in path:
            start_point = start
            for y in x:
                dy, dx = directions[y]
                assert isinstance(start_point, tuple) and len(start_point) >= 2
                start_point = (start_point[0] + dy, start_point[1] + dx, indx)
                path_solve.append(start_point)
            indx += 1
        return path_solve
    return path_solve


COLORS: Dict[str, Union[Dict[int, str], str]] = {
    "wall": {
        1: "\033[91m",  # Bright red
        2: "\033[92m",  # Bright green
        3: "\033[95m"   # Bright magenta
    },
    "space": {
        1: "\033[108m",  # Bright white space
        2: "\033[107m",
        3: "\033[107m"
    },
    "solve": {
        1: "\033[44m",  # Blue
        2: "\033[43m",  # Yellow
        3: "\033[42m"   # Green
    },
    "reset": "\033[0m"
}

WALL: Dict[int, Dict[str, str]] = {
    0: {"corner_tl": "╔", "corner_tr": "━━━╗", "corner_bl": "╚",
        "corner_br": "╝", "h": "━━━", "v": "┃", "h+1": "━━━━"},
    1: {"corner_tl": "+", "corner_tr": "===+", "corner_bl": "+",
        "corner_br": "+", "h": "===", "v": "║", "h+1": "===="},
    2: {"corner_tl": "╔", "corner_tr": "━━━╗", "corner_bl": "╚",
        "corner_br": "╝", "h": "━━━", "v": "┃", "h+1": "━━━━"},
    3: {"corner_tl": "╔", "corner_tr": "━━━╗", "corner_bl": "╚",
        "corner_br": "╝", "h": "━━━", "v": "┃", "h+1": "━━━━"}
}

_wall_colors = COLORS["wall"]
_space_colors = COLORS["space"]
_solve_colors = COLORS["solve"]
assert isinstance(_wall_colors, dict)
assert isinstance(_space_colors, dict)
assert isinstance(_solve_colors, dict)

COLOR_MENU: Dict[int, Dict[str, str]] = {
    0: {
        "wall_color": "\033[37m",
        "space_color": "\033[47m",  # Black background for empty space
        "solve_color": "\033[67m",  # Blue background for path / arrows
    },
    1: {
        "wall_color": _wall_colors[1],
        "space_color": _space_colors[1],
        "solve_color": _solve_colors[1],
    },
    2: {
        "wall_color": _wall_colors[2],
        "space_color": _space_colors[2],
        "solve_color": _solve_colors[2],
    },
    3: {
        "wall_color": _wall_colors[3],
        "space_color": _space_colors[3],
        "solve_color": _solve_colors[3],
    },
    4: {
        "wall_color": "\033[31m",
        "space_color": "\033[30m",
        "solve_color": "\033[33m",
    },
    5: {
        "wall_color": "\033[32m",
        "space_color": "\033[30m",
        "solve_color": "\033[35m",
    },
    6: {
        "wall_color": "\033[34m",
        "space_color": "\033[37m",
        "solve_color": "\033[31m",
    },
    7: {
        "wall_color": "\033[35m",
        "space_color": "\033[36m",
        "solve_color": "\033[33m",
    },
    8: {
        "wall_color": "\033[91m",
        "space_color": "\033[90m",
        "solve_color": "\033[93m",
    },
    9: {
        "wall_color": "\033[94m",
        "space_color": "\033[97m",
        "solve_color": "\033[92m",
    },
}

FORTY_TWO_COLORS: List[str] = [
    "\033[40m",
    "\033[48;5;196m",
    "\033[48;5;202m",
    "\033[48;5;46m",
    "\033[48;5;51m",
    "\033[48;5;226m",
    "\033[48;5;201m",
]

ARROWS: Dict[str, str] = {
    "N": "⟰",
    "S": "⟱",
    "E": "⭆",
    "W": "⭅",
}


if __name__ == "__main__":
    loading()
