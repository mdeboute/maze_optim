# Maze

This is a programming project about generation and labyrinth tour. There are 3 main files :
+ `solution_generate.py` for generate a labyrinth,
+ `solution_shortest.py` for calculate a shorter path,
+ `solution_visit.py` for making * visits * (without visibility of the complete labyrinth).

Each of these files can be run from the command line, and
the `-h` or` --help` option gives usable options. For example,

`python3 solution_generate.py --help`

displays

```
usage: Generate a labyrinth of given size [-h] [-o FILE] [--slow] [-s]
                                          [-d DRAW] [-r X]
                                          n m

positional arguments:
  n                     Number of columns of the labyrinth
  m                     Number of rows of the labyrinth

optional arguments:
  -h, --help            show this help message and exit
  -o FILE               File to save the result
  --slow                Use the slow algorithm for checking connected
                        components
  -s, --show            Show the result in compact form
  -d DRAW, --draw DRAW  Draw the result in an image with this filename
  -r X                  Remove X random walls from the labyrinth
```

The option to draw to a file requires `wand` (based on
ImageMagick, more information
[on their page] (https://docs.wand-py.org/)). Viewing visits
in the terminal is not guaranteed to work under Windows.
