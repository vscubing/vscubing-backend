import random


def generate_scramble():
    moves = ["U", "D", "R", "L", "F", "B"]
    modifiers = ["", "'", "2"]
    scramble = []
    last_move = ""
    for i in range(3):
        move = random.choice(moves)
        while move == last_move:
            move = random.choice(moves)
        modifier = random.choice(modifiers)
        scramble.append(move + modifier)
        last_move = move
    return " ".join(scramble)
