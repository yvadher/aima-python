"""
Assignment 1 file for running 8-Puzzel and finding the A* algortihym optimality

"""

from search import EightPuzzle
import random

class EightPuzzleGame(EightPuzzle):
    def __init__(self, initial):
        super().__init__(initial)

def display(state):
    
    #clousure function 
    def printer(str):
        print (str, end ='')
    
    for index, number in enumerate(state):
        printer(number) if (number != 0 ) else printer("*")
        printer("\n") if ( (index + 1) % 3 == 0 and index != 0 ) else printer(" ")
            
        
def make_rand_8puzzle():
    while True:
        initialPuzzel = random.sample( range(0,9), 9)
        puzzel = EightPuzzleGame(initialPuzzel)
        if (puzzel.check_solvability(puzzel.initial)): 
            return puzzel


make_rand_8puzzle()
