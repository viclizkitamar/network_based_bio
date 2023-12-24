flow_solver
===========

    
Using the Python version:
=========================

Make sure you have [pycosat](https://github.com/ContinuumIO/pycosat) installed. If not, try:

    pip install pycosat
    
Then, from the project root directory, try:

    ./pyflowsolver.py puzzles/jumbo_14x14_01.txt

Puzzle file format
==================

Plain-ASCII file, one line per row of puzzle. Use the following
characters to specify color:

| Letter | Color        |
|--------|--------------|
| R      | red          |
| B      | blue         |
| Y      | yellow       |
| G      | green        |
| O      | orange       |
| C      | cyan         |
| M      | magenta      |
| m      | maroon       |
| P      | purple       |
| A      | gray         |
| W      | white        |
| g      | bright green |
| T      | tan          |
| b      | dark blue    |
| c      | dark cyan    |
| p      | pink         |

Any non-alphabetical, non-newline character becomes a blank space.
Puzzle size is set by the number of characters before the first
newline.



