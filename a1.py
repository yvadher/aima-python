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

    return EightPuzzleGame((1,0,3,4,2,6,7,5,8))
    return EightPuzzleGame( (4,1,0,7,5,3,6,8,2) )
    return EightPuzzleGame((8,2,3,4,5,6,7,1,0))


def palyTheGame():
    randPuzzles = []
    for i in range(0,10):
        tempPuzzel = make_rand_8puzzle()
        randPuzzles.append(tempPuzzel)

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