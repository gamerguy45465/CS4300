InitialState() - Defines the intial state that the agent will be acting in

Actions(state) - Will define a list of actions that the agent will be able to take

Transition(state, action) - Will transition from one state to the next, depending on the legal action given

GoalTest(state) - Will test to see if the state given is the Goal we desire or not

StepCost(state, action, next_state) - Will calculate the step cost (although, in this particular problem, every step has only a cost of 1 per move, rendering this function potentially pointless to implement).

Heuristic(state) - This function will define the remaining cost of the state we are in to the goal.