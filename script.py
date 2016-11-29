import argparse
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

ON = 255
OFF = 0
vals = [ON, OFF]


def random_grid(N):
    '''Returns a grid of NxN random {0, 255} values.'''
    return np.random.choice(vals, N * N, p=[0.2, 0.8]).reshape(N, N)


def add_glider(i, j, grid):
    '''Adds a glider with top-left cell at (i, j) on grid.'''
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i + 3, j:j + 3] = glider


def add_gosper(i, j, grid):
    base = np.zeros(11 * 38).reshape(11, 38)
    base[5:7, 1:3] = np.array([[255, 255], [255, 255]])
    base[3:10, 11:19] = np.array([[0, 0, 255, 255, 0, 0, 0, 0],
                                  [0, 255, 0, 0, 0, 255, 0, 0],
                                  [255, 0, 0, 0, 0, 0, 255, 0],
                                  [255, 0, 0, 0, 255, 0, 255, 255],
                                  [255, 0, 0, 0, 0, 0, 255, 0],
                                  [0, 255, 0, 0, 0, 255, 0, 0],
                                  [0, 0, 255, 255, 0, 0, 0, 0]
                                  ])
    base[1:8, 21:26] = np.array([[0, 0, 0, 0, 255],
                                 [0, 0, 255, 0, 255],
                                 [255, 255, 0, 0, 0],
                                 [255, 255, 0, 0, 0],
                                 [255, 255, 0, 0, 0],
                                 [0, 0, 255, 0, 255],
                                 [0, 0, 0, 0, 255]
                                 ])
    base[3:5, 35:37] = np.array([[255, 255], [255, 255]])
    grid[i:i + 11, j:j + 38] = base


def create_grid(args):
    grid = np.array([])
    if args.glider:
        grid = np.zeros(args.N * args.N).reshape(args.N, args.N)
        add_glider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(args.N * args.N).reshape(args.N, args.N)
        add_gosper(1, 1, grid)
    elif args.patternfile:
        f = open(args.patternfile, 'r').readlines()
        args.N = int(f[0].strip('\n'))
        grid = np.zeros(args.N * args.N).reshape(args.N, args.N)
        pattern = [line.strip('\n').split(' ') for line in f[1:]]
        grid[:] = pattern[:]
    else:
        grid = random_grid(args.N)
    return grid, args


def update(frame_num, img, grid, N):
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            # calculate the 8-neighbor sum using toroidal boundary conditions
            neighbors = [(x, y)
                         for x in [(i - 1) % N, i, (i + 1) % N]
                         for y in [(j - 1) % N, j, (j + 1) % N]
                         if (x, y) != (i, j)]
            total = int(sum(grid[x, y] for x, y in neighbors) / ON)
            if grid[i, j] == ON and ((total < 2) or (total > 3)):
                new_grid[i, j] = OFF
            elif grid[i, j] == OFF and total == 3:
                new_grid[i, j] = ON
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img


def parse_shell():
    desc = "Runs Conway's Game of Life simulation"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--grid-size', dest='N', default=100, type=int,
                        choices=range(9, 1000), required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='inter', default=50, type=int,
                        required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    parser.add_argument('--pattern-file', dest='patternfile', required=False)
    return parser.parse_args()


def main():
    args = parse_shell()
    grid, args = create_grid(args)
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    anim = animation.FuncAnimation(fig, update, fargs=(img, grid, args.N),
                                   frames=10, interval=args.inter,
                                   save_count=50)
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show()

if __name__ == "__main__":
    main()
