import copy
import sys
import time
import numpy as np

from collections import deque
from random import shuffle
import heapq
import experiment_jw_astar_manhat

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]

    i, j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number, base=10)
            if 0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i - 1) // n][(i - 1) % n] = i
    goal_state[n - 1][n - 1] = 0

    # experiment_jw_astar_manhat(f, "output_astar_mahat")

    puzzle = experiment_jw_astar_manhat.Puzzle(init_state, goal_state)
    tic = time.time()
    ans = puzzle.solve()
    toc = time.time()
    print("Found solution in " + str(toc - tic) + " seconds")
    print("Time - No. nodes added to frontier: " + str(puzzle.added_to_frontier))
    print("Space - Max frontier size: " + str(puzzle.max_frontier))
    print("Size of solution: " + str(len(ans)))

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer + '\n')

