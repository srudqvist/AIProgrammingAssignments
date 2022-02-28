'''Make a board 
Dr. Browning January 31,2021'''
# Create a game board in which each square is marked as safe or unsafe.
# Assignment: find a path from any square back to 00 using only safe squares.
# Board rows and columns are numbered 0-3.
# Square 0,0 is in the upper left corner.

import random

DIMENSION = 4
BIG_NUMBER = 2*DIMENSION*DIMENSION
UNSAFE_PROB_FACTOR = 4 #= 100/%; 1 in this number of squares are unsafe

# Square class objects have five attributes: row, column, safe (Boolean), pathCost and parent.
class Square:
    def __init__(self,row,col, pathCost = BIG_NUMBER, parent = None):
        self.row = row
        self.col = col
        self.safe = True 
        self.pathCost = pathCost
        self.parent = parent
        if random.randint(1,UNSAFE_PROB_FACTOR)==1:
          #25% of the time if probability factor is 4
          self.safe = False

    # isSafe is a getter method for if the square is safe
    def isSafe(self): 
        return(self.safe)

    # setPathCost is a setter method for path cost
    def setPathCost(self, newCost):
      self.pathCost = newCost

    # getPathCost is a getter method for path cost
    def getPathCost(self):
      return self.pathCost

    # setParent is a setter method for parent
    def setParent(self, newParent):
      self.parent = newParent

    # getParent is a getter method for parent
    def getParent(self):
      return self.parent


BIG_SQUARE = Square(-1,-1, BIG_NUMBER, None)

# A Board object has a squares attribute, which is a 4x4 array
# of squares.  One method prints the board, another allows the
# user to set the safe/unsafe value for each square on the board.
class Board:
    # Constructor for board class
    def __init__(self):
        # Make the board.
        self.squares = []
        for row in range(DIMENSION):
            thisRow = []
            for col in range(DIMENSION):
                thisRow.append(Square(row,col))
            self.squares.append(thisRow)
 
    # Function to print out the board
    def printBoard(self):
        for row in range(DIMENSION):
            out = '** '
            for col in range(DIMENSION):
                square = self.squares[row][col]
                if square.isSafe():
                    out=out+" safe "+" ** "
                else:
                    out=out+" dark "+" ** "
            print(out)

    # setSafes allows the user to set the safe/unsafe value for each
    # square on the board.  Example:
    # myboard.setSafes([[False,False,True,True],[False,True,False,True],
    #                   [False,False,True,True],[False,False,False,True]])
    def setSafes(self,newSafes):
        for col in range(DIMENSION):
            for row in range(DIMENSION):
                self.squares[row][col].safe = newSafes[row][col]        

    # Function to get a list of neighbors from a given square
    def neighborList(self, givenSquare):
        neighborList = []
        givenRow = givenSquare.row
        givenCol = givenSquare.col
        
        # gets the upper neighbor
        if givenRow > 0:
          neighborList.append(self.squares[givenRow-1][givenCol])

        # gets the lower neighbor
        if givenRow < DIMENSION-1:
          neighborList.append(self.squares[givenRow+1][givenCol])

        # gets the left neighbor
        if givenCol > 0:
          neighborList.append(self.squares[givenRow][givenCol-1])

        # gets the right neighbor
        if givenCol < DIMENSION-1:
          neighborList.append(self.squares[givenRow][givenCol+1])

        # return list of neighbors
        return neighborList

    def shortestPath(self, startSquare):
      incompleteList = []
      
      # if location or square -- isn't safe, returns empty list
      if startSquare.isSafe == False:
        return []
      elif self.squares[0][0].isSafe == False:
        return []
      
      # Copy pointers to the safe squares into an incomplete list
      for row in self.squares:
        for square in row:
          if square.isSafe() == True:
            incompleteList.append(square)

      #Set the path cost of the current location to 0, and its parent to itself
      startSquare.setPathCost(0)
      startSquare.setParent(startSquare)

      answerList = []

      # While there are safe squares
      while incompleteList != []:
        smallestCostSquare = BIG_SQUARE

        # for loop for each square in the safe square list
        for square in incompleteList:

          #Find the square with the smallest path cost
          if square.getPathCost() < BIG_SQUARE.getPathCost():
            smallestCostSquare = square

        #If the smallest path cost is BIG_NUMBER, return an empty list
        if smallestCostSquare.getPathCost() == BIG_NUMBER:
          return []
        
        answerList.append(smallestCostSquare)
        if smallestCostSquare == self.squares[0][0]:
          return answerList
        
        # take out the square with the smallest cost
        incompleteList.remove(smallestCostSquare)

        neighbors = self.neighborList(smallestCostSquare)

        #check neighbor safety
        for neighbor in neighbors:
          if neighbor.isSafe() == False:
            neighbors.remove(neighbor)
      
        # for loop for each neighbor in the neighbor list of the smallest costing square
        # in order to get the smallest path cost
        for neighbor in neighbors:
          if neighbor.getPathCost() > smallestCostSquare.getPathCost()+1:
            neighbor.setPathCost(smallestCostSquare.getPathCost()+1) 
            neighbor.setParent(smallestCostSquare)
      
      return answerList
    
    # Function to get the shortest path
    def getActualAnswers(self, bunchaSquares):
      actualAnswers = []
      if len(bunchaSquares) == 0:
        print("There is no path")
        return actualAnswers
      startSquare = bunchaSquares[0]
      endSquare = bunchaSquares[len(bunchaSquares)-1]
      actualAnswers.append(endSquare)
      currentSquare = endSquare
      
      while bunchaSquares != []:
        currentParent = currentSquare.getParent()
        if currentParent in actualAnswers:
          actualAnswers.remove(currentSquare)
        else:
          actualAnswers.append(currentParent)
          if currentParent == startSquare:
            return actualAnswers
        currentSquare = currentParent
        
      return actualAnswers

# Function to test the list of neighbors
def testNeighborList():
    myboard = Board()
    myboard.printBoard()
    for square in myboard.neighborList(myboard.squares[3][2]):
        print(square.row,square.col,square.safe)



# [00] [01] [02] [03]
# [10] [11] [12] [13]
# [20] [21] [22] [23]
# [30] [31] [32] [33]
# Tests
# Path 1 is up and then left
path1 = [[True,True,True,True],[False,True,False,True],[False,False,True,True],[False,False,False,True]]
# Path 2 left then up
path2 = [[True,False,False,False],[True,False,False,False],[True,False,False,False],[True,True,True,True]]
# Path 3 All are true
path3 = [[True,True,True,True],[True,True,True,True],[True,True,True,True],[True,True,True,True]]
# Path 4 All are false
path4 = [[False,False,False,False],[False,False,False,False],[False,False,False,True],[False,False,False,False]]
# Path 5 is goal and start true, rest is false
path5 = [[True,False,False,False],[False,False,False,False],[False,False,False,True],[False,False,False,True]]
# Path 6 is zig-zags
path6 = [[True,False,False,False],[True,True,False,False],[False,True,True,False],[False,False,True,True]]
# Path 7 is Diagonal
path7 = [[True,False,False,False],[False,True,False,False],[False,False,True,False],[False,False,False,True]]

# for testing 8*8
path8 = [[True,True,True,True,True,True,True,True],[False,False,False,False,False,False,False,True],[False,False,False,False,False,False,False,True],[False,False,False,False,False,False,False,True],[False,False,False,False,False,False,False,True],[False,False,False,False,False,False,False,True],[False,False,False,False,False,False,False,True],[False,False,False,False,False,False,False,True]]


# Run specific tests.
def testCaseA(testNumber, path, expected):
  print(f"\nTest {testNumber}")
  myboard = Board()
  ansList = []
  # Set the safe path.
  myboard.setSafes(path)
  answers = myboard.shortestPath(myboard.squares[DIMENSION -1][DIMENSION -1])
  print(f"  Answer for test {testNumber}: ")
  actual = myboard.getActualAnswers(answers)
 
  for i in range(0,len(actual)):
      ans = actual.pop()
      ansString = str(ans.row)
      ansString2 = str(ans.col)
      ansList.append(ansString + ansString2)
      print(f"  {ans.row}, {ans.col}")
  if ansList != expected:
    print(f"  Test {testNumber} failed.")
  else:
    print(f"  Test {testNumber} passed.")

# Test multiple boards
def testCaseB(numBoards):
  print("\nTest B")
  for i in range(numBoards):
    myboard = Board()
    answers = myboard.shortestPath(myboard.squares[DIMENSION -1][DIMENSION -1])
    myboard.printBoard()
    print(f"  Answer for test {i + 1}: ")
    actual = myboard.getActualAnswers(answers)
    for i in range(0,len(actual)):
      ans = actual.pop()
      print(f"  {ans.row}, {ans.col}")

# Test with different dimensions, the path parameter is optional.
def testCaseC(testNumber, dimension, path = None):
  print("\nTest C")
  # Reach the global scope to set the dimension.
  global DIMENSION
  DIMENSION = dimension
  myboard = Board()
  if path:
    myboard.setSafes(path)
  answers = myboard.shortestPath(myboard.squares[DIMENSION -1][DIMENSION -1])
  myboard.printBoard()
  print(f"  Answer for test {testNumber}: ")
  actual = myboard.getActualAnswers(answers)
  for i in range(0,len(actual)):
    ans = actual.pop()
    print(f"  {ans.row}, {ans.col}")

def test():
  testCaseA(1, path1, ["33", "23", "13", "03", "02", "01", "00"])
  testCaseA(2, path2, ["33", "32", "31", "30", "20", "10", "00"])
  testCaseA(3, path3, ["33", "32", "31", "30", "20", "10", "00"])
  testCaseA(4, path4, [])
  testCaseA(5, path5, [])
  testCaseA(6, path6, ["33", "32", "22", "21", "11", "10", "00"])
  testCaseA(7, path7, [])
  testCaseB(3)
  testCaseC(1,4, path1)
  testCaseC(2,3)
  testCaseC(3,2)
  testCaseC(5,8, path8)
  



# Main Function
def main():
    # Generate a Board
    myboard = Board()

    # Set the values on a board and print it.
    myboard.setSafes([[True,True,True,True],[False,True,False,True],[False,False,True,True],[False,False,False,True]])
    myboard.printBoard()

    print("SHORTEST PATH: ")                 
    answers = myboard.shortestPath(myboard.squares[3][3])
    actual = myboard.getActualAnswers(answers)
    for i in range(0,len(actual)):
      ans = actual.pop()
      print(ans.row, ans.col)
    
#testNeighborList()
#main()
test()

