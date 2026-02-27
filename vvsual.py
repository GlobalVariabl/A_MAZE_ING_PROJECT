import os
import shutil
import sys
import random
import time
import re

from help import loading, COLORS, WALL, COLOR_MENU, decode_cell, ARROWS, FORTY_TWO_COLORS, decode_cell_for_animate


def export_output(output_file: str) -> dict:
    """Parse maze output file into structured data."""
    try:
        with open(output_file, 'r') as file:
            lines = [line.rstrip("\n") for line in file]

        end_maze = lines.index("")
        maze = lines[:end_maze]
        path = lines[-1].strip()
        start = [int(x) for x in lines[end_maze+1].split(",")]
        end = [int(x) for x in lines[end_maze+2].split(",")]
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


def print_live_maze(data: dict, show: bool = False, change_color: bool = False,
                    display_42: bool = False, animate_maze: bool = False,
                    frame: int = 0) -> None:
    """Print formatted maze with path visualization."""
    try:
        if not data:
            print("No maze data available")
            return
        maze = data.get("maze", [])
        start = tuple(data.get("start"))
        end = tuple(data.get("end"))
        path = data.get("path")
        height = len(maze)
        width = len(maze[0])
        directions = {
            'N': (-1, 0),
            'E': (0, 1),
            'S': (1, 0),
            'W': (0, -1),
            }

        path_solve = []
        if path:
            start_point = start
            for x in path:
                dy, dx = directions[x]
                start_point = (start_point[0] + dy, start_point[1] + dx)
                path_solve.append(start_point)

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
        wall_color = menu["wall_color"]
        space_color = FORTY_TWO_COLORS[forty_two]
        solve_color = menu["solve_color"]
        wall_type = WALL[choice]
        clear_terminal()
        loading()

        line = wall_color + wall_type["corner_tl"] + wall_type["h+1"] * (width - 1) + wall_type["corner_tr"] + COLORS["reset"]
        print(center_text(line))

        for y in range(height):
            row_top = wall_color + "┃" + COLORS["reset"]
            row_bottom = wall_color + (wall_type["corner_bl"] if y == height - 1 else wall_type["v"]) + COLORS["reset"]
            for x in range(width):
                if animate_maze:
                    cell_walls = decode_cell_for_animate(maze[y][x], frame)
                else:
                    cell_walls = decode_cell(maze[y][x])

                if (y, x) == start:
                    cell_char = COLORS["reset"] + solve_color + " S " + COLORS["reset"] + wall_color
                elif (y, x) == end:
                    cell_char = solve_color + " X " + COLORS["reset"] + wall_color 
                elif show and (y, x) in path_solve:
                    arrow = f" {ARROWS[path[path_solve.index((y, x))]]} "
                    cell_char = solve_color + arrow + COLORS["reset"] + wall_color 
                else:
                    if all(cell_walls.values()):
                        cell_char = COLORS["reset"] + space_color + "░░░" + COLORS["reset"] + wall_color
                    else:
                        cell_char = "   " + wall_color

                row_top += wall_color + cell_char + (wall_type["v"] if cell_walls['E'] or x == width - 1 else " ") + COLORS["reset"]
                # 3. South Wall (Horizontal)
                row_bottom += wall_color + (wall_type["h"] if cell_walls['S'] or y == height - 1 else "   ") + COLORS["reset"]
                if x < width - 1:
                    if y < height - 1:
                        # Inside the maze: Use a cross-junction
                        row_bottom += wall_color + "╋" + COLORS["reset"] 
                    else:
                        # Bottom edge: Use a T-junction pointing up
                        row_bottom += wall_color + "┻" + COLORS["reset"]
                else:
                    if y < height - 1:
                        # Right edge: Use a T-junction pointing left
                        row_bottom += COLORS["reset"] + wall_color + "┃" + COLORS["reset"]
                    else:
                        # Final bottom-right corner "┛"
                        row_bottom += wall_color + wall_type["corner_br"] + COLORS["reset"]

            print(center_text(row_top))
            print(center_text(row_bottom))

    except Exception as e:
        print(f"Error printing maze: {e}")
        sys.exit()


def new_maze(maze):
    """Generate and display new maze."""
    maze.re_import_with_new_maze()
    display = export_output(maze.output_file)
    if display:
        print_live_maze(display, False, False, False)


def visible_len(text: str) -> int:
    """Return length of string ignoring ANSI escape codes"""
    ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')
    return len(ANSI_ESCAPE.sub('', text))


def get_terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except OSError:
        return 80


def center_text(text: str) -> str:
    term_width = get_terminal_width()
    padding = max((term_width - visible_len(text)) // 2, 0)
    return " " * padding + text


def clear_terminal():
    os.system('clear')


def quit_terminal():
    sys.exit()


def show_menu(maze) -> None:
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
            print("4. Change “42” colours")
            print("5. Animate maze generation")
            print("6. Quit")
            choice_input = input(center_text("Choice? (1-6): ")).strip()
            if choice_input.isdigit():
                choice = int(choice_input)
                if 1 <= choice <= 6:
                    display = export_output(maze.output_file)
                    if choice == 1:
                        new_maze(maze)
                        show_path = False
                    elif choice == 2:
                        show_path = not show_path
                        display = export_output(maze.output_file)
                        print_live_maze(display, show_path, False, False)
                    elif choice == 3:
                        change_color = True
                        print_live_maze(display, show_path,
                                        change_color, False)
                    elif choice == 4:
                        forty_two = True
                        print_live_maze(display, show_path, False, forty_two)
                    elif choice == 5:
                        display = export_output(maze.output_file)
                        indx = 0
                        while indx < 4:
                            print_live_maze(display, False, False,
                                            change_color, True, indx)
                            time.sleep(0.4)
                            indx += 1
                        print_live_maze(display, show_path,
                                        False, forty_two, False)
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


def to_start(maze) -> None:
    clear_terminal()
    loading(0.3, "ascii-art.txt")
    display = export_output(maze.output_file)
    print_live_maze(display, False, False, False)
    show_menu(maze)
