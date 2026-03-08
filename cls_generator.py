import random
import sys
from typing import List, Tuple, Union
from collections import deque
sys.setrecursionlimit(5000)


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple, exit: tuple,
                 output_file: str, perfect: bool, seed: int, algo: str):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.forbidden_coordinates: List[Tuple[int, int]] = []
        self.seed = seed
        self.algo = algo
        if algo is None:
            self.algo = "dfs"
        if seed is not None:
            random.seed(seed)
        self.maze = [[15 for _ in range(width)] for _ in range(height)]

    N, E, S, W = 0, 1, 2, 3

    directions = {
        N: (-1, 0),
        E: (0, 1),
        S: (1, 0),
        W: (0, -1)
    }

    oposite = {N: S, E: W, S: N, W: E}
    type_solving = {"Closer": 0, "Farther": 1, "All": 2}

    def allocate_irea_for_print(self, visited: list[list],
                                from_regenarate: bool) -> None:
        start_x = self.height - 5
        start_y = self.width - 7
        if start_x < 2 or start_y < 2:
            if not from_regenarate:
                print("WARNING: the size of maze not enough for dicplai 42")
                print("Press Enter to continue...")
                input()
            return
        start_x //= 2
        start_y //= 2
        coords = [
                (start_x, start_y),
                (start_x + 1, start_y),
                (start_x + 2, start_y),
                (start_x + 2, start_y + 1),
                (start_x + 2, start_y + 2),
                (start_x + 3, start_y + 2),
                (start_x + 4, start_y + 2),

                (start_x, start_y + 4),
                (start_x, start_y + 5),
                (start_x, start_y + 6),
                (start_x + 1, start_y + 6),
                (start_x + 2, start_y + 4),
                (start_x + 2, start_y + 5),
                (start_x + 2, start_y + 6),
                (start_x + 3, start_y + 4),
                (start_x + 4, start_y + 4),
                (start_x + 4, start_y + 5),
                (start_x + 4, start_y + 6),
            ]
        self.forbidden_coordinates = coords
        if self.entry in coords or self.exit in coords:
            if not from_regenarate:
                print("WORNING: the entry or exit coordinats of maze allocate"
                      " 42 Blocks so it wont dicplai")
                print("Press Enter to continue...")
                input()
            return

        # alocate 4 in 7 blocks

        visited[start_x][start_y] = True
        visited[start_x + 1][start_y] = True
        visited[start_x + 2][start_y] = True

        visited[start_x + 2][start_y + 1] = True
        visited[start_x + 2][start_y + 2] = True
        visited[start_x + 3][start_y + 2] = True
        visited[start_x + 4][start_y + 2] = True

        # alocate 2 in 11 blocks

        visited[start_x][start_y + 4] = True
        visited[start_x][start_y + 5] = True
        visited[start_x][start_y + 6] = True
        visited[start_x + 1][start_y + 6] = True
        visited[start_x + 2][start_y + 4] = True
        visited[start_x + 2][start_y + 5] = True
        visited[start_x + 2][start_y + 6] = True
        visited[start_x + 3][start_y + 4] = True
        visited[start_x + 4][start_y + 4] = True
        visited[start_x + 4][start_y + 5] = True
        visited[start_x + 4][start_y + 6] = True

    def create_other_paths(self):
        if (self.width <= 3 and self.height <= 2):
            t_r = 50
        elif (self.width > 20 or self.height > 20):
            t_r = 8
        else:
            t_r = 0
        for _ in range(self.width + self.height + t_r):
            d = random.choice([self.N, self.W, self.E, self.S])
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)

            if (x, y) in self.forbidden_coordinates:
                continue

            next_x = x + self.directions[d][0]
            next_y = y + self.directions[d][1]

            if (next_x, next_y) in self.forbidden_coordinates:
                continue

            if 0 <= next_x < self.height and 0 <= next_y < self.width:
                self.maze[x][y] &= ~(1 << d)
                self.maze[next_x][next_y] &=\
                    ~(1 << self.oposite[d])

    def generate_maze_dfs(self, from_regenarate: bool = False) -> None:
        if self.seed is not None:
            random.seed(self.seed)
        visited = [[False for _ in
                    range(self.width)] for _ in range(self.height)]
        self.allocate_irea_for_print(visited, from_regenarate)

        def creat_path(x: int, y: int):

            visited[x][y] = True
            directs = [d for d in self.directions.keys()]
            random.shuffle(directs)

            for direct in directs:

                next_x = (x + self.directions[direct][0])
                next_y = (y + self.directions[direct][1])

                if (0 <= next_x < self.height) and (0 <= next_y < self.width)\
                        and not visited[next_x][next_y]:

                    self.maze[x][y] &= ~(1 << direct)
                    self.maze[next_x][next_y] &= ~(1 << self.oposite[direct])
                    creat_path(next_x, next_y)

        creat_path(self.entry[0], self.entry[1])
        if not self.perfect:
            self.create_other_paths()

    def generate_maze_prims(self, from_regenarate: bool = False) -> None:
        if self.seed is not None:
            random.seed(self.seed)

        visited = [[False for _ in range(self.width)]
                   for _ in range(self.height)]

        self.allocate_irea_for_print(visited, from_regenarate)

        wall = []
        x, y = self.entry
        visited[x][y] = True

        for dir, (dx, dy) in self.directions.items():
            next_x, next_y = x + dx, y + dy
            if 0 <= next_x < self.height and 0 <= next_y < self.width:
                wall.append((x, y, dir))

        while (wall):
            x, y, d_wall = wall.pop(random.randint(0, len(wall) - 1))
            next_x = x + self.directions[d_wall][0]
            next_y = y + self.directions[d_wall][1]

            if not visited[next_x][next_y]:
                self.maze[x][y] &= ~(1 << d_wall)
                self.maze[next_x][next_y] &= ~(1 << self.oposite[d_wall])
                visited[next_x][next_y] = True

                for dir, (dx, dy) in self.directions.items():
                    nex_next_x = next_x + dx
                    nex_next_y = next_y + dy

                    if 0 <= nex_next_x < self.height\
                            and 0 <= nex_next_y < self.width:
                        if not visited[nex_next_x][nex_next_y]:
                            wall.append((next_x, next_y, dir))
        if not self.perfect:
            self.create_other_paths()

    def generate_maze(self, from_regenarate: bool = False):
        if self.algo.lower() == "dfs":
            self.generate_maze_dfs(from_regenarate)
        else:
            self.generate_maze_prims(from_regenarate)

    def re_import_with_new_maze(self):
        self.maze = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]

        self.generate_maze(True)
        self.import_maze()

    def solve_the_maze(self) -> str:
        visited = [[False for _
                    in range(self.width)] for _ in range(self.height)]

        queue: deque[Tuple[int, int, str]] = deque()
        queue.append((self.entry[0], self.entry[1], ""))
        visited[self.entry[0]][self.entry[1]] = True

        while (queue):
            x, y, path = queue.popleft()
            if (x, y) == self.exit:
                return path
            for d, (d_x, d_y) in self.directions.items():
                next_x, next_y = x + d_x, y + d_y
                if 0 <= next_x < self.height and 0 <= next_y < self.width:
                    if (not self.maze[x][y] & (1 << d)) and\
                       (not visited[next_x][next_y]):

                        visited[next_x][next_y] = True
                        queue.append((next_x, next_y, path + "NESW"[d]))
        return ""

    def get_selected_solution(self, type: int) -> Union[list, str]:
        solutions = self.solve_all_paths()

        if type == self.type_solving["Closer"]:
            return min(solutions, key=len)
        elif type == self.type_solving["Farther"]:
            return max(solutions, key=len)
        elif type == self.type_solving["All"]:
            return solutions
        return self.solve_the_maze()

    class stop_rec(Exception):
        pass

    def solve_all_paths(self) -> list:
        visited = [[False for _ in range(self.width)]
                   for _ in range(self.height)]
        all_paths: list[str] = []

        def track_current_path(x: int, y: int, path: str) -> None:
            if len(all_paths) >= 3:
                raise self.stop_rec
            visited[x][y] = True
            if (x, y) == self.exit:
                all_paths.append(path)
                visited[x][y] = False
                return

            for d, (d_x, d_y) in self.directions.items():
                next_x = x + d_x
                next_y = y + d_y

                if 0 <= next_x < self.height and 0 <= next_y < self.width:
                    if not (self.maze[x][y] & (1 << d))\
                       and not visited[next_x][next_y]:
                        track_current_path(next_x, next_y, path + "NESW"[d])
            visited[x][y] = False
        try:
            track_current_path(self.entry[0], self.entry[1], "")
        except self.stop_rec:
            pass
        return all_paths

    def import_maze(self) -> bool:
        solution = self.solve_the_maze()
        try:
            with open(self.output_file, "w") as f:
                for row in self.maze:
                    line = "".join(f"{block:X}" for block in row) + "\n"
                    f.write(line)
                f.write("\n")
                f.write(f"{self.entry[0]},{self.entry[1]}\n")
                f.write(f"{self.exit[0]},{self.exit[1]}\n")
                f.write(solution + "\n")
                return True
        except Exception:
            print("ERROR: can not load file output")
            return False

# v10
# maze = MazeGenerator(27, 37, (0,0), (36,26), "ouht", False, None, "primes")
# maze.generate_maze()
# print(maze.get_selected_solution(2))
