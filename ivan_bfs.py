import copy
import sys


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.isSourcePuzzle = False
        self.zero_x_coord = -1
        self.zero_y_coord = -1
        self.parentPuzzle = None
        self.action = None

    def setParentPuzzle(self, parPuzzle):
        self.parentPuzzle = parPuzzle

    def setIsSourcePuzzleToTrue(self):
        self.isSourcePuzzle = True

    def isGoalState(self):
        return self.init_state == self.goal_state

    def setZeroXAndY(self, blank_x, blank_y):
        self.zero_x_coord = blank_x
        self.zero_y_coord = blank_y

    def setAction(self, actionToBeDone):
        self.action = actionToBeDone

    def solve(self):
        if self.isSolvable:
            VISITED = {}
            FRONTIER = []

            source_puzzle = Puzzle(init_state, goal_state)
            source_puzzle.setParentPuzzle(None)
            zero_x, zero_y = source_puzzle.findZeroDimension()
            source_puzzle.setZeroXAndY(zero_x, zero_y)

            FRONTIER.append(source_puzzle)

            while len(FRONTIER) > 0:
                currentPuzzle = FRONTIER.pop()

                if currentPuzzle.isGoalState():
                    return ['hello']

                else:
                    possible_actions = self.findPossibleActions(currentPuzzle.zero_x_coord, currentPuzzle.zero_y_coord)
                    return ['hello']
        else:
            return ['UNSOLVABLE']

    def findPossibleActions(self, x, y):
        y_max = len(self.goal_state) - 1
        x_max = len(self.goal_state[0]) - 1
        output = []

        if y + 1 <= y_max:
            output.append("UP")
        if x + 1 <= x_max:
            output.append("RIGHT")
        if y - 1 >= 0:
            output.append("DOWN")
        if x - 1 >= 0:
            output.append("LEFT")

        return output

    def apply_action_to_state(self, prev_state, action, prev_blank_x, prev_blank_y):
        if action is None:
            return prev_state
        else:
            new_state = copy.deepcopy(prev_state)




    # you may add more functions if you think is useful
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

        n = len(self.init_state)
        inversion_number = self.calculateInversions()

        if n % 2 != 0 & inversion_number == 0:
            return True
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
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer + '\n')
