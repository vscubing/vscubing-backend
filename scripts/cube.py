from rubik.cube import Cube
import time
import re


class ReconstructionValidator:
    def __init__(self, scramble, reconstruction):
        self.start_time = time.time()
        self.cube = Cube("WWWWWWWWWOOOGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBYYYYYYYYY")

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
        self.cube.sequence(move_sequence)


if __name__ == '__main__':

    # scramble = "U L' B2"
    # reconstruction = "S/*0*/ E'/*121*/ S'/*336*/ E/*424*/ S/*1044*/ E'/*1228*/ x'/*1946*/ M/*2160*/ E/*3103*/ S'/*3328*/ z'/*4640*/ B/*4817*/ L'/*5060*/ Lw'/*5500*/ x/*5993*/ x/*6336*/ x/*6620*/ Rw/*6928*/ B'/*7205*/ z/*7456*/ y/*8528*/ D'/*8808*/ Rw'/*9068*/ U/*9336*/ F/*9592*/ F'/*9865*/ F'/*10093*/ U'/*10340*/ L/*10648*/ D/*10905*/ y'/*11137*/ Dw/*11356*/ M'/*11584*/ Uw'/*11817*/ Lw/*12072*/ x'/*12524*/ x'/*12797*/ x'/*13137*/ x'/*13349*/ Uw/*13708*/ Uw/*13985*/ Uw/*14084*/ x/*14288*/ Dw'/*14936*/ Dw/*16485*/ x'/*20212*/ x'/*21105*/ y'/*21408*/ y'/*21656*/ y'/*22284*/ x'/*22905*/ y'/*23240*/ y/*23717*/ y'/*23879*/ y'/*24148*/ y/*24608*/ F/*25007*/ F/*25172*/ R'/*25472*/ U/*26048*/ y/*26368*/ U'/*26388*/ U'/*26608*/ R'/*26981*/ R'/*27139*/ y'/*27449*/ U/*27908*/ R'/*28077*/ F/*28277*/ R/*28380*/ U'/*29420*/ R'/*29780*/ U'/*29924*/ R/*30032*/ y/*30220*/ U/*30469*/ L/*30637*/ U/*30840*/ L'/*31037*/ y/*32308*/ y'/*32677*/ R'/*32944*/ U'/*33124*/ R/*33265*/ y/*33348*/ U'/*33503*/ y'/*33812*/ U/*33900*/ U/*34088*/ y/*34228*/ L/*34552*/ U/*34740*/ L'/*34888*/ R/*36240*/ U'/*36412*/ R'/*36531*/ y/*36916*/ L/*37249*/ U/*37425*/ L'/*37559*/ y'/*37828*/ U/*38321*/ U'/*39076*/ F'/*39400*/ R/*39670*/ U/*39848*/ R'/*39984*/ U'/*40136*/ R'/*40364*/ F/*40653*/ R/*40888*/ U'/*41320*/ U'/*41783*/ U/*42108*/ R'/*42336*/ U'/*42473*/ F'/*42672*/ R/*43308*/ U/*43692*/ R'/*43840*/ U'/*43980*/ F/*44265*/ F'/*44879*/ R'/*45184*/ F/*45425*/ R/*45592*/ U'/*45960*/ U/*46340*/ R/*46508*/ U'/*46628*/ R'/*46776*/ U/*47052*/ U'/*47525*/ U/*47961*/ R/*48165*/ U/*48812*/ Rw/*49561*/ U/*49949*/ U/*50123*/ R'/*50288*/ U'/*50480*/ R/*50660*/ U'/*50806*/ Rw'/*51152*/ U'/*51780*/ U/*52033*/ U'/*52336*/ L'/*53421*/ L/*53952*/ M'/*54606*/ U'/*55108*/ M'/*55960*/ M'/*56165*/ U'/*56492*/ M'/*56796*/ M'/*57006*/ U'/*57451*/ M'/*57753*/ U'/*58025*/ U'/*58200*/ M'/*58483*/ M'/*58672*/ U'/*58921*/ U'/*59093*/"
    scramble = "U R2 D2"
    reconstruction = "D/*0*/ D/*232*/ R'/*773*/ R'/*1051*/ x'/*1744*/ x'/*2021*/ D'/*2936*/"

    v = ReconstructionValidator(scramble=scramble, reconstruction=reconstruction)
