import subprocess
import csv
import sys


def get_state_after_moves(moves, discipline):
    cmd = [
        "./vendor/twsearch/build/bin/twsearch",
        "--showmoves",
        "--quiet",
        f"./scripts/solution_validator/{discipline}.tws",
    ]
    return subprocess.run(
        args=cmd, input=moves, capture_output=True, text=True
    ).stdout.strip("\n")


def get_valid_states(discipline):
    with open(f"./scripts/solution_validator/{discipline}_valid_states.csv") as file:
        reader = csv.reader(file, quoting=csv.QUOTE_ALL)
        return next(reader)


def generate_valid_states(discipline):
    valid_states = []
    for face in ["", "x", "x'", "z", "z'", "z2"]:
        for orientation in ["", "y", "y'", "y2"]:
            valid_states.append(
                get_state_after_moves(
                    moves=f"{face} {orientation}", discipline=discipline
                )
            )

    with open(
        f"./scripts/solution_validator/{discipline}_valid_states.csv",
        "w",
    ) as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(valid_states)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Please provide a discipline name")
    discipline = sys.argv[1]
    generate_valid_states(discipline=discipline)
