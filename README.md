*This project has been created as part of the 42 curriculum by [magram], [souhsain].*

# AMI — ASCII Maze Interactive

## Description

AMI is a terminal-based maze generator and solver written in Python. The program reads a configuration file, procedurally generates a maze of the requested dimensions, solves it, and renders it interactively in the terminal using Unicode box-drawing characters and ANSI colour codes.

The goal of the project is to implement maze generation and pathfinding algorithms from scratch and present the result as a visually rich, interactive terminal application. The user can regenerate the maze, toggle the solution path, cycle through colour themes, and reveal a hidden **42** easter egg embedded directly into the maze structure.

The project is split across four source files:

| File | Role |
|---|---|
| `a_maze_ing.py` | Entry point — parses the config file and launches the UI |
| `cls_generator.py` | `MazeGenerator` class — generation, solving, file I/O |
| `vvsual.py` | Rendering and interactive menu |
| `help.py` | Shared utilities, constants, and colour tables |

---

## Instructions

### Requirements

- Python 3.10 or later
- A terminal that supports ANSI escape codes and Unicode (any modern Linux/macOS terminal)

### Running the program

```bash
python3 a_maze_ing.py <config.txt>

or 

make run
```

Example:

```bash
python3 a_maze_ing.py config.txt

or 

make run
```

### Config file format

The config file is a plain-text key=value file. Lines beginning with `#` and blank lines are ignored. All keys are case-insensitive.

```ini
# AMI config file

WIDTH       = 27        # Number of columns (required, positive integer)
HEIGHT      = 37        # Number of rows    (required, positive integer)
ENTRY       = 0,0       # Entry point as row,col (required)
EXIT        = 36,26     # Exit point  as row,col (required)
OUTPUT_FILE = maze.out  # Path to write the generated maze file (required)
PERFECT     = true      # true = perfect maze (no loops); false = imperfect (optional, default: true)
SEED        = 42        # Integer seed for reproducible generation (optional)
ALGO        = dfs       # Generation algorithm: dfs or prims (optional, default: dfs)
```

**Constraints:**
- `WIDTH` and `HEIGHT` must be positive integers.
- `ENTRY` and `EXIT` must be valid coordinates within the maze bounds and must not be the same point.
- If `PERFECT = false`, extra random passages are carved to create loops and multiple solution paths.
- Omitting `SEED` produces a different maze on each run.
- The 42 easter egg requires a maze of at least `WIDTH ≥ 9` and `HEIGHT ≥ 7`. If the maze is too small, or if ENTRY/EXIT overlap the reserved area, a warning is printed.

### Output file format

The generator writes a structured text file used by the renderer:

```
<maze rows as hex characters, one row per line>
<blank line>
<entry row>,<entry col>
<exit row>,<exit col>
<solution path as a string of N/E/S/W characters>
```

Each hex character encodes the walls of one cell as a 4-bit value: bit 3 = N, bit 2 = E, bit 1 = S, bit 0 = W. A set bit means the wall is present. For example, `F` (1111) is a fully walled cell and `0` (0000) is fully open.

### Interactive menu

Once the maze is displayed, a menu appears:

```
1. Re-generate a new maze
2. Show/Hide path from start to exit
3. Change maze wall colours
4. Change '42' colours
5. Show three maze paths
6. Quit
```

---

## Features

### Maze generation algorithms

**Depth-First Search (DFS)** is the default algorithm (`ALGO = dfs`). Starting from the ENTRY cell, it recursively visits unvisited neighbours in a random order, carving passages as it goes. Because every cell is visited exactly once and the result is a spanning tree, the output is always a *perfect* maze — exactly one path exists between any two cells.

DFS was chosen because:
- It is straightforward to implement recursively and easy to reason about.
- It produces long, winding corridors with relatively few dead-ends near the start, which makes the solution non-trivial to trace visually.
- It naturally integrates with the forbidden-coordinate system used by the 42 easter egg — cells pre-marked as visited are simply skipped during generation.

**Prim's algorithm** is also available (`ALGO = prims`). It grows the maze outward from the entry point by maintaining a frontier of candidate walls and picking one at random, producing a more uniform, "bushy" structure with shorter average path lengths.

### Imperfect mazes

Setting `PERFECT = false` runs a post-processing pass (`create_other_paths`) that randomly removes additional walls, introducing loops and creating multiple valid routes between ENTRY and EXIT.

### Pathfinding

The solver uses **Breadth-First Search (BFS)** to guarantee the shortest path. Up to three distinct paths can be found via a depth-limited recursive search (`solve_all_paths`), shown simultaneously in the menu's option 5 with colour-coded overlays.

### 42 easter egg

When the maze is large enough, a block of cells forming the digits **42** is pre-marked as visited before generation begins. The generator never carves passages through these cells, leaving them as fully-walled islands. The renderer draws them with a distinct background colour.

### Colour themes

Ten colour themes (0–9) are available, randomised when option 3 is selected. The 42 easter egg cells cycle through seven additional background colours independently when option 4 is active.

---

## Reusable components

`help.py` is entirely independent of the maze logic and can be dropped into any terminal Python project:

- `visible_len(text)` — measures string length ignoring ANSI escape sequences, useful for any terminal layout calculation.
- `center_text(text, width)` — centres a (potentially ANSI-coloured) string in the terminal.
- `loading(time, file)` — renders any ASCII art file with a per-line delay.
- `decode_cell(value)` — converts a hex wall-encoding character to a `{N, E, S, W: bool}` dict; useful for any grid-based map format that encodes adjacency as bitmasks.
- `fetch_path(path, start)` — converts a string of cardinal directions into a list of absolute coordinates; works for both single paths and lists of paths.
- `COLORS`, `COLOR_MENU`, `WALL`, `ARROWS` — ANSI colour and box-drawing constant tables.

The `MazeGenerator` class in `cls_generator.py` is also self-contained. It can be imported and used independently to generate and export mazes without the visual layer:

```python
from cls_generator import MazeGenerator

maze = MazeGenerator(27, 37, (0, 0), (36, 26), "out.txt", True, None, "dfs")
maze.generate_maze()
maze.import_maze()
print(maze.solve_the_maze())       # shortest path string
print(maze.get_selected_solution(2))  # up to 3 distinct paths
```

---

## Team and project management

### Roles

| Member | Responsibilities |
|---|---|
| souhsain | `cls_generator.py` — maze generation algorithms, BFS/DFS solver, file I/O and the overall project's structure |
| magram | `vvsual.py` + `help.py` — terminal renderer, colour system, interactive menu, easter egg layout |

`a_maze_ing.py` and integration testing were shared between both members.

### Planning

**Initial plan:** We estimated one week for generation, one week for rendering, and a final week for integration and polish.

**How it evolved:** Generation was completed on schedule. The rendering phase ran longer than expected — centering ANSI-coloured strings required building `visible_len` as a separate utility, and the 42 easter egg required coordinating between the generator's visited-cell pre-allocation and the renderer's colour pass. Integration and final type-checking took an additional two days.

### What worked well

- Encoding walls as 4-bit hex values kept the output file compact and made the renderer straightforward to write.
- Separating `help.py` early meant both members could work on their modules in parallel without merge conflicts.
- Adding a `SEED` option made debugging reproducible — the same maze could be regenerated exactly for testing.


### What could be improved

- The recursion depth limit (`sys.setrecursionlimit(5000)`) is a workaround; a future version should convert `generate_maze_dfs` to an iterative stack-based implementation.
- The config parser is minimal — a more robust parser (e.g. using `configparser` from the standard library) would handle edge cases more gracefully.
- The three-path solver stops at three paths but does not guarantee they are meaningfully different; a diversity heuristic could improve this.

### Tools used

- **Python 3.12** — primary language
- **MyPy** — static type checking throughout development
- **Git / GitHub** — version control and collaboration
- **Claude (Anthropic)** — used for MyPy error resolution: identifying incompatible type annotations (`list[tuple[()]]`, untyped `deque`, bare `dict` return types), suggesting correct `typing` module annotations, and converting the `MazeController` stub to a proper `Protocol` class. All logic, algorithms, and design decisions were made by the team.

---

## Resources

- [Maze generation algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Depth-first search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Prim's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Breadth-first search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [ANSI escape codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Unicode box-drawing characters](https://www.unicode.org/charts/PDF/U2500.pdf)
- [Python `typing` module documentation](https://docs.python.org/3/library/typing.html)
- [MyPy documentation](https://mypy.readthedocs.io/en/stable/)
- [Jamis Buck — *Mazes for Programmers* (book)](https://pragprog.com/titles/jbmaze/mazes-for-programmers/) — comprehensive reference on maze algorithms and representations
- [Jamis Buck's maze algorithm blog series](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)