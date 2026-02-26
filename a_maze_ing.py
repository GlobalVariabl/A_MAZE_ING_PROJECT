import sys
from cls_generator import MazeGenerator
import random
from vvsual import to_start

def parse_config_file(file_name: str) -> dict:
    redict = {}
    try:
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                if "=" not in line:
                    raise ValueError(f"the line ({line}) is not valid")
                key, value = line.split("=", 1)
                redict[key.strip().upper()] = value.strip()
    except ValueError as e:
        print("ERROR:", e)
        return None
    return redict


def get_location(string_loc: str) -> tuple:
    try:
        x, y = string_loc.split(",", 1)
        return (int(x), int(y))
    except Exception:
        raise ValueError("invalid location value")


def check_locations_within_eria(location: tuple, wigth: int,
                                height: int) -> bool:
    if 0 <= location[0] < wigth and 0 <= location[1] < height:
        return (True)
    return (False)


def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    configs = parse_config_file(sys.argv[1])

    try:
        wigth = int(configs["WIDTH"])
        height = int(configs["HEIGHT"])
        entry = get_location(configs["ENTRY"])
        exit_ = get_location(configs["EXIT"])
        output_file = configs["OUTPUT_FILE"]
        perfect = (configs.get("PERFECT", "true").lower() == "true")
        seed = int(configs["SEED"]) if "SEED" in configs else None
        if seed is not None:
            random.seed(seed)


        if not check_locations_within_eria(entry, wigth, height):
            print("ENTRY point is outsid of the maze")
            sys.exit(1)
        if not check_locations_within_eria(exit_, wigth, height):
            print("EXIT point is outsid of the maze")
            sys.exit(1)
        if entry == exit_:
            print("ENTRY and EXIT points can not be the same point")
            sys.exit(0)
        maze = MazeGenerator(wigth, height, entry, exit_, output_file, perfect)
        maze.generate_maze()
        maze.import_maze()
        to_start(maze)

    except ValueError as e:
        print(f"EROOR: invalid value in config ({e})")
    except KeyError:
        print("ERROR: there is not key in configfile")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
