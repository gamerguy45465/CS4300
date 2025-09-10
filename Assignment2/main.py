import random as rnd

class State:
    def __init__(self, p1, p2, p3, p4, p5, p6, p7, p8, p9):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8
        self.p9 = p9


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


    print(list_to_work)

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

    return actions_to_take, keys, values

def Transition(state, action):
    empty = 0
    list_to_work = state.listState()

    for i in range(len(list_to_work)):
        if list_to_work[i] == '0':
            empty = i

    list_to_work[empty], list_to_work[action] = list_to_work[action], list_to_work[empty]

    print(list_to_work)

    state.update(list_to_work)


    return state

def GoalTest(state, goal):
    list_to_work = state.listState()

    if (list_to_work == goal):
        return True

    return False

def StepCost(state, action, next_state):
    return 1 #For this problem, everything should be 1


def Heuristic(state):
    pass








def main():
    state = IntiaialState()

    while(not GoalTest(state, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])):
        actions_to_take, items, indexes = Actions(state)
        randindex = rnd.randint(0, len(items) - 1)
        state = Transition(state, indexes[randindex])
        print(state)





if __name__ == '__main__':
    main()