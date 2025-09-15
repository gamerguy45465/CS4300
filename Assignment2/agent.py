import random as rnd
import math
import heapq as hq
from typing import List, Tuple, Optional, Dict
import time

def reverse_path(path):
    i = 0
    j = len(path) - 1

    while i <= j:
        path[i], path[j] = path[j], path[i]
        i += 1
        j -= 1



def is_solvable(state): #Idea here is that the number of inversions is even
    list_to_check = [i for i in state if i != 0]

    inversions = 0

    for i in range(len(list_to_check)):
        for j in range(i+1, len(list_to_check)):
            if list_to_check[i] > list_to_check[j]:
                inversions += 1


    return inversions % 2 == 0

def InitialState():

    while True:
        states = []
        while len(states) <= 8:
            r = rnd.randint(0, 8)
            if r not in states:
                states.append(r)


        if is_solvable(tuple(states)):
            return tuple(states)


def Heuristic(name, goal):
    def manhattan(state):
        result = 0
        for i, t in enumerate(state):
            r = i // 3
            c = i % 3

            gr = goal.index(t) // 3
            gc = goal.index(t) % 3

            result += abs(r - gr) + abs(c - gc)


        return result


    def misplaced(state):
        count = 0
        for i in range(len(state)):
            if state[i] != i:
                count += 1

        return count


    def zero(state):
        return 0.0

    def one_count(state):
        return 1

    possibilities = {"manhattan": manhattan, "misplaced": misplaced, "zero": zero, "one_count": one_count}

    return possibilities[name]


def Actions(state):
    zero_index = state.index(0)

    r = zero_index // 3
    c = zero_index % 3

    what_to_do = []

    if(r > 0):
        what_to_do.append('U')

    if(r < 2):
        what_to_do.append('D')

    if(c > 0):
        what_to_do.append('L')

    if(c < 2):
        what_to_do.append('R')

    return what_to_do


def Transition(s, action):
    state = list(s)
    zero_index = state.index(0)
    if action == 'U':
        state[zero_index], state[zero_index - 3] = state[zero_index - 3], state[zero_index]

    elif action == 'D':
        state[zero_index], state[zero_index + 3] = state[zero_index + 3], state[zero_index]

    elif action == 'L':
        state[zero_index], state[zero_index - 1] = state[zero_index - 1], state[zero_index]

    elif action == 'R':
        state[zero_index], state[zero_index + 1] = state[zero_index + 1], state[zero_index]

    return tuple(state)

def GoalTest(start, goal=(1,2,3,4,5,6,7,8,0)):
    return start == goal


def UCS(start, h = Heuristic("zero",goal=[1,2,3,4,5,6,7,8,0])):
    frontier = []
    best_g = {tuple(start): h(start)}
    parent = {tuple(start): None}
    hq.heappush(frontier, (tuple(start), best_g[tuple(start)]))
    expanded = set()
    max_size = len(frontier)
    while frontier:
        if(len(frontier) > max_size):
            max_size = len(frontier)
        n, g = hq.heappop(frontier)

        if n in expanded:
            continue

        expanded.add(n)

        if GoalTest(n):
            path = [(1, 2, 3, 4, 5, 6, 7, 8, 0)]
            while path[-1] != start:
                path.append(parent[path[-1]])

            reverse_path(path)
            print("Max Frontier Size: ", max_size)
            return path, expanded

        for action in Actions(n):
            s_p = Transition(n, action)
            g_p = g + 1
            if g_p < best_g.get(tuple(s_p), math.inf):
                best_g[tuple(s_p)] = g_p
                parent[tuple(s_p)] = n
                hq.heappush(frontier, (tuple(s_p), g_p))


    print("Nodes Generated: ", expanded)
    print("Max Frontier Size: ", max_size)
    return None, expanded

def a_star(start, h = Heuristic("manhattan", goal=[1,2,3,4,5,6,7,8,0])):
    frontier = []
    best_g = {tuple(start): 0}
    parent = {tuple(start): None}
    expanded = set()
    max_size = len(frontier)

    hq.heappush(frontier, (h(start), 0, start))

    while frontier:
        if (len(frontier) > max_size):
            max_size = len(frontier)
        f, g, n = hq.heappop(frontier)
        #f = initial heuristic function
        #g = cost so far
        #n = our state node (I'm just doing this in a simple list)

        if n in expanded:
            continue

        expanded.add(n)




        if GoalTest(n):
            path = [(1,2,3,4,5,6,7,8,0)]
            while path[-1] != start:
                path.append(parent[path[-1]])

            reverse_path(path)
            print("Max Frontier Size: ", max_size)
            return path, expanded

        for action in Actions(n):
            s_p = Transition(n, action)

            g_p = g + 1

            keys = best_g.keys()



            if g_p <= best_g.get(tuple(s_p), math.inf): #Might have to fix this part
                best_g[tuple(s_p)] = g_p
                parent[tuple(s_p)] = n
                hq.heappush(frontier, (g_p + h(s_p), g_p, s_p))


    print("Nodes Generated: ", expanded)
    print("Max Frontier Size: ", max_size)
    return None, expanded


def main():
    h0time = []
    h1time = []
    h2time = []
    #1
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000

    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()


    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000

    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h = Heuristic("misplaced", goal=[1,2,3,4,5,6,7,8,0]))
    elapsed = (time.perf_counter() - start) * 1000

    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #2
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)


    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()


    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000

    h2time.append(elapsed)

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()


    #3
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)


    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #4
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #5
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)


    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #6
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)


    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)


    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)


    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #7
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)


    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #8
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #9
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #10
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)


    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #11
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)


    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #12
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)


    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #13
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #14
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)


    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #15
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #16
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)


    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)


    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #17
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)


    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)


    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #18
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)


    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #19
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #20
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #21
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #22
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #23
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #24
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #25
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #26
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #27
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #28
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()

    #29
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    #30
    initial_state = InitialState()

    cp_state1 = initial_state

    cp_state2 = initial_state

    start = time.perf_counter()
    result1, expanded1 = a_star(cp_state1)
    elapsed = (time.perf_counter() - start) * 1000
    h0time.append(elapsed)

    print("A* with Manhattan heuristic:")
    print()

    print("Path: ", result1)
    print("Number of nodes expanded: ", len(expanded1))
    print("Elapsed time: ", elapsed)
    print()

    start = time.perf_counter()
    result2, expanded2 = UCS(cp_state2)
    elapsed = (time.perf_counter() - start) * 1000
    h1time.append(elapsed)

    print()
    print("UCS with Zero Heuristic:")
    print()
    print("Path: ", result2)
    print("Number of nodes expanded: ", len(expanded2))
    print("Elapsed time: ", elapsed)

    print()
    print("A* with Misplaced Tile heuristic:")
    print()

    start = time.perf_counter()
    result3, expanded3 = a_star(cp_state1, h=Heuristic("misplaced", goal=[1, 2, 3, 4, 5, 6, 7, 8, 0]))
    elapsed = (time.perf_counter() - start) * 1000
    h2time.append(elapsed)

    print("Path: ", result3)
    print("Number of nodes expanded: ", len(expanded3))
    print("Elapsed time: ", elapsed)
    print()


    '''for t in h0time:
        print(t)


    print()

    for t in h1time:
        print(t)


    print()


    for t in h2time:
        print(t)


    print()'''







    






if __name__ == '__main__':
    main()