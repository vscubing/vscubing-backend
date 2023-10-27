from rubik.cube import Cube
import time
import re


class SolveValidator:
    def __init__(self, scramble, reconstruction):
        self.start_time = time.time()
        self.cube = Cube("WWWWWWWWWOOOGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBYYYYYYYYY")
        print(self.cube)

        self.scramble = scramble
        self.reconstruction = reconstruction

        self.notation_translator = {
            "L": "L",
            "L'": "Li",
            "R": "R",
            "R'": "Ri",
            "U": "U",
            "U'": "Ui",
            "D": "D",
            "D'": "Di",
            "F": "F",
            "F'": "Fi",
            "B": "B",
            "B'": "Bi",
            "M": "M",
            "M'": "Mi",
            "E": "E",
            "E'": "Ei",
            "S": "S",
            "S'": "Si",
            "x": "X",
            "x'": "Xi",
            "y": "Y",
            "y'": "Yi",
            "z": "Z",
            "z'": "Zi",
            "Lw": "L M",
            "Lw'": "Li Mi",
            "Rw": "R Mi",
            "Rw'": "Ri M",
            "Uw": "U Ei",
            "Uw'": "Ui E",
            "Dw": "D E",
            "Dw'": "Di Ei",
            "Fw": "F S",
            "Fw'": "Fi Si",
            "Bw": "B Si",
            "Bw'": "Bi S",

        }

    def is_valid(self):
        self._scramble_cube()
        self._solve_cube()
        print(self.cube.is_solved())
        print(time.time() - self.start_time)
        return self.cube.is_solved()

    def _scramble_cube(self):
        pattern = r"/\*\d*\*/"
        self.scramble = re.sub(pattern, "", self.scramble).split()
        result = ""
        for move in self.scramble:
            if len(move) == 1:
                result += move[0] + " "
            elif move[1] == "2":
                result += move[0] + " " + move[0] + " "
            elif move[1] == "'":
                result += move + " "

        self.scramble = result.split()
        for move in self.scramble:
            move = self.notation_translator[move]
            getattr(self.cube, move)()

    def _solve_cube(self):
        pattern = r"/\*\d*\*/"
        self.reconstruction = re.sub(pattern, "", self.reconstruction).split()
        move_sequence = ""
        for move in self.reconstruction:
            move = self.notation_translator[move]
            move_sequence += move + " "
        print(move_sequence)
        self.cube.sequence(move_sequence)


if __name__ == '__main__':

    scramble = "U R L'"
    reconstruction = "Rw/*0*/ R'/*980*/ D/*2048*/ D'/*2723*/ B'/*3143*/"

    v = SolveValidator(scramble=scramble, reconstruction=reconstruction)
    print(v.is_valid())
