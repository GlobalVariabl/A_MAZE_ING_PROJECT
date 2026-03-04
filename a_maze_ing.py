import sys
from cls_generator import MazeGenerator
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
    if 0 <= location[0] < height and 0 <= location[1] < wigth:
        return (True)
    return (False)


def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    configs = parse_config_file(sys.argv[1])
    if configs is None:
        sys.exit(1)

    try:
        current_key = "WIDTH"
        width = int(configs["WIDTH"])
        current_key = "HEIGHT"
        height = int(configs["HEIGHT"])
        current_key = "ENTRY"
        entry = get_location(configs["ENTRY"])
        current_key = "EXIT"
        exit_ = get_location(configs["EXIT"])
        current_key = "OUTPUT_FILE"
        output_file = configs["OUTPUT_FILE"]
        current_key = "PERFECT"
        perfect = (configs.get("PERFECT", "true").lower() == "true")
        current_key = "SEED"
        seed = int(configs["SEED"]) if "SEED" in configs else None
        current_key = "ALGO"
        algo = configs["ALGO"] if "ALGO" in configs else None

        if width <= 0 or height <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive integers")
        if not check_locations_within_eria(entry, width, height):
            print("ENTRY point is outsid of the maze")
            sys.exit(1)
        if not check_locations_within_eria(exit_, width, height):
            print("EXIT point is outsid of the maze")
            sys.exit(1)
        if entry == exit_:
            print("ENTRY and EXIT points can not be the same point")
            sys.exit(0)
        maze = MazeGenerator(width, height, entry, exit_, output_file,
                             perfect, seed, algo)
        maze.generate_maze()
        if not maze.import_maze():
            sys.exit(1)
        to_start(maze)

    except ValueError as e:
        print(f"ERROR: invalid value in config :({e})")
    except KeyError:
        print(f"ERROR: there is not {current_key} key in configfile")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
#v10