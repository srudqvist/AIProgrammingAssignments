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

Some notes....

The wumpus world is a cave consisting of rooms connected by passageways. 
Lurking somewhere in the cave is the terrible wumpus, a beast that eats 
anyone who enters its room. The wumpus can be shot by an agent, but the 
agent has only one arrow. Some rooms contain bottomless pits that will 
trap anyone who wanders into these rooms (except for the wumpus, which 
is too big to fall in). The only mitigating feature of this bleak 
environment is the possibility of finding a heap of gold.

PEAS
Performance measurment: 
    -1000 for falling in pit, +1000 for getting the gold.
Environment:
    A nxn grid of rooms. Agent starts in [0,0].
    Location of gold and wumpus are random with uniform distribution.
    (not start) With probability of 0.2
Actuators:
    Constrictions:
        Cannot move through walls.
        Only has one arrow for the shot.
        Can only climb from square [1,1]
        Wumpus does not move.
    Moves:
        Forward, left (90), right (90)
    Actions:
        Grab - Pick up gold if in same square.
        Shoot - Shoot in the direction the agent is facing. The shot
                keeps going until it hits the wumpus or a wall.
        Climb - Climb out of the cage
    Death:
        Enter square with pit or live wumpus.
    Safe:
        Enter empty square or square w dead wumpus.
Sensors:
    Sensors that will give the agent information.

    Stench - When in the same or directly adjacent squares as the wumpus, a stench is perceived.
    Breeze - When in squares directly adjacent to a pit, a breeze is perceived.
    Glitter - When in same square as the gold, glitter is perceived.
    Bump - When walking into a wall, a bump is perceived.
    Scream - When the wumpus dies, a scream is perceived.
    Will be given in format [stench, breeze, glitter, bump, scream], if they are not perceived
    replace the name with None.

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

    def __init__(self, col, row):
        self.col = col
        self.row = row
        # These are declared here and set to "unknown"
        self.wumpus, self.stench = None, None
        self.pit, self.breeze = None, None
        self.gold, self.glitter = None, None

    def getSensors(self):
        return [self.stench, self.breeze, self.glitter]

    def getInfo(self):  # Report on the state of this square
        answer = ''
        # Information for wumpus.
        if self.wumpus:
            answer = answer + "W"
        # 1. Add the information for pit, gold, stench, and breeze.
        # Information for breeze.
        if self.pit:
            answer = answer + "P"
        if self.breeze:
            answer = answer + "B"
        # Information for gold.
        if self.glitter:
            answer = answer + "G"
        # Information for stench
        if self.stench:
            answer = answer + "S"
        return answer


class Board:

    # Create a new game board
    def __init__(self, dimension):

        # make the empty board
        self.dimension = dimension
        self.squares = []
        for col in range(dimension):
            thisCol = []
            for row in range(dimension):
                thisCol.append(Square(col, row))
            self.squares.append(thisCol)

        self.__placeWumpusAndStench()
        self.__placeGoldAndGlitter()
        self.__placePitsAndBreezes()

    # print the current state of each square on the board
    def printBoard(self):
        print("")
        for row in range(self.dimension):
            out = ""
            for col in range(self.dimension):
                square = self.squares[col][row]
                out = out+str(col)+str(row)+square.getInfo()+"**"
            print(out, "\n")

    def printBoard2(self):
        print()
        # Upperscore = "\u00AF"

        for row in range(self.dimension):
            out = ""
            if row == 0:
                out = out + "{:^2}{:^2}{:^4}{:>2}".format("|","\u00AF\u00AF "," \u00AF\u00AF","|")
                
            else:
                out = out + "{:^2}{:^2}{:^4}{:>2}".format("|","__ "," __","|")

            for col in range(self.dimension - 1):

                if row == 0:
                    out = out + "{:^2}{:^2}{:^4}{:>2}".format("|","\u00AF\u00AF "," \u00AF\u00AF","|")
                else:
                    out = out + "{:^2}{:^2}{:^4}{:>2}".format("|","__ "," __","|")
            out = out+ "\n"
            for col in range(self.dimension):
                if row == 0:
                    square = self.squares[col][row]
                    out = out + ("{:^2}{:^2}{:^3}{:>2}".format("|",f"{col}{row}  ",f"{square.getInfo()}","|"))
                else:
                    out = out + ("{:^2}{:^2}{:^4}{:>2}".format("|","   ","   ","|"))

            if row != 0:    
                out = out+ "\n"
                for col in range(self.dimension):
                    #out = out + ("{:^2}{:^2}{:^2}{:>2}".format("|","   ","   ","|"))
                    square = self.squares[col][row]
                    out = out + ("{:^2}{:^2}{:^3}{:>2}".format("|",f"{col}{row}  ",f"{square.getInfo()}","|"))

            if row == self.dimension - 1:
                out = out + "\n"
                for col in range(self.dimension):
                    out = out + "{:^2}{:^2}{:^4}{:>2}".format("|","__ "," __","|")

            print(out)
    # Return a list of the neighboring squares given col,row.
    def getNeighborList(self, col, row):
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
    def getNeighbors(self, aSquare):
        return self.getNeighborList(aSquare.col, aSquare.row)

    # Find a random square other than 0,0.
    def __randomSquareNot00(self):
        # 2. return a random square that is not 00
        randomCol = random.randint(1, DIMENSION -1)
        #print(f"Random Col: {randomCol}")
        randomRow = random.randint(1, DIMENSION -1)
        #print(f"Random Row: {randomRow}")

        # Check if the random numbers would generate square 00.
        if randomCol + randomRow != 0:
            randomSquare = self.squares[randomCol][randomRow]
            return randomSquare
        else:
            self.__randomSquareNot00()

    def __placeWumpusAndStench(self):
        wsquare = self.__randomSquareNot00()
        wsquare.wumpus = True
        print(f"wumpus col: {wsquare.col}")
        print(f"wumpus row: {wsquare.row}")
        # 3. Place the stenches.
        # Stenches go in all the neighbors of where the wumpus is.
        neighbors = self.getNeighbors(wsquare)
        for neighbor in neighbors:
            neighbor.stench = True
        #wsquare.stench = False

    def __placeGoldAndGlitter(self):
        # 4. Randomly place the gold and glitter.
        # Places the gold in a random square and then the glitter
        # in that same square.
        goldSquare = self.__randomSquareNot00()
        goldSquare.gold = True
        goldSquare.glitter = True
        
    def __placePitsAndBreezes(self):
        # Randomly place pits but not in 0,0.
        psquare = self.__randomSquareNot00()
        psquare.pit = True
        #pit also has a breeze
        psquare.breeze = True

        # put breezes on the neighbors of the pits
        neighbors = self.getNeighbors(psquare)
        for neighbor in neighbors:
            neighbor.breeze = True

        '''
        for col in range(DIMENSION):
            for row in range(DIMENSION):
                if col > 0 or row > 0:
                    current = self.squares[col][row]
                    if random.randint(1, PIT_PROB_FACTOR) == 1:
                        # 20% of the time if prob factor is 5
                        current.pit = True
                        
                            '''




def main():  # generates one game board
    # 5. Generate and print 5 boards.
    gameBoard = Board(DIMENSION)
    #gameBoard.printBoard()
    gameBoard.printBoard2()
    for i in range(6):
        print(f"\nBoard {i}")
        gameBoard = Board(DIMENSION)
        gameBoard.printBoard2()



main()
