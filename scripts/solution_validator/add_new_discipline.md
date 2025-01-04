### Adding a new discipline

1. Clone cubing.js
2. Run `bun cubing.js/src/bin/puzzle-geometry-bin.ts --ksolve --allmoves --rotations [twsearch_puzzle] > [vscubing_puzzle].tws` to generate a puzzle definition like `3by3.tws` and put it into this directory
3. Run `python3 -m scripts.solution_validator.generate_valid_states [vscubing_puzzle]` to generate all 24 valid states for the new puzzle
4. Add necessary moves preprocessing
 
NOTE:
    - `[twsearch_puzzle]`: `3x3x3`, `2x2x2` etc, for more examples refer to [the first lines of files in this directory](https://github.com/cubing/twsearch/tree/main/samples/main), e.g. 3x3x3
    - `[vscubing_puzzle]`: `3by3`, `2by2` etc
