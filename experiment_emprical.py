import copy
import sys
import time
import numpy as np

from collections import deque
from random import shuffle
import heapq
import random
import experiment_jw_astar_manhat
import experiment_ivan_bfs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Wrong number of arguments!")

    test_size = 10
    test_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    n = 3
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]

    # Create goal node
    for i in range(1, max_num + 1):
        goal_state[(i - 1) // n][(i - 1) % n] = i
    goal_state[n - 1][n - 1] = 0

    # Initialise Sum
    bfs_sum_popped_frontier, bfs_sum_max_frontier, bfs_sum_size, bfs_sum_time, bfs_unsolvable = 0, 0, 0, 0, 0
    # a1_sum_popped_frontier, a1_sum_max_frontier, a1_sum_size, a1_sum_time, a1_unsolvable = 0, 0, 0, 0, 0
    a2_sum_popped_frontier, a2_sum_max_frontier, a2_sum_size, a2_sum_time, a2_unsolvable = 0, 0, 0, 0, 0
    # a3_sum_popped_frontier, a3_sum_max_frontier, a3_sum_size, a3_sum_time, a3_unsolvable = 0, 0, 0, 0, 0

    # Run random test cases for test_size times
    for test_num in range(0, test_size):
        # Generate Random Test Cases
        random.shuffle(test_arr)
        i = 0
        for val in test_arr:
            init_state[i // n][i % n] = val
            i = i + 1

        # BFS
        puzzle = experiment_ivan_bfs.Puzzle(init_state, goal_state)
        tic = time.time()
        ans = puzzle.solve()
        toc = time.time()
        if ans == ['UNSOLVABLE']:
            bfs_unsolvable += 1
        else:
            bfs_sum_popped_frontier += puzzle.added_to_frontier
            bfs_sum_max_frontier += puzzle.max_frontier
            bfs_sum_size += len(ans)
            bfs_sum_time += toc - tic
        del puzzle
        """
        # A Star Heuristic 1
        puzzle = a1.Puzzle(init_state, goal_state)
        tic = time.time()
        ans = puzzle.solve()
        toc = time.time()
        if ans == ['UNSOLVABLE']:
            a1_unsolvable += 1
        else:
            a1_sum_popped_frontier += puzzle.added_to_frontier
            a1_sum_max_frontier += puzzle.max_frontier
            a1_sum_size += len(ans)
            a1_sum_time += toc - tic
        del puzzle
        """
        # A Star Heuristic 2: Manhattan Distance
        puzzle = experiment_jw_astar_manhat.Puzzle(init_state, goal_state)
        tic = time.time()
        ans = puzzle.solve()
        toc = time.time()
        if ans == ['UNSOLVABLE']:
            a2_unsolvable += 1
        else:
            a2_sum_popped_frontier += puzzle.added_to_frontier
            a2_sum_max_frontier += puzzle.max_frontier
            a2_sum_size += len(ans)
            a2_sum_time += toc - tic
        del puzzle
        """
        # A Star Heuristic 3
        puzzle = a3.Puzzle(init_state, goal_state)
        tic = time.time()
        ans = puzzle.solve()
        toc = time.time()
        if ans == ['UNSOLVABLE']:
            a3_unsolvable += 1
        else:
            a3_sum_popped_frontier += puzzle.added_to_frontier
            a3_sum_max_frontier += puzzle.max_frontier
            a3_sum_size += len(ans)
            a3_sum_time += toc - tic
        del puzzle
        """
    bfs_num_test = test_size - bfs_unsolvable
    bfs_avg_popped_frontier = bfs_sum_popped_frontier / bfs_num_test
    bfs_avg_max_frontier = bfs_sum_max_frontier / bfs_num_test
    bfs_avg_size = bfs_sum_size / bfs_num_test
    bfs_avg_time = bfs_sum_time / bfs_num_test

    a2_num_test = test_size - a2_unsolvable
    a2_avg_popped_frontier = a2_sum_popped_frontier / a2_num_test
    a2_avg_max_frontier = a2_sum_max_frontier / a2_num_test
    a2_avg_size = a2_sum_size / a2_num_test
    a2_avg_time = a2_sum_time / a2_num_test

    with open(sys.argv[1], 'a') as f:
        f.write("Number of test cases randomly generated: " + str(test_size) + '\n')
        f.write('\n')
        f.write("Search Type: Uninformed Search" + '\n')
        f.write("Algorithm Used: Breadth First Search" + '\n')
        f.write("Average number of nodes popped: " + str(bfs_avg_popped_frontier) + '\n')
        f.write("Average maximum Frontier size:  " + str(bfs_avg_max_frontier) + '\n')
        f.write("Average time taken to solve:    " + str(bfs_avg_time) + ' s\n')
        f.write("Average solution steps:         " + str(bfs_avg_size) + '\n')
        f.write("Number of unsolvable puzzles:   " + str(bfs_unsolvable) + " out of " + str(test_size) + '\n')
        f.write('\n\n')
        '''f.write("Search Type: Informed Search" + '\n')
        f.write("Algorithm Used: A* Search" + '\n')
        f.write("Heuristics 1: Number of misplaced tiles" + '\n')
        f.write("Average number of nodes popped: " + str(a1_avg_popped_frontier) + '\n')
        f.write("Average maximum Frontier size:  " + str(a1_avg_max_frontier) + '\n')
        f.write("Average time taken to solve:    " + str(a1_avg_time) + ' s\n')
        f.write("Average solution steps:         " + str(a1_avg_size) + '\n')
        f.write("Number of unsolvable puzzles:   " + str(a1_unsolvable) + " out of " + str(test_size) + '\n')
        f.write('\n\n')'''
        f.write("Search Type: Informed Search" + '\n')
        f.write("Algorithm Used: A* Search" + '\n')
        f.write("Heuristics 2: Total Manhattan Distance" + '\n')
        f.write("Average number of nodes popped: " + str(a2_avg_popped_frontier) + '\n')
        f.write("Average maximum Frontier size:  " + str(a2_avg_max_frontier) + '\n')
        f.write("Average time taken to solve:    " + str(a2_avg_time) + ' s\n')
        f.write("Average solution steps:         " + str(a2_avg_size) + '\n')
        f.write("Number of unsolvable puzzles:   " + str(a2_unsolvable) + " out of " + str(test_size) + '\n')
        '''f.write('\n\n')
        f.write("Search Type: Informed Search" + '\n')
        f.write("Algorithm Used: A* Search" + '\n')
        f.write("Heuristics 3: Total Linear Conflicts" + '\n')
        f.write("Average number of nodes popped: " + str(a3_avg_popped_frontier) + '\n')
        f.write("Average maximum Frontier size:  " + str(a3_avg_max_frontier) + '\n')
        f.write("Average time taken to solve:    " + str(a3_avg_time) + '\n')
        f.write("Average solution steps:         " + str(a3_avg_size) + '\n')
        f.write("Number of unsolvable puzzles:   " + str(a3_unsolvable) + " out of " + str(test_size) + '\n')'''