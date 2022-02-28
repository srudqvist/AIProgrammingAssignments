"""
Solution to the Peasant, cabbage, goat, and wolf river crossing problem
By Carol Browning
January 20, 2020

Change log: Updated January 26, 2021
"""

""" Define constants to make code easier to read. """

# To change sides, multiply current side by -1:
EAST = 1   
WEST = -1

# A state list will be a list of sides (east or west) in the order
# peasant, cabbage, goat, wolf.
# These constants will be indices into the state list.
PEASANT=0   
CABBAGE=1   
GOAT=2
WOLF=3

""" Define the Node class.
    Node objects are the vertices of the search tree.
    Each node contains a state, a pointer to the parent,
    the action to derive this state from the parent, and the
    cost of getting to this node.
"""

class Node:
    def __init__(self,state,parent,action,cost):
        # a state is a list of four values, each either east or west
        self.state = state
        # the pointer to the previous state
        self.parent = parent 
        # what action is performed on parent to get this state
        self.action = action
        # length of path from initial state to this one
        self.cost = cost
        
""" Given a state, generate a list of the possible actions.
    An action is a list of items to move to the other side. The peasant must
    be included in any action.  The peasant may take another item that is on
    the same side as the peasant.
"""

def actionList(state): 
    # Initialize mylist with the action that the peasant travels alone.
    mylist = [[PEASANT]] 
    for item in [CABBAGE,GOAT,WOLF]:
        if state[item] == state[PEASANT]:
            # If the item is on the same side as the peasant,
            # the peasant could take this item across in the boat.
            mylist.append([PEASANT,item])
    return(mylist)

""" Given a state, check to see whether or not it is valid. Goats cannot
    be left alone with another item because goats eat cabbage and wolves
    eat goats.
"""

def isValid(state):
    # If the goat is left alone, it cannot be with the cabbage or the wolf.
    if state[PEASANT] != state[GOAT]:
        if state[GOAT] == state[CABBAGE] or state[GOAT] ==state[WOLF]:
            return False
    return True

""" Given a current state and an action, return the next state.
    A state is a list of four sides. A side is either east or west.
    The action is the list of items that change sides.
"""

def makeNewState(currentState,action):
    newState = []
    for item in [PEASANT,CABBAGE, GOAT, WOLF]:
        if item in action:
            # Have this item change sides
            newState.append(-1*currentState[item])
        else:
            # Leave this item on its current side
            newState.append(currentState[item])
    return newState

""" findAnswer is the main algorithm for searching the space for a solution.
"""

def findAnswer():

    # Create the initial state, the goal state, the initial node for the
    # search tree, the frontier list, and the explored states list.
    initialState = [WEST,WEST,WEST,WEST]
    goalState = [EAST,EAST,EAST,EAST]
    initialNode = Node(initialState,None,None,0)
    frontierNodes = [initialNode]
    exploredStates = []

    # Keep searching if there are nodes to search from.
    while frontierNodes != [ ]:
        # Get the first node out of the frontier list.
        # Note: pop() removes from back of list, pop(0)from front of list
        current = frontierNodes.pop(0)
        
        # Check to see if we've reached the goal. If so, return this node.
        if current.state == goalState:   
            return(current,len(exploredStates))
        # Make a list of the actions we can perform in this state.
        actions = actionList(current.state)
        # Add current state to explored states list
        exploredStates.append(current.state)    
        
        # For each action, see if we need to create a new node 
        for action in actions:
            newState = makeNewState(current.state,action)
            # If this state is valid and not already seen, create the new node
            # and add it to the back of the frontierNodes list.
            if isValid(newState):
                newNode = Node(newState,current,action,current.cost+1)
                if newNode not in frontierNodes:
                    if newNode.state not in exploredStates:
                        frontierNodes.append(newNode)

    # If frontier is empty and no solution has been found, notify user.
    print("No solution found")
    return(None,-1)

""" Print the path from the initial node to the given node.
    This is a recursive function.
"""

def printAnswer(node):
    
    # If this node's parent is None, we are at the starting node.
    if node.parent == None:
        print(" The peasant, cabbage, goat, and wolf are on the west bank. ")
        # print("Initial state: ",node.state)

    # Otherwise, print the previous step then print this one.
    else:
        
        # Print the path to the previous step.
        printAnswer(node.parent)

        # Compose the message that describes the action to get to this step.
        
        # The first item in each action is the side that the peasant is on.
        message = " Move the peasant from "
        if node.state[0]==EAST:
            message = message + "west to east"
        else:
            message = message + "east to west"
            
        # Each action may contain one other item for the peasant to transport.
        if len(node.action) > 1:
            message = message + ", along with the "
            if node.action[1]==1:message = message +"cabbage. "
            if node.action[1] == 2: message = message + "goat. "
            if node.action[1] == 3: message = message + "wolf. "
        else:
            message = message + ". "

        # Print the message describing the action to get to this step.
        # print("Action: ",node.action)
        print(message)
        # print ("New state: ",node.state)
        
""" Main program. Find the answer, then print the answer and the analysis.
"""

def main():
    finalNode,numExploredStates = findAnswer()
    if numExploredStates != -1:
        printAnswer(finalNode)
        print(" The peasant, cabbage, goat, and wolf are on the east bank. ")
        print("Number of trips = ",finalNode.cost)
        print("Number of explored states = ",numExploredStates)

main()

