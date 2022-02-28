'''
Wumpus World Board Generator
Dr. Browning January 9,2022

A board object is a 2d array of square objects, with
column and row numbers as follows:
  00 10 ...
  01 11
  ...

The player is initially in square 00.  The wumpus is in a random
square other than 00, as is the gold.  Each square other than 00
has a chance of having a pit.  Squares neighboring the wumpus
have a stench, and squares neighboring a pit have a breeze.  The
square with the gold has glitter.
'''

import random

DIMENSION = 4

# FACTOR = 100/%. FACTOR = 5 means 1 in 5 squares are pits,
# so each square has a 20% probability of being a pit.
PIT_PROB_FACTOR = 5

# Create a blank square for the board with Boolean attributes
# that tell which are present: player, wumpus, stench, pit,
# breeze, gold, glitter.

class Square:
    
    def __init__(self,col,row):
        self.col = col
        self.row = row
        #These are declared here and set to "unknown"
        self.wumpus, self.stench = None,None
        self.pit, self.breeze = None, None
        self.gold,self.glitter = None,None
        
    def getSensors(self):
        return [self.stench,self.breeze,self.glitter]
    
    def getInfo(self): #Report on the state of this square
        answer = ''
        if self.wumpus: answer = answer + "W"
        if self.pit: answer = answer + "P"
        if self.gold: answer = answer + "GG"
        if self.stench: answer = answer + "S"
        if self.breeze: answer = answer + "B"
        return answer
         
class Board:
    
    #Create a new game board
    def __init__(self, dimension): 
        
        #make the empty board
        self.dimension = dimension
        self.squares = []
        for col in range(dimension):
            thisCol = []
            for row in range(dimension):
                thisCol.append(Square(col,row))
            self.squares.append(thisCol)

        self.__placeWumpusAndStench()
        #self.__placeWumpusAndStenchTest()
        self.__placeGoldAndGlitter()
        self.__placePitsAndBreezes()
        
    #print the current state of each square on the board
    def printBoard(self):
        print("")
        for row in range(self.dimension):
            out=""
            for col in range(self.dimension):         
                square = self.squares[col][row]
                out=out+str(col)+str(row)+square.getInfo()+"**"
            print(out, "\n")
            
    # Return a list of the neighboring squares given col,row.
    def getNeighborList(self,col,row):
        neighborlist = []
        if row > 0:
            neighborlist.append(self.squares[col][row-1])
        if row < self.dimension-1:
            neighborlist.append(self.squares[col][row+1])
        if col > 0:
            neighborlist.append(self.squares[col-1][row])
        if col < self.dimension-1:
            neighborlist.append(self.squares[col+1][row])
        return neighborlist
    
    # return a list of the neighboring squares given a square.
    def getNeighbors(self,aSquare):
        return self.getNeighborList(aSquare.col,aSquare.row)

    # Find a random square other than 0,0.
    def __randomSquareNot00(self):
        col = random.randint(0,DIMENSION-1)
        row = random.randint(0,DIMENSION-1)
        while col==0 and row==0:
            col = random.randint(0,DIMENSION-1)
            row = random.randint(0,DIMENSION-1)
        return self.squares[col][row]
        
    def __placeWumpusAndStench(self):
        wsquare = self.__randomSquareNot00()
        wsquare.wumpus = True
        for square in self.getNeighbors(wsquare):
            square.stench = True
          
    def __placeWumpusAndStenchTest(self):
        # place the wumpus in square 10
        wsquare = self.squares[0][2]
        wsquare.wumpus = True
        for square in self.getNeighbors(wsquare):
            square.stench = True
          
    def __placeGoldAndGlitter(self):
        gsquare = self.__randomSquareNot00()
        gsquare.gold = True
        gsquare.glitter = True

    def __placePitsAndBreezes(self):
        # Randomly place pits but not in 0,0.
        for col in range(DIMENSION):
          for row in range(DIMENSION):
              if col>0 or row>0:
                current = self.squares[col][row]
                if random.randint(1,PIT_PROB_FACTOR)==1:
                    #20% of the time if prob factor is 5
                    current.pit = True
                    for square in self.getNeighbors(current):
                        square.breeze=True
        
def main(): #generates and prints one game board
    gameBoard = Board(DIMENSION)
    gameBoard.printBoard()

#main()
        
