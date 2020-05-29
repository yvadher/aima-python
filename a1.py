"""
Assignment 1 file for running 8-Puzzel and finding the A* algortihym optimality

"""
import random
import time
from utils import memoize, PriorityQueue
from search import EightPuzzle, Node, Problem

class EightPuzzleGame(EightPuzzle):

    def __init__(self, initial):
        super().__init__(initial)

    def calculateMissplacedTiles(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal) if s != 0)


    def calculateManhattenDist(self,node):
        h_value = 0
        for i, number in enumerate(node.state):
            if number:
                h_value += abs((number-1)%3 - i%3) + abs((number-1)//3 - i//3)
        return h_value

    def maxH(self, node):
        return max(self.calculateManhattenDist(node), self.calculateMissplacedTiles(node))


    def display(self):
         #clousure function
        def printer(str):
            print (str, end ='')

        for index, number in enumerate(self.initial):
            printer(number) if (number != 0 ) else printer("*")
            printer("\n") if ( (index + 1) % 3 == 0 and index != 0 ) else printer(" ")

class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        leftMoveAllowed =  (1,5,8,3,4,7)
        rightMoveAllowed = (0,2,6,3,4,7)
        downMoveAllowed =  (0,1,3,4,5)
        upMoveAllowed =    (2,3,6,7,8)

        if index_blank_square not in leftMoveAllowed:
            possible_actions.remove('LEFT')
        if index_blank_square not in rightMoveAllowed:
            possible_actions.remove('RIGHT')
        if index_blank_square not in upMoveAllowed:
            possible_actions.remove('UP')
        if index_blank_square not in downMoveAllowed:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if (blank in (0,1)): delta['DOWN'] = 2
        if (blank in (2,3)): delta['UP'] = -2

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        # for it to be solvable first 3 index should have 1,2,3 only 
        validSet = (1,2,3)
        if (state[0] not in validSet or state[1] not in validSet or state[2] not in validSet):
            return None

        # find inversion for the first for indexes 
        inversionFirst = 0
        for i in range(0,3):
            for j in range(i+1, 4):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversionFirst += 1
        # find the inversion for the second block and must be even in order to be solvble
        inversionSecond = 0
        for i in range(3, len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversionSecond += 1   
        
        # # blank is the index of the blank square
        blank = self.find_blank_square(state)

        # solvable if only zero is on the first row and it has to be odd inversion for the frist block. 
        if ( blank < 2 and inversionFirst % 2 != 0):
            return inversionSecond % 2 == 0
        else:
            return (inversionFirst % 2 == 0 and inversionSecond % 2 == 0)

    def calculateMissplacedTiles(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal) if s != 0)

    def calculateManhattenDist(self,node):
        dictIndexCord     = { 0: (1,1), 1: (1,2), 2: (2,1), 3: (2,2) , 4: (2,3), 5: (2,4) , 6: (3,2), 7: (3,3), 8: (3,4)  }
        dictGoalCord = { 1: (1,1), 2: (1,2), 3: (2,1), 4: (2,2) , 5: (2,3), 6: (2,4) , 7: (3,2), 8: (3,3) }

        h_value = 0
        for i, num in enumerate(node.state):
            if (num == 0): continue
            h_value += abs( dictIndexCord[i][0] - dictGoalCord[num][0]) + abs( dictIndexCord[i][1] - dictGoalCord[num][1])
        
        return h_value

    def maxH(self, node):
        return max(self.calculateManhattenDist(node), self.calculateMissplacedTiles(node))

    def display(self, state):
        print (state[0], state[1])
        print (state[2], state[3],state[4], state[5])
        print (" ", state[6], state[7], state[8])

## below function code is from the search.py with some modification.
def astar_search(problem, h, display=False):

    h = memoize(h or problem.h, 'h')
    f = memoize(lambda n: n.path_cost + h(n), 'f')
    
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    frontierPopCount = 0
    start_time = time.time()
    while frontier:
        node = frontier.pop()
        frontierPopCount += 1
        if problem.goal_test(node.state):
            if display:
                print("Sln Length :", str(node.depth), " | removed nodes from frontier:  ", str(frontierPopCount))
                elapsed_time = time.time() - start_time
                print(f'elapsed time (in seconds): {elapsed_time}s')
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)

    print ( str(frontierPopCount) )
    return None

def display(state):

    #clousure function
    def printer(str):
        print (str, end ='')

    for index, number in enumerate(state):
        printer(number) if (number != 0 ) else printer("*")
        printer("\n") if ( (index + 1) % 3 == 0 and index != 0 ) else printer(" ")

def make_rand_8puzzle():
    while True:
        initialPuzzel = tuple(random.sample( range(0,9), 9))
        puzzel = EightPuzzleGame(initialPuzzel)
        if (puzzel.check_solvability(puzzel.initial)):
            print (initialPuzzel)
            return puzzel

    # return EightPuzzleGame((1,0,3,4,2,6,7,5,8))
    # return EightPuzzleGame( (4,1,0,7,5,3,6,8,2) )
    return EightPuzzleGame((8,2,3,4,5,6,7,1,0))

def make_rand_duckpuzzle():
    while True:
        initialPuzzel = tuple(random.sample( range(0,9), 9))
        puzzel = DuckPuzzle(initialPuzzel)
        if (puzzel.check_solvability(puzzel.initial)):
            print (initialPuzzel)
            return puzzel

def paly_the_game():
    randPuzzles = []
    for i in range(0,10):
        tempPuzzel = make_rand_8puzzle()
        randPuzzles.append(tempPuzzel)


dPuz = make_rand_duckpuzzle()

dPuz.display(dPuz.initial)
print ("------- Puzzel ---------")
print (dPuz.check_solvability( dPuz.initial) )
node = astar_search(dPuz, h=dPuz.calculateManhattenDist, display=True)
print ( len(node.solution()))

# puz = make_rand_8puzzle()
# print ("------- Puzzel ---------")
# puz.display()

# print ("------- Misplaced tiles ----------")
# astar_search(puz, h=puz.calculateMissplacedTiles, display=True)

# print ("\n------- Manhatten Distance ----------")
# astar_search(puz, h=puz.calculateManhattenDist, display=True)

# print ("\n------- Max of both  ----------")
# astar_search(puz, h=puz.maxH, display=True)

# print (puz.calculateManhattenDist( puz.initial))

# print (puz.maxH( puz.initial))