import random as rnd
import math
import heapq as hq
from typing import List, Tuple, Optional, Dict

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


    def zero(state):
        return 0.0

    possibilities = {"manhattan": manhattan, "zero": zero}

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

def a_star(start, h = Heuristic("manhattan", goal=[1,2,3,4,5,6,7,8,0])):
    frontier = []
    best_g = {tuple(start): 0}
    parent = {tuple(start): None}
    Current = start

    hq.heappush(frontier, (h(start), 0, start))

    while frontier:
        f, g, n = hq.heappop(frontier)
        #f = initial heuristic function
        #g = cost so far
        #n = our state node (I'm just doing this in a simple list)

        Current = n


        if GoalTest(n):
            path = [(1,2,3,4,5,6,7,8,0)]
            while path[-1] != start:
                path.append(parent[path[-1]])

            reverse_path(path)
            return path

        for action in Actions(n):
            s_p = Transition(n, action)

            g_p = g + 1

            keys = best_g.keys()



            if g_p <= best_g.get(tuple(s_p), math.inf): #Might have to fix this part
                best_g[tuple(s_p)] = g_p
                parent[tuple(s_p)] = n
                hq.heappush(frontier, (g_p + h(s_p), g_p, s_p))

    print(Current)
    path = [Current]
    while path[-1] != start:
        path.append(parent[path[-1]])

    return path.reverse()


def main():

    initial_state = InitialState()


    result = a_star(initial_state)








if __name__ == '__main__':
    main()