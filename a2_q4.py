
import time
import csv 
from a2_q1 import *
from csp import *

class CSPModified(CSP):

    def __init__(self, variables, domains, neighbors, constraints, nUnAssigned):
        super().__init__(variables, domains, neighbors, constraints)
        self.nUnAssigned = 0

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]
            self.nUnAssigned += 1

    def getUnassign(self):
        return self.nUnAssigned

#############################################################################################################
#                               HELPER FUNCTIONS
#############################################################################################################

def MapColoringCSP(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return CSPModified(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint, 0)

# For additional data I am using the count of maximum people in team. Inspired by github.com/MaxWong03

def maxTeamCount(csp_sol):
    team = {}
    maxTeam = 0
    for i in range(len(csp_sol)):
        if csp_sol[i] not in team:
            team[csp_sol[i]] = 0

    for i in range(len(team)):
        for j in range(len(csp_sol)):
            if i == csp_sol[j]:
                team[i] += 1

    for i in range(len(team)):
        if team[i] > maxTeam:
            maxTeam = team[i]

    return maxTeam	

# number of teams in solution
def teamsCount(csp_sol):
    team = []
    for i in range (len(csp_sol)):
        if csp_sol[i] not in team:
            team.append(csp_sol[i])
    return len(team)

# Using the color coding for solving the problem. 
def createColor(domain,number):
    domains = []
    done = False
    for i in range(number):
        if not done:
            domains.append(i)
        if i + 1 == domain:
            done = True

    return domains

#############################################################################################################
#                               Q4
#############################################################################################################

def run_q4():

    # Setup the csv files with header to gather data. 
    with open('resultProblemQ4.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(["Problem", "Solution"])

    with open('resultDataQ4.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(['Problem Index',"Probabilty","# Teams devided into", "Running Time", "Count of Assigned variables"," Count of Unassigned Variables", "Max people in team" ])
    
    graphs = [rand_graph(0.1, 105), rand_graph(0.2, 105), rand_graph(0.3, 105),rand_graph(0.4, 105), rand_graph(0.5, 105), rand_graph(0.6, 105)]
    
    index = 1
    for tmpGraph in graphs:
        print ("Graph")
        startTime = time.time()
        tmpGraph = graphs[index - 1]
        lenOfProblem = len(tmpGraph)
        haltTracker = False
        for state in range(lenOfProblem):
            if not haltTracker :
                problem = MapColoringCSP(createColor(state + 1, lenOfProblem), tmpGraph)
                AC3(problem)
                solution = min_conflicts(problem)

                if solution != None:
                    endTime = time.time() 
                    rowProblem = [ tmpGraph, solution]
                    rowData = [ index, index/10 ,teamsCount(solution), endTime-startTime, problem.nassigns, problem.getUnassign(), maxTeamCount(solution)]

                    # Write data to csv
                    with open('resultProblemQ4.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow(rowProblem)
                    with open('resultDataQ4.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow(rowData)
                
                    haltTracker = True
        index += 1
# run the bellow command for creating statstics. 
run_q4()
