import copy
import sys
import time
import numpy as np

from collections import deque
from random import shuffle
import heapq

## A* STAR ALGORITHM WITH MISPLACED TILES AS HEURISTIC ##


class Puzzle(object):
    actions = []
    goalActions = []
    visited = 0
    added_to_frontier = 0 # reflective of time complexity
    popped = 0
    max_frontier = 0  # reflective of space complexity

    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.isSourcePuzzle = False
        self.zero_x_coord = -1
        self.zero_y_coord = -1
        self.parentPuzzle = None
        self.action = None
        self.cost = 0

    def __eq__(self, other):
        return self.init_state == other.init_state

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        hashable = tuple(map(tuple, self.init_state))
        return hash(hashable)

    def setParentPuzzle(self, parPuzzle):
        self.parentPuzzle = parPuzzle

    def isGoalState(self):
        return self.init_state == self.goal_state

    def setParams(self, blank_x, blank_y, action_done, parent_puzzle, new_cost):
        self.zero_x_coord = blank_x
        self.zero_y_coord = blank_y
        self.parentPuzzle = parent_puzzle
        self.action = action_done
        self.cost = new_cost

    def solve(self):
        VISITED = set()
        FRONTIER = []

        source_puzzle = Puzzle(init_state, goal_state)
        zero_x, zero_y = source_puzzle.findZeroDimension()
        source_puzzle.setParams(zero_x, zero_y, None, None, 0)

        if source_puzzle.isSolvable():

            heapq.heappush(FRONTIER, (source_puzzle.f_score(), source_puzzle))

            while len(FRONTIER) != 0:

                puzzleTuple = heapq.heappop(FRONTIER)
                currentPuzzle = puzzleTuple[1]
                Puzzle.popped += 1
                VISITED.add(currentPuzzle)

                if currentPuzzle.isGoalState():
                    return self.recursiveBacktrack(currentPuzzle)
                else:
                    possible_actions = self.findPossibleActions(
                        currentPuzzle.zero_x_coord, currentPuzzle.zero_y_coord)
                    shuffle(possible_actions)

                    for next_action in possible_actions:
                        child_state, child_x, child_y = self.apply_action_to_state(
                            currentPuzzle.init_state, next_action, currentPuzzle.zero_x_coord, currentPuzzle.zero_y_coord)
                        child_puzzle = Puzzle(child_state, goal_state)

                        if child_puzzle not in VISITED:
                            child_puzzle.setParams(
                                child_x, child_y, next_action, currentPuzzle, currentPuzzle.cost + 1)

                            fvalue = child_puzzle.f_score()
                            heapq.heappush(FRONTIER, (fvalue, child_puzzle))
                            Puzzle.added_to_frontier += 1

                            # For space complexity
                            if len(FRONTIER) > Puzzle.max_frontier:
                                Puzzle.max_frontier = len(FRONTIER)
        else:
            return ['UNSOLVABLE']

    def recursiveBacktrack(self, goalPuzzle):
        currPuzzle = goalPuzzle
        output = []
        while(currPuzzle.parentPuzzle is not None):
            action = ""
            if (currPuzzle.action == "UP"):
                action = "DOWN"
            elif (currPuzzle.action == "DOWN"):
                action = "UP"
            elif (currPuzzle.action == "LEFT"):
                action = "RIGHT"
            else:
                action = "LEFT"
            output.append(action)
            currPuzzle = currPuzzle.parentPuzzle
        output.reverse()
        return output

    def numOfMisplaced(self):
        count = 0
        gridSize = len(self.init_state)
        current = self.init_state
        goal = self.goal_state
        for i in range(0, gridSize):
            for j in range(0, gridSize):
                if current[i][j] != current[i][j] and goal[i][j] != 0:
                    count += 1

        return count

    def f_score(self):
        return self.cost + self.numOfMisplaced()

    def findPossibleActions(self, x, y):
        max_y_row = len(self.goal_state) - 1
        max_x_col = len(self.goal_state[0]) - 1
        output = []

        if y + 1 <= max_y_row:
            output.append("DOWN")
        if x + 1 <= max_x_col:
            output.append("RIGHT")
        if y - 1 >= 0:
            output.append("UP")
        if x - 1 >= 0:
            output.append("LEFT")
        return output

    def apply_action_to_state(self, prev_state, action, col, row):
        if action is None:
            return prev_state, col, row
        else:
            new_arr = y = [row[:] for row in prev_state]
            new_col = col
            new_row = row

            # Defines the possible movements and returns an array representing the movement
            if action == "RIGHT":
                new_arr[row][col] = new_arr[row][col + 1]
                new_arr[row][col + 1] = 0
                new_col = col + 1

            elif action == "LEFT":
                new_arr[row][col] = new_arr[row][col - 1]
                new_arr[row][col - 1] = 0
                new_col = col - 1

            elif action == "UP":
                new_arr[row][col] = new_arr[row - 1][col]
                new_arr[row - 1][col] = 0
                new_row = row - 1

            elif action == "DOWN":
                new_arr[row][col] = new_arr[row + 1][col]
                new_arr[row + 1][col] = 0
                new_row = row + 1
            return new_arr, new_col, new_row

    # Helper method to calculate the permutation inversions in initial state
    def calculateInversions(self):
        # Flatten array for easier computation
        flat_arr = []
        for i in range(0, len(self.init_state)):
            for j in range(0, len(self.init_state)):
                flat_arr.append(self.init_state[i][j])

        inversion_count = 0

        # Loop through flat array and compare numbers in pairs
        for i in range(0, len(flat_arr)):
            for j in range(i + 1, len(flat_arr)):
                if flat_arr[i] == 0 or flat_arr[j] == 0:
                    continue
                elif flat_arr[i] > flat_arr[j]:
                    inversion_count += 1

        return inversion_count

    def findZeroPos(self):
        for row in range(0, len(self.init_state)):
            for col in range(0, len(self.init_state)):
                if self.init_state[row][col] == 0:
                    return len(self.init_state) - row

    def findZeroDimension(self):
        for row in range(0, len(self.init_state)):
            for col in range(0, len(self.init_state)):
                if self.init_state[row][col] == 0:
                    return col, row

    def isSolvable(self):
        selfLen = len(self.init_state)
        inversion_number = self.calculateInversions()

        if selfLen % 2 != 0:
            if inversion_number % 2 == 0:
                return True
            else:
                return False
        else:
            zeroPos = self.findZeroPos()
            if zeroPos % 2 == 0 and inversion_number % 2 != 0:
                return True
            elif zeroPos % 2 != 0 and inversion_number % 2 == 0:
                return True
            else:
                return False


if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
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

    puzzle = Puzzle(init_state, goal_state)
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
