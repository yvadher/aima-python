# check_teams if csp solution is correct with given graph. 

def check_teams(graph, csp_sol):
	solLength = len(csp_sol)
	for i in range (solLength):
		for j in range(1, solLength):
			if csp_sol[i] == csp_sol[j]:
				if j in graph[i]:
					return false
	return True


# g = {0: [1, 2], 1: [0], 2: [0], 3: []}
# X = {0:0, 1:1, 2:1, 3:0}
# print (check_teams(g,X))