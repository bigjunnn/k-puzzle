import sys
import time

from random import shuffle
import heapq

## A* STAR ALGORITHM WITH NO. OF MISPLACED TILES HEURISTIC ##


class Node:
    def __eq__(self, other):
        return self.init_state == other.init_state

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        hashable = tuple(map(tuple, self.init_state))
        return hash(hashable)

    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.zero_x_coord = -1
        self.zero_y_coord = -1
        self.parentPuzzle = None
        self.action = None
        self.cost = 0

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


class Puzzle(object):
    actions = []
    goalActions = []
    visited = 0
    added_to_frontier = 0
    popped = 0

    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.parentPuzzle = None
        self.action = None
        self.cost = 0

    def solve(self):
        VISITED = set()
        FRONTIER = []

        source_node = Node(init_state, goal_state)
        zero_x, zero_y = Puzzle.findZeroDimension(source_node)
        source_node.setParams(zero_x, zero_y, None, None, 0)

        if Puzzle.isSolvable(source_node):

            heapq.heappush(
                FRONTIER, (Puzzle.f_score(source_node), source_node))

            while len(FRONTIER) != 0:

                curr = heapq.heappop(FRONTIER)
                currNode = curr[1]
                Puzzle.popped += 1
                VISITED.add(currNode)

                if currNode.isGoalState():
                    return recursiveBacktrack(currNode)
                else:
                    possible_actions = self.findPossibleActions(
                        currNode.zero_x_coord, currNode.zero_y_coord)
                    shuffle(possible_actions)

                    for next_action in possible_actions:
                        child_state, child_x, child_y = self.apply_action_to_state(
                            currNode.init_state, next_action, currNode.zero_x_coord, currNode.zero_y_coord)
                        child_node = Node(child_state, goal_state)

                        if child_node not in VISITED:
                            child_node.setParams(
                                child_x, child_y, next_action, currNode, currNode.cost + 1)

                            fvalue = Puzzle.f_score(child_node)
                            heapq.heappush(FRONTIER, (fvalue, child_node))
                            Puzzle.added_to_frontier += 1
        else:
            return ['UNSOLVABLE']

    @staticmethod
    def numOfMisplaced(inputNode):
        count = 0
        gridSize = len(inputNode.init_state)
        current = inputNode.init_state
        goal = inputNode.goal_state
        for i in range(0, gridSize):
            for j in range(0, gridSize):
                if current[i][j] != current[i][j] and goal[i][j] != 0:
                    count += 1

        return count

    @staticmethod
    def f_score(inputNode):
        return inputNode.cost + Puzzle.numOfMisplaced(inputNode)

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

    @staticmethod
    def apply_action_to_state(prev_state, action, col, row):
        if action is None:
            return prev_state, col, row
        else:
            new_arr = [x[:] for x in prev_state]
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
    @staticmethod
    def calculateInversions(inputNode):
        # Flatten array for easier computation
        flat_arr = []
        for i in range(0, len(inputNode.init_state)):
            for j in range(0, len(inputNode.init_state)):
                flat_arr.append(inputNode.init_state[i][j])

        inversion_count = 0

        # Loop through flat array and compare numbers in pairs
        for i in range(0, len(flat_arr)):
            for j in range(i + 1, len(flat_arr)):
                if flat_arr[i] == 0 or flat_arr[j] == 0:
                    continue
                elif flat_arr[i] > flat_arr[j]:
                    inversion_count += 1

        return inversion_count

    @staticmethod
    def findZeroPos(inputNode):
        for row in range(0, len(inputNode.init_state)):
            for col in range(0, len(inputNode.init_state)):
                if inputNode.init_state[row][col] == 0:
                    return len(inputNode.init_state) - row

    @staticmethod
    def findZeroDimension(inputNode):
        for row in range(0, len(inputNode.init_state)):
            for col in range(0, len(inputNode.init_state)):
                if inputNode.init_state[row][col] == 0:
                    return col, row

    @staticmethod
    def isSolvable(inputNode):
        selfLen = len(inputNode.init_state)
        inversion_number = Puzzle.calculateInversions(inputNode)

        if selfLen % 2 != 0:
            if inversion_number % 2 == 0:
                return True
            else:
                return False
        else:
            zeroPos = Puzzle.findZeroPos(inputNode)
            if zeroPos % 2 == 0 and inversion_number % 2 != 0:
                return True
            elif zeroPos % 2 != 0 and inversion_number % 2 == 0:
                return True
            else:
                return False


def recursiveBacktrack(goalNode):
    currNode = goalNode
    output = []
    while(currNode.parentPuzzle is not None):
        action = ""
        if (currNode.action == "UP"):
            action = "DOWN"
        elif (currNode.action == "DOWN"):
            action = "UP"
        elif (currNode.action == "LEFT"):
            action = "RIGHT"
        else:
            action = "LEFT"
        output.append(action)
        currNode = currNode.parentPuzzle
    output.reverse()
    return output


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

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer + '\n')