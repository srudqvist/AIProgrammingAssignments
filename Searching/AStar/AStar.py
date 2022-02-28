# Replit.com link:
# https://replit.com/@cwilliams039/A-Star#WithTests.py

'''
    A* algorithm for finding a path through a grid
    Starter code by Dr. Browning, January 28, 2020
    Updated Feb. 7, 2021, and January 29, 2022

    In an n by n grid, some walls are erected, specified in the grid with 1's.          
    Given a starting position and ending position (valid i.e. not in walls)
    find the shortest path from start to end.
'''

GRID_0 = [[0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0]]

GRID_1 =[[0, 0, 0, 0, 0, 1, 0, 0],
         [0, 1, 0, 1, 0, 0, 0, 0],
         [0, 1, 0, 1, 0, 1, 1, 1],
         [0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]

GRID_2= [[0, 0, 0, 0, 0, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 0, 0],
         [0, 1, 0, 0, 1, 0, 0, 0],
         [0, 1, 0, 0, 0, 0, 1, 1],
         [0, 1, 1, 1, 0, 0, 1, 0],
         [0, 1, 0, 1, 1, 0, 1, 0],
         [0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]

GRID_3= [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 0, 1, 1, 1, 0, 0],
         [0, 1, 0, 0, 1, 1, 0, 0],
         [0, 1, 0, 0, 0, 1, 1, 1],
         [0, 1, 1, 1, 0, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 1, 1, 0, 0],
         [0, 0, 0, 0, 0, 1, 0, 0]]
         
NO_WAY_GRID=[[0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]] 

GRID = NO_WAY_GRID
# dimension - GRID is N by N
N = len(GRID) 
START = (1,6)
END = (7,1)
INF = N*N # > the length of a path between any two places in the grid
BIG_DISTANCE = INF+1
OPEN_ADD = 0

'''
grid = [[0, 0,     0, 0, 0, 0, 1, 0],
        [0, 0,     0, 0, 0, 0, 1, END],
        [0, 0,     0, 0, 0, 0, 1, 0],
        [0, 0,     0, 1, 0, 1, 1, 0],
        [0, 0,     0, 1, 0, 0, 0, 0],
        [0, 0,     0, 1, 0, 0, 0, 0],
        [0, START, 0, 1, 0, 0, 0, 0],
        [0, 0,     0, 1, 0, 0, 0, 0]]
'''

# We can move up, down, left, or right as long as we don't move onto
# a wall (1) or off the grid.
MOVES = [(0,-1),(0,1),(-1,0),(1,0)]

# Sean: To move diagonal, would we add (1, 1), (-1, -1), (1, -1), (-1, 1) This works and is proven!

# Each grid location visited on our search will have a Vertex object.
# G is the number of moves taken to get to this location.
# H is the square of the Euclidean distance from our location to end.
class Vertex:
    def __init__(self,column, row,G=INF,pathParent=None):
        self.col = column            # location in grid
        self.row = row
        self.pathParent = pathParent    # parent on path of lowest cost so far
        self.G = G                      # cost of getting here
        self.H = (column - END[0])**2 + (row - END[1])**2
                                        # square of Euclidean distance to end
        self.F = G+self.H               # A* heuristic

    # A setter for G also updates F.
    def setG(self,value):
        '''Assignment part 1 DONE'''
        self.G = value
        self.F = self.G + self.H

    def samePlace(self,anotherVertex):
        # Tell whether or not two vertices refer to the same grid location.
        if self.col==anotherVertex.col and self.row==anotherVertex.row:
            return True
        return False

    def printVertex(self):
        print(self.col, self.row)

    def getF(self):
        return self.F

    def getG(self):
        return self.G
  
    def setParent(self, newParent):
        self.pathParent = newParent

BIG_VERTEX = Vertex(-1,-1, BIG_DISTANCE)

# Find the vertex in vlist with the smallest heuristic value F.
def smallest(vlist): # 
    '''Assignment part 2 DONE'''
    smallestV = BIG_VERTEX
    for vertex in vlist:
      if vertex.getF() < smallestV.getF():
        smallestV = vertex
    
    return smallestV # change this line!!!

# See if a vertex refers to the same grid position as a node on a list of
# vertices.  If so, return that node.
def onList(vertex, vlist):
    # If vertex's position is same as position of a node on vlist,
    # return that node.
    '''Assignment part 3 DONE'''
    for node in vlist:
        if vertex.samePlace(node):
          return node
        
    #else return None
    return None

# If a given move from a given vertex should be added to the openList, add it.
# If it is already on the open list, update its G value.
def considerMoving(move,bestV,closedList,openList):
    global OPEN_ADD
    newColumn = bestV.col + move[0]
    newRow = bestV.row + move[1]
    # See if the new position is on the grid.
    if newColumn >= 0 and newColumn < N and newRow >= 0 and newRow < N :
        # Make sure new position is not a wall.
        if GRID[newRow][newColumn] != 1:           
            # Make vertex for new position.
            newVertex = Vertex(newColumn,newRow,bestV.G+1,bestV)
            # If we haven't already closed this vertex,
            if onList(newVertex,closedList)==None:
                nodeOnOpenList = onList(newVertex,openList)
                # and it is not on the open list,
                if nodeOnOpenList == None:
                    # add the vertex to the open list.
                    '''Assignment part 4a DONE.'''
                    OPEN_ADD = OPEN_ADD + 1
                    openList.append(newVertex)
                else:
                    # If the path to nodeOnOpenList through bestV is a better G
                    # value, update G value and path parent for nodeOnOpenList.
                    '''Assignment part 4b PENDING.'''
                    #path to node through bestV | path to node not through bestV
                    if bestV.getG()+1 < nodeOnOpenList.getG():
                      nodeOnOpenList.setG(bestV.getG()+1)
                      nodeOnOpenList.setParent(bestV)

#HINT:
#In part 4b, we have the shortest path from start to bestV.  Its length is bestV’s G.  We have a node on the open list.  We want to know whether or not to update the node’s G value and its parent node.  If we go through bestV to get to the node, the new G value will be one more than bestV's G value since each time we move a square over, it is a path cost of 1.  We should update if the new G value is better than the current one.

# Print the answer - the path from startVertex to endVertex.

''' Assignment part 5 Change this function to show grid & illustrate path.'''
def printAnswer(grid,startVertex,endVertex):
    Eprinted = False
    printGrid = None
    citylist = [(endVertex.row,endVertex.col)]
    cityVertex = endVertex
    while cityVertex != startVertex:
        cityVertex = cityVertex.pathParent
        citylist = [(cityVertex.row,cityVertex.col)] + citylist
    
    print(f"citylist: {citylist}")
    print(startVertex.row)
    print(startVertex.col)
    currRow = -1
    currCol = -1
    for row in grid:
      currRow += 1
      currCol = -1
      printGrid = ""

      for node in row:
        currCol += 1
        if currRow == endVertex.row and currCol == endVertex.col:
          printGrid = printGrid + " E "
          Eprinted = True
        if currRow == startVertex.row and currCol == startVertex.col:
          printGrid = printGrid + " S "
        else:
          found = False
          for cityNode in citylist:
            if currRow == cityNode[0] and currCol == cityNode[1]:
              found = True
              if not Eprinted:
                printGrid = printGrid + " X "
              else:
                pass
              
          if found == False:
            printGrid = printGrid + " " + str(node) + " "  
          # Set back to false so that the end has not been found on 
          # other rows.
          Eprinted = False       
      print(printGrid)



#Example:
#    def printBoard(self):
#        for row in range(DIMENSION):
#            out = '** '
#            for col in range(DIMENSION):
#                square = self.squares[row][col]
#                if square.isSafe():
#                    out=out+" safe "+" ** "
#                else:
#                    out=out+" dark "+" ** "
#            print(out)



    answer = "The shortest path from ("+str(startVertex.row)+","
    answer = answer + str(startVertex.col)+") to ("+str(endVertex.row)+","
    answer = answer + str(endVertex.col)+")"
    answer = answer +" has length "+str(endVertex.F )+":"
    print(answer)
    
    #citylist = [(endVertex.row,endVertex.col)]
    #cityVertex = endVertex
    #while cityVertex != startVertex:
    #    cityVertex = cityVertex.pathParent
    #    citylist = [(cityVertex.row,cityVertex.col)] + citylist
    print(citylist)

# Search the grid for a path from the start point to the end point,
# going around walls if necessary.
def main():
    # Make the starting vertex.
    startVertex = Vertex(START[0],START [1],0)
    startVertex.pathParent = startVertex

    # We will generate vertices as we encounter them.  When a new vertex is
    # generated as we search, we add it to the open list.
    openList = [startVertex]
    # We will move vertices to the closed list as we search past them.
    closedList = []

    # Open list is a list of vertices we need to explore.
    done = False
    while openList != [] and not done:
        # Find the next vertex to explore: open list element with smallest F.  
        bestV = smallest(openList)
        if bestV.col == END[0] and bestV.row == END[1]:
            ans = printAnswer(GRID, startVertex,bestV)
            done = True
        else: # so bestV is completed
            openList.remove(bestV)
            closedList.append(bestV)
            # Look at the moves we can make from bestV.
            # Which ones get added to openList?
            for move in MOVES:
                considerMoving(move,bestV,closedList,openList)
    if not done:
        print(f"The grid had no path from start to end.")
    #print(f"Open Add: {OPEN_ADD}")

def testCase(testNumber, grid):
    global GRID
    global OPEN_ADD
    GRID = grid
    OPEN_ADD = 0

    # Make the starting vertex.
    startVertex = Vertex(START[0],START [1],0)
    startVertex.pathParent = startVertex

    # We will generate vertices as we encounter them.  When a new vertex is
    # generated as we search, we add it to the open list.
    openList = [startVertex]
    # We will move vertices to the closed list as we search past them.
    closedList = []

    # Open list is a list of vertices we need to explore.
    done = False
    while openList != [] and not done:
        # Find the next vertex to explore: open list element with smallest F.  
        bestV = smallest(openList)
        if bestV.col == END[0] and bestV.row == END[1]:
            print("\nResult for test {testNumber}")
            printAnswer(GRID, startVertex,bestV)
            done = True
        else: # so bestV is completed
            openList.remove(bestV)
            closedList.append(bestV)
            # Look at the moves we can make from bestV.
            # Which ones get added to openList?
            for move in MOVES:
                considerMoving(move,bestV,closedList,openList)
    if not done:
        print(f"\nThe grid in test {testNumber} had no path from start to end.")

def test():
    print("Testing.")
    testCase(1,GRID_0)
    testCase(2,GRID_1)
    testCase(3,GRID_2)
    testCase(4,GRID_3)
    testCase(5,NO_WAY_GRID)
                       
#main()
test()
