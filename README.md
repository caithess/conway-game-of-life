# Conway Game of Life

An implementation of Conway's Game of Life cellular automaton. Meant to be run via command line. 

Defaults to starting with a _NxN_ random grid of either `0` or `255`.

## Flags

```bash
# Grid of size N x N. Default Value: 100. Allowed: 9-999
--grid-size
# If you want to save 10 frames of the simulation to a file
--mov-file
# Animation update interval in milliseconds. Default: 50. 
--interval
# If you want to start with a glider in top-left corner
--glider
# If you want to start with a Gosper Gun in top-left corner
--gosper
# If you want to start the simulation from a set pattern .txt file
--pattern-file
```

## Sample Pattern File

Requires N as first line of file

```
8
0 0 0 255 0 0 0 255
0 0 0 255 0 0 0 255
0 0 0 255 0 0 0 255
0 0 0 255 0 0 0 255
0 0 0 255 0 0 0 255
0 0 0 255 0 0 0 255
0 0 0 255 0 0 0 255
0 0 0 255 0 0 0 255
```

![](https://github.com/caithess/conway-game-of-life/blob/master/conway_example.gif)
