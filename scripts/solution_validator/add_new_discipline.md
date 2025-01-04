### Adding a new discipline

1. Clone cubing.js
2. Run `bun cubing.js/src/bin/puzzle-geometry-bin.ts --ksolve --allmoves --rotations [twsearch_puzzle] > [vscubing_puzzle].tws` (for [twsearch_puzzle] examples refer to [the first lines of files in this directory](https://github.com/cubing/twsearch/tree/main/samples/main), e.g. 3x3x3) to generate a puzzle definition like `3by3.tws` and put it into this directory
3. Run `python3 -m scripts.solution_validator.generate_valid_states [vscubing_puzzle]` (ex. for `[vscubing_puzzle]`: 3by3) to generate all 24 valid states for the new puzzle
