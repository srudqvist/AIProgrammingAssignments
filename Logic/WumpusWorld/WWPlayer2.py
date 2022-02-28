'''
Basic Player Class for Wumpus World            
Dr. Browning January 9,2022

The Player class creates a simple player that gets sensor
input, records it in a knowledge base, chooses the move "climb"
and reports move to caller.

Create your own subclass and overwrite the methods so that
your player will make inferences and resolutions in order to
enhance the knowledge base and make smart decisions
about moves to make, either moveTo, shootToward, grab, or climb.
'''

#### NOTES ####
# neighbors from getNeighbors are listed in following order: north, south, west, east
from WWKnowledgeBase import *
import time
#TODO:
#    If we are in 00 and have stench, fire the arrow in any direction.
#      If scream, we are safe, if no scream, wumpus is in the other square.
#
#
#
#
#
#
class Player:
    
    def __init__(self):
        self.kb = KnowledgeBase(DIMENSION)
        self.col = 0
        self.row = 0
        self.hasGold = False
        self.hasArrow = True

    
    # Game sends us sensor data [stench,breeze,glitter,scream]
    # We respond with an action.   
    def move(self,sensorData):
        self.recordSensorData(sensorData)
        self.reason(sensorData)
        return(self.selectAction())
    
    def recordSensorData(self,sensorData):
        #   sensor data is tuple of 4 booleans:
        #   stench, breeze, glitter, scream
        if sensorData[3]:
            self.weKilledTheWumpus()
        if sensorData[0]:
            self.kb.updateStench(self.col,self.row)
        if sensorData[1]:
            self.kb.updateBreeze(self.col,self.row)
        if sensorData[2]:
            self.kb.updateGlitter(self.col,self.row)

    def weKilledTheWumpus(self):
        # make changes to the knowledge base
        return
    # Square is the square that we didnt shoot into,
      # the wumpus is in the square because we missed.
    def weMissedTheWumpus(self, square):
        return

    def reason(self,sensorData):
        # make inferences based on new data
        return

        #check current square for breeze
        # if currentKBSquare.breeze:
        #     #add list of all adjacent squares to the kb.pitInfo list
        #     neighbors = self.kb.getNeighbors(currentKBSquare)
        #     # list to hold possible pits.
        #     possiblePit = []
        #     for neighbor in neighbors:
        #         if (neighbors[0].visited == False):
        #             possiblePit.append(neighbor)
        #     if len(possiblePit) > 0:
        #       self.kb.pitInfo.append(possiblePit)
            # print item in pitInfo
            #for item in self.kb.pitInfo[0]:
              #print(f"possible pit: {item.col, item.row}")
            #print(f"PitInfo: {self.kb.pitInfo}")
              
        # Check if we killed the wampus, then check if there is stench and update the wumpusInfo
        #if weKilledTheWumpus() == False:        
            

      

    def selectAction(self):
        # decide to either
        #   "moveTo", col, row
        #   "grab"
        #   "shootToward", col, row
        #   "climb"

        # Example code for grabbing gold
        currentKBSquare = self.kb.squares[self.col][self.row]
        if currentKBSquare.gold: 
            # handle case where we grab  the gold and want to leave
            return "grab"

        # Example: we want to move to the right one square
        oldCol = self.col
        oldRow = self.row
        self.col = self.col+1
        newCol = self.col
        newRow = self.row
        self.kb.updatePlayerLocation(oldCol,oldRow,newCol,newRow)
        return"moveTo",newCol,newRow

class JimmyDean(Player):
    def __init__(self):
        self.kb = KnowledgeBase(DIMENSION)
        self.col = 0
        self.row = 0
        self.hasGold = False
        self.hasArrow = True
        self.wumpusAlive = True
        self.wumpusLocated = False
        self.lastSquare = None
        self.visitedSquares = []
        self.pathBack = []
        self.moveCount = 0
        self.climb = False
        self.shoot = False
        self.givingUp = False
        self.timeToGrab = False
        self.grid = [[0,0,0,0], 
                    [0,0,0,0], 
                    [0,0,0,0], 
                    [0,0,0,0]]
        #self.wayBack = []
    
    
      
    def weKilledTheWumpus(self):
        # make changes to the knowledge base
        print("\nWe killed the wumpus")
        # clear the wumpus list
        self.wumpusAlive = False
        self.kb.wumpusInfo.clear()
        print(f"WumpusInfo: {self.kb.wumpusInfo}")

        return
    # Square is the square that we didnt shoot into,
      # the wumpus is in the square because we missed.
    def weMissedTheWumpus(self, square):
        if self.hasArrow == False and self.wumpusAlive == True:
            self.kb.wumpusInfo.clear()
            self.kb.wumpusInfo.append(square)
            self.wumpusLocated = True
        print()
      
    # Search for the shortest path back
    # Take a list of all visited squares as parameter.
    GRID = [[0,0,0,0], 
            [0,0,0,0], 
            [0,0,0,0], 
            [0,0,0,0]]
    #INF = 16
    # We can move up, down, left, or right as long as we don't move onto
    # a wall (1) or off the grid.
    MOVES = [(0,-1),(0,1),(-1,0),(1,0)]
    #nodeCounter shows the amount of times a node has been added to openList
    nodeCounter = 0
    class Vertex:
        def __init__(self,column, row,G=16,pathParent=None):
            self.column = column
            self.row = row
            self.pathParent = pathParent
            self.G = G
            self.H = (column - END[0])**2 + (row - END[1])**2
            self.F = G+self.H 

        # A setter for G also updates F.
        def setG(self,value):
            self.G = value
            self.F = self.G + self.H

        # Tell whether or not two vertices refer to the same grid location.
        def samePlace(self,anotherVertex):
            if self.column==anotherVertex.column and self.row==anotherVertex.row:
                return True
            return False

        def printVertex(self):
            print(self.column, self.row)

    # Find the vertex in vlist with the smallest heuristic value F.
    def smallest(vlist): 
        small = vlist[0]
        for v in vlist:
            if v.F < small.F:
                small = v
        return small 

    # See if a vertex refers to the same grid position as a node on a list of
    # vertices.  If so, return that node.
    def onList(vertex, vlist):
        # If vertex's position is same as position of a node on vlist,
        # return that node.
        for node in vlist:
            if vertex.row == node.row:
                if vertex.column == node.column:
                    return node
        #else return None
        return None

    # If a given move from a given vertex should be added to the openList, add it.
    # If it is already on the open list, update its G value.
    def considerMoving(move,bestV,closedList,openList):
        newColumn = bestV.column + move[0]
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
                        openList.append(newVertex)
                        global nodeCounter 
                        nodeCounter = nodeCounter + 1
                        
                    else:
                        # If the path to nodeOnOpenList through bestV is a better G
                        # value, update G value and path parent for nodeOnOpenList.
                        if newVertex.G < nodeOnOpenList.G:
                            nodeOnOpenList.setG(newVertex.G)
                            nodeOnOpenList.pathParent = newVertex.pathParent


    def shortPath(self, visitedList, current):
        # 4x4 grid
        # class Vertex:
        #     def __init__(self, column):
        #         self.column = column
        
        #start = Vertex(2)
        print("\n\n\nshortest path called\n\n\n")
        for square in visitedList:
            col = square.col
            row = square.row
            GRID[col][row] = 1
        for col in GRID:
            for row in GRID:
                print(row)

        startVertex = Vertex(START[0],START [1],0)
        startVertex.pathParent = startVertex
        shortestPath = []
        
        return shortestPath






    def reason(self,sensorData):
        # make inferences based on new data
        self.climb = False
        self.shoot = False
        print(f"SensorData: {sensorData}")
        possiblePit = []
        
        # What is the current square
        currentKBSquare = self.kb.squares[self.col][self.row]
        currentKBSquare.safe = True
        if currentKBSquare in self.kb.safeNotVisited:
            self.kb.safeNotVisited.remove(currentKBSquare)
        
        # Skip reasoning if we already have the gold
        if self.hasGold:
            return ""

        # Get the neighbors of the current square.
        neighbors = self.kb.getNeighbors(currentKBSquare)
        
        #if not self.wumpusLocated and len(self.kb.wumpusInfo) > 0:
         #   new = list(set(self.kb.wumpusInfo))
          #  for item in new:
           #     neighbors = self.kb.getNeighbors(item)
        
        
        stench, breeze, glitter = sensorData[0], sensorData[1], sensorData[2]
        ## If we are surrounded in breezes we want to escape
        if len(neighbors) == 2:
            #neighbors[0] is down, neighbors[1] is to the right if we are in 00
            print("\nTEST\n")
            print("current square:", currentKBSquare.col, currentKBSquare.row)
            for neighbor in neighbors:
                print("neighbor:", neighbor.col, neighbor.row)
            print("pitInfo")
            for list in self.kb.pitInfo:
                for item in list:
                    print(item.col, item.row)
            if neighbors[0].visited and neighbors[1].visited:
                if neighbors[0].breeze and neighbors[1].breeze:
                    print("throwing in the towel1")
                    self.climb = True
                    return "climb"
            if neighbors[0].visited and currentKBSquare.col + currentKBSquare.row == 0:
                if len(self.kb.wumpusInfo) > 0:
                    if neighbors[1] in self.kb.wumpusInfo:
                        print("throwing in the towel 2")
                        self.climb = True
                        return "climb"
                if len(self.kb.pitInfo) > 0:
                    if neighbors[1].breeze:
                        print("throwing in the towel 2.1")
                        self.climb = True
                        return "climb"

            if neighbors[1].visited and currentKBSquare.col + currentKBSquare.row == 0:
                if len(self.kb.wumpusInfo) > 0:
                    if neighbors[0] in self.kb.wumpusInfo:
                        print("throwing in the towel3")
                        self.climb = True
                        return "climb"
                if len(self.kb.pitInfo) > 0:
                    if neighbors[0].breeze:
                        print("throwing in the towel 2.1")
                        self.climb = True
                        return "climb"
            
            

        # We missed the wumpus but can draw the conclusion that it was in the other square
        # We are still in 00.
        if (self.moveCount == 1 and not self.hasArrow) and self.wumpusAlive:
            print("We missed the wumpus on the first try")
            neighbors = self.kb.getNeighbors(currentKBSquare)
            neighbor = neighbors[1]
            self.weMissedTheWumpus(neighbor)
            #return ""
        
        if glitter and not self.hasGold:
            print(f"The gold is in this square: {currentKBSquare.col, currentKBSquare.row}")
            self.timeToGrab = True
            return "grab"
            

        if breeze:
            
            print("A breeze was sensed")
            
            print(f"Possible Pits: ")
            # If breeze in 00
            if currentKBSquare.col == 0 and currentKBSquare.row == 0:
              self.climb = True
              return "climb"
            # If the neighbor is not visited, add it to the list of possible pits.
            for neighbor in neighbors:
                if not neighbor.visited:
                    possiblePit.append(neighbor)
                    print(neighbor.col, neighbor.row)
            
            if len(possiblePit) == 1:
                print("This is a pit:", possiblePit[0].col, possiblePit[0].row)
            if len(possiblePit) > 0:
              self.kb.pitInfo.append(possiblePit)

        
            #for list in self.kb.pitInfo:
                #for item in list:
                    #print(f"possible pit: {item.col, item.row}")
            
            # Check for duplicates in the pitInfo list, if there is a duplicate then this square 
            # must contain a pit.
            #for i in range(0, len(self.kb.pitInfo) - 1):
             #   for j in range(1, len(self.kb.pitInfo)):
              #      if self.kb.pitInfo[i] == self.kb.pitInfo:
               #         print(f"{self.kb.pitInfo[j].col, self.kb.pitInfo[j].row} must be the pit.")

        if not stench:
            #for item in self.kb.wumpusInfo:
                #print("WU:", item.col, item.row)
            neighbors = self.kb.getNeighbors(currentKBSquare)
            for neighbor in neighbors:
                while neighbor in self.kb.wumpusInfo:
                    self.kb.wumpusInfo.remove(neighbor)
                    print("removed neighbor from wumpus list")
                    # Set to safe if there is no breeze
                    if not breeze:
                        for i in range(0, len(self.kb.pitInfo)):
                            for item in self.kb.pitInfo[i]:
                                while neighbor in self.kb.pitInfo[i]:
                                    self.kb.pitInfo[i].remove(neighbor)
                                    print("Removed neighbor from pitList")
                        neighbor.safe = True
                        # Make sure it is only added to safeNotVisited once.
                        if not neighbor.visited and (neighbor not in self.kb.safeNotVisited):
                            self.kb.safeNotVisited.append(neighbor)
                    

        if (stench and self.wumpusAlive) and not self.wumpusLocated:
            neighbors = self.kb.getNeighbors(currentKBSquare)

            for i in range(0, len(neighbors)):
              if not neighbors[i].visited:
                  self.kb.wumpusInfo.append(neighbors[i])
            # print item in wumpusInfo
            for item in self.kb.wumpusInfo:
                print(f"possible wumpus: {item.col, item.row}")
            #print(f"WumpusInfo: {self.kb.wumpusInfo}")
            if self.row + self.col == 0:
                print("Stench in 00, we want to shoot")
                self.shoot = True
                return ("shoot")
              
            print("A stench was sensed")
            # We are in a corner, therefore we can determine where the wumpus is.
            # Clear the wumpusInfo and add the square which the wumpus is in.
            if len(neighbors) == 2:
                if neighbors[0].visited:
                    print("We know that the wumpus is in square:", neighbors[1].col, neighbors[1].row)
                    self.wumpusLocated = True
                    self.kb.wumpusInfo.clear()
                    self.kb.wumpusInfo.append(neighbors[1])
                    return ""
                elif neighbors[1].visited:
                    print("We know that the wumpus is in square:", neighbors[1].col, neighbors[1].row)
                    self.wumpusLocated = True
                    self.kb.wumpusInfo.clear()
                    self.kb.wumpusInfo.append(neighbors[0])
                    return ""
                else: 
                    print("We are in a corner, therefore we shoot")
                    self.shoot = True
                    return "shoot"
            #else:
             #   for i in self.kb.wumpusInfo:
              #      for j in self.kb.wumpusInfo:
               #         if i == j:
                #            print("We have located the wumpus in:", j.col, j.row)
                 #           self.wumpusLocated = True
                  #          self.kb.wumpusInfo.clear()
                   #         self.kb.wumpusInfo.append(j)

          



  
# TODO: 
#      Check the current square for smell or breeze    
#      if currSquare has breeze, add a list of all adjacent squares to the kb.pitInfo list
#      if currSquare has stench, add a list of all adjacent squares to the kb.wumpusInfo list

#     
    def selectAction(self):
        print("\nselect action called")
        print("MoveCount:", self.moveCount)
        print("climb",self.climb)
        print("Shoot", self.shoot)
        self.moveCount += 1
        wumpusSquare = None
        currentKBSquare = self.kb.squares[self.col][self.row]
        self.visitedSquares.append(currentKBSquare)
        #if currentKBSquare not in self.wayBack:
         #   self.wayBack.append(currentKBSquare)
        if self.timeToGrab:
            self.timeToGrab = False
            self.hasGold = True
            for square in self.visitedSquares:
              print("Visited Square:", square.col, square.row)
              self.pathBack.append(square)
            self.pathBack.reverse()
            self.pathBack.pop(0)
            return "grab"
        
        if not self.wumpusAlive:
            print("\nThe wumpus is dead\n")
        # If the wumpus has been located, create a square with its location to 
        # compare with when moving.
        elif self.wumpusLocated:
            wumpusSquare = self.kb.wumpusInfo[0]
            print("We know that the wumpus is in square:", wumpusSquare.col, wumpusSquare.row)

        if self.climb:
            print("Climbing out")
            return "climb"

        # GIVE UP
        if (self.moveCount > 20 and not self.hasGold) or self.givingUp:
            #for item in self.wayBack:
             #   print("wayBack:", item.col, item.row)
            #time.sleep(10)
            print("\n", self.moveCount)
            if self.col == 0 and self.row == 0:
                return "climb"
            else:
                if not self.givingUp:
                    print("\nHigh moveCount")
                    for square in self.visitedSquares:
                        print("Visited Square:", square.col, square.row)
                        self.pathBack.append(square)
                    self.pathBack.reverse()
                    
                    self.givingUp = True
                if self.givingUp:
                    if self.col == 0 and self.row == 0:
                        return "climb"
                    else:
                        #nextMove = self.wayBack.pop()
                        nextMove = self.pathBack.pop(0)
                        self.kb.updatePlayerLocation(self.col, self.row, nextMove.col, nextMove.row)
                        self.col = nextMove.col
                        self.row = nextMove.row
                        print("Finding same way back, moving to:", self.col, self.row)
                        return "moveTo", self.col, self.row
            
          
          
        # If we have the gold, we try to get out by using the squares we have visited.
        if self.hasGold:
            print("\nI have the gold!")
            if self.col == 0 and self.row == 0:
                self.lastSquare = currentKBSquare
                print("Climbing out with the gold!")
                return "climb"
            else:
                # If we have the gold and are not in 00
                # Pop the next square of the pathBack list and move to it
                short = self.shortPath(self.pathBack, currentKBSquare)

                nextMove = self.pathBack.pop(0)
                self.kb.updatePlayerLocation(self.col, self.row, nextMove.col, nextMove.row)
                self.col = nextMove.col
                self.row = nextMove.row
                print("Finding same way back, moving to:", self.col, self.row)
                return "moveTo", self.col, self.row
        
        if (self.shoot and self.hasArrow) and self.wumpusAlive:
            self.hasArrow = False
            neighbors = self.kb.getNeighbors(currentKBSquare)
            neighbor = neighbors[0]
            print("Shooting toward a neighbor", neighbor.col, neighbor.row)
            # Shooting toward the first neighbor.
            return "shootToward", neighbor.col, neighbor.row

        if (currentKBSquare.stench and not currentKBSquare.breeze) and self.wumpusAlive:
            print("We have stench but not breeze, and the wumpus is still alive")
            if len(self.kb.wumpusInfo) == 1:
                print("We know where the wumpus is?")


        if currentKBSquare.gold and not self.hasGold:
            self.hasGold = True
            # Figure out the shortest way back to 00
            # Put the resulting path in self.pathBack for use when navigating 
            for square in self.visitedSquares:
              print("Visited Square:", square.col, square.row)
              self.pathBack.append(square)
            self.pathBack.reverse()
            self.pathBack.pop(0)
            for item in self.pathBack:
                print("pathback",item.col, item.row)
            return "grab"

        
        else:
            # Make a list of neighbors
            neighbors = self.kb.getNeighbors(currentKBSquare)
            visitedNeighbors = []

            while neighbors:
                # Append visiten neighbors to a list and remove them from the neighbors list.
                if neighbors[0].visited: 
                    visitedNeighbors.append(neighbors.pop(0))
                else:
                    inPitInfo = False
                    neighbor = False

                    # Visit the neighbors in the safeNotVisited list first
                    for i in range(0, len(neighbors)):
                        if neighbors[i] in self.kb.safeNotVisited:
                            neighbor = neighbors.pop(i)
                            break

                    if not neighbor:
                        neighbor = neighbors.pop(0)

                    # Check if the neighbor is in the pitInfo list.
                    if len(self.kb.pitInfo) != 0:
                        for list in self.kb.pitInfo:
                            for item in list:
                                if neighbor == item:
                                    print("here")
                                    inPitInfo = True
                    
                    
                    if (neighbor not in self.kb.wumpusInfo) and (not inPitInfo) and (neighbor != wumpusSquare):
                        self.kb.updatePlayerLocation(self.col,self.row,
                                                     neighbor.col,neighbor.row)
                        self.col = neighbor.col
                        self.row = neighbor.row
                        self.lastSquare = currentKBSquare
                        print("1moveTo", self.col, self.row)
                        return "moveTo",self.col,self.row
                    else:
                        # Go back to a previos square.
                        #if neighbor in inPitInfo and 
                        if len(visitedNeighbors) != 0:
                            goBack = visitedNeighbors.pop(0)
                            #self.wayBack.pop()
                            self.kb.updatePlayerLocation(self.col, self.row,
                                                        goBack.col, goBack.row)
                            self.col = goBack.col
                            self.row = goBack.row
                            self.lastSquare = currentKBSquare
                            print("2moveTo", self.col, self.row)
                            return "moveTo", self.col, self.row
                        # Shoot the arrow to find out where the wumpus is.
                        #elif len(visitedNeighbors) != 0 and currentKBSquare.stench:
                         #   print("3we are in the first square and have stench.")
                          #  return "shoot", neighbor.col, neighbor.row
            if not self.hasGold:
                print("No new squares were available.")
                #self.givingUp = True
                
                if len(visitedNeighbors) != 0:
                    nextSquare = visitedNeighbors.pop(0)
                    while nextSquare == self.lastSquare and (len(visitedNeighbors) != 0):
                        nextSquare = visitedNeighbors.pop(0)
                    self.kb.updatePlayerLocation(self.col, self.row,
                                                nextSquare.col, nextSquare.row)
                    self.col = nextSquare.col
                    self.row = nextSquare.row
                    self.lastSquare = currentKBSquare
                    print("3moveTo", self.col, self.row)
                
                return "moveTo", self.col, self.row
                
        # If all neighbors have been visited, climb out or just go walkabout.
        if self.col==0 and self.row==0:
            print("climb")
            return "climb"
        #nbr = random.choice(self.kb.getNeighbors(currentKBSquare))
        #self.kb.updatePlayerLocation(self.col,self.row,
        #                                 nbr.col,nbr.row)
        #self.col,self.row = nbr.col,nbr.row
        #print("0MoveTo", self.col, self.row )
        #return "moveTo",self.col,self.row 















  
class BraveFool(Player):  # will go boldly forward
    
    def selectAction(self):
        # Where am I?
        currentKBSquare = self.kb.squares[self.col][self.row]
        # Can I get the gold?
        if currentKBSquare.gold and not self.hasGold:
            self.hasGold = True
            return "grab"
        else:
            # Is there a neighbor I haven't visited?
            neighbors = self.kb.getNeighbors(currentKBSquare)
            while neighbors:
                if neighbors[0].visited: neighbors.pop(0)
                else:
                    # Let's go visiting
                    neighbor = neighbors.pop(0)
                    self.kb.updatePlayerLocation(self.col,self.row,
                                                 neighbor.col,neighbor.row)
                    self.col = neighbor.col
                    self.row = neighbor.row
                    return "moveTo",self.col,self.row
                
        # If all neighbors have been visited, climb out or just go walkabout.
        if self.col==0 and self.row==0:
            return "climb"
        nbr = random.choice(self.kb.getNeighbors(currentKBSquare))
        self.kb.updatePlayerLocation(self.col,self.row,
                                         nbr.col,nbr.row)
        self.col,self.row = nbr.col,nbr.row
        return "moveTo",self.col,self.row                   



class ScaredyCat(Player):  # prefers to be poor and alive
    def selectAction(self):  return "climb"




        
    
    


        
