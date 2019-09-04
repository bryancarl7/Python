# Python Repo
The single python files are simple scripts, the folders are full-fledged applets. It's mostly just a dump folder for scripts and stuff that I might want whenever I begin with a new system.

## Scripts

### Path.py
Lists all the files by size given a directory and a csv file to print to.

"Usage: python3 path.py <directory_to_list_from> <csv_file_to_print_to>"

ex:
`python3 path.py ../lists file_list.csv`

### Specs.py
Lists system information when run on any computer. This factors out some functionality from path.py, but they're both useful. You can simplye run the command:

`python3 specs.py`

And it will give you a small prompt with your system information and then ask if you would like a report of your largest files. 

## Applets

### Sudoku Solver
A python implementation for a sudoku solver. All the boards are represented properly in the boards folder. Just simply pick the board of your choosing and run the program! The harder puzzles take a little longer, but they are all solvable


### Five-Twelve
A psuedo implementation of the classic tile game 2048. It is run by executing the game engine. Unfortunately you must click on the window for the game to start, but after that you can navigate the game simply with just arrows.

--- Each Folder will have its own README with proper documentation for execution ---
