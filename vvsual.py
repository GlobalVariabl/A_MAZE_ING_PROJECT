import os
import sys
import random
import time
from typing import Any, Dict, List, Tuple, Union

from help import loading, COLORS, WALL, COLOR_MENU, decode_cell, center_text
from help import ARROWS, FORTY_TWO_COLORS, decode_cell_for_animate, fetch_path
from cls_generator import MazeGenerator


def export_output(output_file: str) -> Dict[str, Any]:
    try:
        with open(output_file, 'r') as file:
            lines = [line.rstrip("\n") for line in file]

        end_maze: int = lines.index("")
        maze: List[str] = lines[:end_maze]
        path: str = lines[-1].strip()
        start: List[int] = [int(x) for x in lines[end_maze+1].split(",")]
        end: List[int] = [int(x) for x in lines[end_maze+2].split(",")]
        if not maze or not path or not start or not end:
            print(f"The file {output_file} cannot be empty")
            return {}
        return {
            "maze": maze,
            "path": path,
            "start": start,
            "end": end
        }
    except FileNotFoundError as e:
        print(e)
        return {}
    except Exception as e:
        print(e)
        return {}


def print_live_maze(data: Dict[str, Any],
                    show: bool = False,
                    change_color: bool = False,
                    display_42: bool = False,
                    animate_maze: bool = False,
                    three_path: bool = False,
                    frame: int = 0) -> None:
    try:
        if not data:
            print("No maze data available")
            return
        maze: List[str] = data.get("maze", [])
        start_data: List[int] = data.get("start") or []
        end_data: List[int] = data.get("end") or []
        path: str = data.get("path") or ""
        height = len(maze)
        width = len(maze[0])

        start: Tuple[int, int] = (start_data[0], start_data[1])
        end: Tuple[int, int] = (end_data[0], end_data[1])
        path_solve: List[Union[Tuple[int, int], Tuple[int, int, int]]]
        path_solve = fetch_path(path, start)
        choice_color = 0
        choice = 0
        if change_color:
            choice_color = random.randint(1, 9)
            choice = random.randint(0, 3)
        else:
            choice_color = 0
        forty_two = 0
        if display_42:
            forty_two = random.randint(1, 4)

        menu = COLOR_MENU[choice_color]
        wall_color: str = menu["wall_color"]
        space_color: str = FORTY_TWO_COLORS[forty_two]
        solve_color: str = menu["solve_color"]
        wall_type = WALL[choice]
        clear_terminal()
        loading()

        reset: str = str(COLORS["reset"])
        line = (wall_color + wall_type["corner_tl"]
                + wall_type["h+1"] * (width - 1) + wall_type["corner_tr"]
                + reset)
        print(center_text(line, width))

        for y in range(height):
            row_top: str = wall_color + "┃" + reset
            row_bottom: str = (wall_color
                               + (wall_type["corner_bl"] if y == height - 1
                                  else wall_type["v"])
                               + reset)
            for x in range(width):
                if animate_maze:
                    cell_walls = decode_cell_for_animate(maze[y][x], frame)
                else:
                    cell_walls = decode_cell(maze[y][x])

                cell_char: str
                if (y, x) == start:
                    cell_char = (reset + solve_color + " S " + reset +
                                 wall_color)
                elif (y, x) == end:
                    cell_char = solve_color + " X " + reset + wall_color
                elif show and not three_path and (y, x) in path_solve:
                    arrow = f" {ARROWS[path[path_solve.index((y, x))]]} "
                    cell_char = solve_color + arrow + reset + wall_color
                elif three_path:
                    if (y, x, 0) in path_solve:
                        cell_char = (reset + "\033[41m" + " 1 " + reset +
                                     wall_color)
                    elif (y, x, 1) in path_solve:
                        cell_char = (reset + "\033[42m" + " 2 " + reset +
                                     wall_color)
                    elif (y, x, 2) in path_solve:
                        cell_char = (reset + "\033[43m" + " 3 " + reset +
                                     wall_color)
                    elif all(cell_walls.values()):
                        cell_char = (reset + space_color + "░░░" + reset +
                                     wall_color)
                    else:
                        cell_char = "   " + wall_color
                elif all(cell_walls.values()):
                    cell_char = (reset + space_color + "░░░" + reset +
                                 wall_color)
                else:
                    cell_char = "   " + wall_color

                row_top += (wall_color + cell_char
                            + (wall_type["v"]
                               if cell_walls['E'] or x == width - 1 else " ")
                            + reset)
                row_bottom += (wall_color +
                               (wall_type["h"]
                                if cell_walls['S'] or y == height - 1
                                else "   ") + reset)
                if x < width - 1:
                    if y < height - 1:
                        row_bottom += wall_color + "╋" + reset
                    else:
                        row_bottom += wall_color + "┻" + reset
                else:
                    if y < height - 1:
                        row_bottom += reset + wall_color + "┃" + reset
                    else:
                        row_bottom += (wall_color + wall_type["corner_br"] +
                                       reset)

            print(center_text(row_top, width))
            print(center_text(row_bottom, width))

    except Exception as e:
        print(f"Error printing maze: {e}")
        sys.exit()


def animate_maze_generation(maze: MazeGenerator) -> None:
    display = export_output(maze.output_file)
    indx = 0
    while indx < 4:
        print_live_maze(display, False, False, True, True, False, indx)
        time.sleep(0.4)
        indx += 1
    print_live_maze(display, False, False, False, False, False)


def new_maze(maze: MazeGenerator) -> None:
    maze.re_import_with_new_maze()
    display = export_output(maze.output_file)
    if display:
        animate_maze_generation(maze)


def clear_terminal() -> None:
    os.system('clear')


def quit_terminal() -> None:
    sys.exit()


def show_menu(maze: MazeGenerator, width: int) -> None:
    """Display interactive menu."""
    show_path = False
    change_color = False
    forty_two = False
    try:
        while True:
            print("\n", " " * 6, "=== Menu ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from start to exit")
            print("3. Change maze wall colours")
            print("4. Change '42' colours")
            print("5. Show three maze paths")
            print("6. Quit")
            choice_input = input(center_text("Choice? (1-6): ", width)).strip()
            if choice_input.isdigit():
                choice = int(choice_input)
                if 1 <= choice <= 6:
                    display = export_output(maze.output_file)
                    three_path = maze.get_selected_solution(2)
                    if choice == 1:
                        new_maze(maze)
                        show_path = False
                    elif choice == 2:
                        show_path = not show_path
                        print_live_maze(display, show_path, False, False)
                    elif choice == 3:
                        change_color = True
                        print_live_maze(display, show_path, change_color,
                                        False)
                    elif choice == 4:
                        forty_two = True
                        print_live_maze(display, show_path, False, forty_two)
                    elif choice == 5:
                        display["path"] = three_path
                        print_live_maze(display, True, False, forty_two, False,
                                        True)
                    elif choice == 6:
                        clear_terminal()
                        quit_terminal()
                else:
                    print("Invalid choice. Please enter 1-5.")
            else:
                print("Invalid input. Please enter a number between 1 and 5. ")
                break
    except Exception as e:
        print(e)


def to_start(maze: MazeGenerator) -> None:
    clear_terminal()
    # loading(0.3, "ascii-art.txt")
    display = export_output(maze.output_file)
    print_live_maze(display, False, False, False)
    show_menu(maze, len(display['maze'][0]))
