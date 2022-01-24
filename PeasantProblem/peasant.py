# peasantProblem.py
# Date: 01/19/2021
# Course: Artificial Intelligence CSCI 0461
# Authors: 
#   Asa Hutchinson, Carter Williams, Samuel Rudqvist, Sean McCarty.
#
# Purpose: To implement a BFS algorithm to solve the peasant problem.

# The peasant problem: 
#   Move a peasant, a cabbage, a goat and a wolf from one side of the
#   river to the other side. 
#   Constraints:
#     The wolf and goat can never be left together on one side without 
#     the peasant. 
#     The goat and the cabbage can never be left together on one side 
#     without the peasant. 
#
# How does the peasant move everything to the other side of the river 
# in the smallest amount of passings?
# Solution:
#   Peasant takes goat across, returns alone
#   Takes wolf across, returns with the goat
#   Takes cabbage across, returns alone
#   Takes goat across
#   Total of 7 trips

# State: for each P, C, G and W, say 1 bank or -1 bank
# Initial state: all are east.
# Actions: One of the following crosses the river: P, PC, PG, PW 
#          either west to east or east to west.
# Possible actions: move peasant alone west, move peasant alone east,
#                   move peasant with G west move P and G east
#                   move P with W west, move P with W east
#                   move P with C west, move P with C east
# Transition model: For each component that crosses, swap 1 
#                   and -1 to get the new state.
# Goal test: Are all four on the west bank.
# Path cost: 1 unit for each crossing.

import queue

# Node - A class for the nodes in the graph
#   State - The state to which the node corresponds
#   cost - The length of the path to this node from the initial state.
#   parent - The parent node of the node being constructed.

class Node:
  def __init__(self, state=[1,1,1,1], cost=0, parent = "none"):
        self.state = state
        self.cost = cost
        self.parent = parent


# create_child_node() - Creates a new node with cost set to one unit higher and
#                       the old node as it's parent.
#   Parameters:
#     parent - The node in the search tree that generated this node.
#     state - The state of the parent node.
def create_child_node(parent, state):
    parent = parent
    return Node(state, parent.cost + 1, parent)
    

# is_safe() - Check if the state of the node is a safe state i.e the state is 
#             within the constraints.
#   Parameters:
#       state - The current state of the node.
def is_safe(state):
    if state[1] == state[2] and state[1] != state[0]:
        return False
    elif state[1] == state[3] and state[1] != state[0]:
        return False
    else:
        return True


# move() - Moves the components across the river by switching between 1 and -1.
#   Parameters:
#       state - the state of the node before the movement.
#       action - the action that is supposed to be taken.
def move(state, action):
    # Move only P
    if action == "P":
        state[0] = state[0] * -1
    # Move P and G
    if action == "PG" and state[0] == state[1]:
        state[0] = state[0] * -1
        state[1] = state[1] * -1
    # Move P and W
    if action == "PW" and state[0] == state[2]:
        state[0] = state[0] * -1
        state[2] = state[2] * -1
    # Move P and C
    if action == "PC" and state[0] == state[3]:
        state[0] = state[0] * -1
        state[3] = state[3] * -1
    
    # Check if the new state is safe
    if is_safe(state):
        return state
    else:
        return 0


# solution() - A function that prints a list of the states when the algorithm finds a solution.
#   Parameters: 
#        node - The node in the graph that holds information about that position.
def solution(node):
    trace_list = []
    while node.cost != 0:
        trace_list.append(node.parent.state)
        node = node.parent
    trace_list.reverse()
    return trace_list


# BSF_search() - Breadth First Search algorithm for solving the 
#                peasant problem. Returns a solution or failure.
#   Parameters:
#     actions - The set of possible moves that the elements can do
#     goal_state - The set that the algorithm is trying to match for a solution
def BFS_search(actions, goal_state):
    node = Node()
    # Checks if the state is within the constraints
    if not is_safe(node.state):
      print("The starting state was not safe.")
      return 0

    # Create the frontier as a queue an initialize explored to an empty list.
    # The frontier is the set of all nodes available for expansion at any given point.
    frontier = queue.Queue()
    frontier.put(node)
    explored = []
    # Checks if the queue is empty
    if frontier.empty():
        print("frontier was empty")
        return 0

    # While loop for when the queue has stuff in it
    while not frontier.empty():
        node = frontier.get()
        explored.append(node.state)
        
        for action in actions:
            child = create_child_node(node, node.state)
            child.state = move(child.state.copy(), action)
            
            # checks for 0 here because move returns 0 for incorrect states.
            if child.state == goal_state:
                trace = solution(child)
                trace.append(child.state)
                # Print how many trips it took for the solution
                print(f"A solution with {len(trace) - 1} trips has been found ")
                # Loop to print all of the states in the solution
                for i in range (0, len(trace)):
                  print(trace[i])
                return child
                
            # Check if the state of this child has already been explored.
            if child.state in explored:
              pass
            # This state did not satisfy the constraints.
            elif child.state == 0:
              pass
            else:
                frontier.put(child)
                if frontier.empty():
                    print("queue is empty")
                    
    print("No solution was found.")
    return 0


if __name__ == "__main__":
    actions = ["P","PG","PW","PC"]
    goal_state = [-1,-1,-1,-1]
    BFS_search(actions, goal_state)