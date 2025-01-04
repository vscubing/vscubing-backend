import re
from .generate_valid_states import get_state_after_moves, get_valid_states
from time import perf_counter


def is_solution_valid(scramble, solution, discipline):
    solution = _remove_comments(solution)
    moves = f"{scramble} {solution}"
    moves = _preprocess_moves(moves)

    state = get_state_after_moves(moves=moves, discipline=discipline)
    return state in get_valid_states(discipline=discipline)


def _remove_comments(moves):
    return re.sub(r"\/\*\d+?\*\/", "", moves)


def _preprocess_moves(moves):
    moves = moves.replace("M", "2L")
    moves = moves.replace("S", "2F")
    moves = moves.replace("E", "2D")
    moves = moves.replace("Rw'", "R' 2L")
    moves = moves.replace("Rw", "R 2L'")
    moves = moves.replace("Lw'", "L' 2L'")
    moves = moves.replace("Lw", "L 2L")
    moves = moves.replace("Uw'", "U' 2D")
    moves = moves.replace("Uw", "U 2D'")
    moves = moves.replace("Dw'", "D' 2D'")
    moves = moves.replace("Dw", "D 2D")
    return moves


if __name__ == "__main__":
    scramble = ""
    solution = (
        "R L S' D' L y x' y' x' U' L U R' D' E D L R' L R' L' R U' y x' y' D U' D L U R' M M U R' U' L U R' L D' D U L R L' R' L R D' x' y y' M M R' U R' L E' S E' S S' S E E' S E L R' L U' F' F y' y M' M' Dw M' Uw' Lw x' Rw' Uw x' x' y y x' y' x x' y' y y y' y' D R R x x' D U F R' F F D' U' y y' U R' F R F' y' U' L' U' L y y y' y' R U' R' y y' y U' R' U R U x x' M' M' U U M' M' U U U' R U' R' U y' R' U R R U' R' U' R U R' U U R U' R' U' R' U' R U' R' U R U B' B R B' R' B U U U U' U F' U U' F U U' F' U' F R R Uw R' U R U' R Uw' R R U "
        * 1000
    )
    time_start = perf_counter()

    print(is_solution_valid(scramble=scramble, solution=solution, discipline="3by3"))

    time_duration = perf_counter() - time_start
    print(f"Took {time_duration:.3f} seconds")
