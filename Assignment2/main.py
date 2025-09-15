import random as rnd
import math
import heapq as hq


class State:
    def __init__(self, p1, p2, p3, p4, p5, p6, p7, p8, p9):
        self.p1 = p1 #(0, 0)
        self.p2 = p2 #(1, 0)
        self.p3 = p3 #(2, 0)
        self.p4 = p4 #(0, -1)
        self.p5 = p5 #(1, -1)
        self.p6 = p6 #(2, -1)
        self.p7 = p7 #(0, -2)
        self.p8 = p8 #(1, -2)
        self.p9 = p9 #(2, -2)
    def printState(self):
        print_string = ""
        print_string += self.p1 + " "
        print_string += self.p2 + " "
        print_string += self.p3 + " "
        print_string += self.p4 + " "
        print_string += self.p5 + " "
        print_string += self.p6 + " "
        print_string += self.p7 + " "
        print_string += self.p8 + " "
        print_string += self.p9 + " "

        print(print_string)


    def listState(self):
        list_to_return = []
        list_to_return.append(self.p1)
        list_to_return.append(self.p2)
        list_to_return.append(self.p3)
        list_to_return.append(self.p4)
        list_to_return.append(self.p5)
        list_to_return.append(self.p6)
        list_to_return.append(self.p7)
        list_to_return.append(self.p8)
        list_to_return.append(self.p9)
        return list_to_return


    def listStateInt(self):
        list_to_return = []
        list_to_return.append(int(self.p1))
        list_to_return.append(int(self.p2))
        list_to_return.append(int(self.p3))
        list_to_return.append(int(self.p4))
        list_to_return.append(int(self.p5))
        list_to_return.append(int(self.p6))
        list_to_return.append(int(self.p7))
        list_to_return.append(int(self.p8))
        list_to_return.append(int(self.p9))
        return list_to_return



    def update(self, list_to_update):
        self.p1 = list_to_update[0]
        self.p2 = list_to_update[1]
        self.p3 = list_to_update[2]
        self.p4 = list_to_update[3]
        self.p5 = list_to_update[4]
        self.p6 = list_to_update[5]
        self.p7 = list_to_update[6]
        self.p8 = list_to_update[7]
        self.p9 = list_to_update[8]



def IntiaialState():
    states = []
    while len(states) <= 8:
        r = rnd.randint(0, 8)
        if r not in states:
            states.append(r)

    return State(str(states[0]), str(states[1]), str(states[2]), str(states[3]), str(states[4]), str(states[5]), str(states[6]), str(states[7]), str(states[8]))


def Actions(state):
    position = 0
    actions_to_take = {}
    list_to_work = state.listState()
    for i in range(len(list_to_work)):
        if int(list_to_work[i]) == 0:
            position = i


    #print(list_to_work)

    if((position - 3) >= 0):
        actions_to_take[list_to_work[position - 3]] = position - 3

    if((position - 1) >= 0):
        actions_to_take[list_to_work[position - 1]] = position - 1

    if((position + 3) < 9):
        actions_to_take[list_to_work[position + 3]] = position + 3

    if((position + 1) < 9):
        actions_to_take[list_to_work[position + 1]] = position + 1

    keys = list(actions_to_take.keys())
    values = list(actions_to_take.values())

    return values, keys, actions_to_take

def Transition(state, action):
    empty = 0
    list_to_work = state.listState()

    #print(action)

    for i in range(len(list_to_work)):
        if list_to_work[i] == '0':
            empty = i

    list_to_work[empty], list_to_work[action] = list_to_work[action], list_to_work[empty]

    #print(list_to_work)

    state.update(list_to_work)


    return state

def GoalTest(state, goal):
    list_to_work = state.listState()

    if (list_to_work == goal):
        return True

    return False

def StepCost(state, action, next_state):
    return 1 #For this problem, everything should be 1


def Heuristic(h_type, g):
    goal = g.listStateInt()
    def manhattan(state):
        s = state.listStateInt()
        return abs(s[0] - goal[0]) + abs(s[1] - goal[1]) + abs(s[2] - goal[2]) + abs(s[3] - goal[3]) + abs(s[4] - goal[4]) + abs(s[5] - goal[5]) + abs(s[6] - goal[6]) + abs(s[7] - goal[7]) + abs(s[8] - goal[8])

    def euclidean(state):
        s = state.listStateInt()
        return math.hypot(s[0] - goal[0], s[1] - goal[1], s[2] - goal[2], s[3] - goal[3], s[4] - goal[4], s[5] - goal[5], s[6] - goal[6], s[7] - goal[7], s[8] - goal[8])


    def zero(state):
        return 0.0


    def weighted_15(s):
        return 1.5 * manhattan(s)

    types_dict = {"zero": zero, "manhattan": manhattan, "euclidean": euclidean, "weighted_15": weighted_15}

    return types_dict[h_type]



def A_star(s0, goal):
    pq = []
    hq.heappush(pq, (0, s0))
    h = Heuristic("manhattan", goal)
    f = h(s0)
    g = 0
    best_g = {}
    parent = {}



    while pq:
        n = hq.heappop(pq)
        if GoalTest(n[1], goal):
            path = [goal]
            while path[-1] != s0:
                path.append(parent[path[-1]])

            return path

        A, values, dict_to_work = Actions(n[1])

        for a in A:
            s_p = Transition(n[1], a)
            print(g)
            g_p = g + 1

            if s_p not in best_g:
                best_g[s_p] = g_p
                parent[n] = s_p
                hq.heappush(pq, (g_p, s_p))
                g = g_p


            elif g_p <= best_g[s_p]:
                best_g[s_p] = g_p
                parent[n] = s_p
                hq.heappush(pq, (g_p, s_p))
                g = g_p



            print(best_g)


    print("Came here")
    return None

def main():
    state = IntiaialState()

    n = A_star(state, State("1", "2", "3", "4", "5", "6", "7", "8", "0"))



if __name__ == '__main__':
    main()