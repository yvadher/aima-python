import random

# return random graph based on probability 

def rand_graph(p, n):
    graph = {}
    for val in range(n):
        graph[val] = []

    for i in range(n):
        for j in range(i+1,n): 
            if (random.random() < p):
                graph[i].append(j)
                graph[j].append(i)

    return graph

# Test the function 
# print (rand_graph(0.6, 5))