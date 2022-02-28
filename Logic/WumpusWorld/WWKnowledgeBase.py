'''
Knowledge Base Class for Wumpus World            
Dr. Browning January 9, 2022

Each player will use a knowledge base to track what is known
about the game board and make inferences.
'''

import random
from WWBoardGenerator import *

#Create a blank square for the knowledge base
class KBSquare(Square):    
    def __init__(self,col,row):
        super().__init__(col,row)
        self.player=False
        self.visited,self.safe = False,None
        self.pitInfo = []
        self.wumpusInfo = []
        
    #Report on the knowledge of this square
    def getInfo(self): 
        answer = super().getInfo()
        if self.player: answer = answer + "player"
        if self.visited: answer = answer +"V"
        if self.safe: answer = answer + "safe"
        #return "{:^25}".format(answer)
        return answer
     
class KnowledgeBase(Board):
    
    # Create a board for tracking information as we learn.
    def __init__(self, dimension): 
        
        # Make the empty board.
        self.dimension = dimension
        self.squares = []
        for col in range(dimension):
            thisCol = []
            for row in range(dimension):
                thisCol.append(KBSquare(col,row))
            self.squares.append(thisCol)

        # Useful lists for reasoning.
        self.pitInfo = [] # a list of lists of possible places 
        self.wumpusInfo = [] # a list of lists of possible places
        self.safeNotVisited = [] # a list of safe squares to explore

        # Initialize player to square 00.
        self.squares[0][0].player = True
        self.squares[0][0].safe = True
        self.squares[0][0].visited = True
    
    # printBoard method is inherited, as are getNeighborList
    # and getNeighbors of a square.

    def updatePlayerLocation(self,oldCol,oldRow,newCol,newRow):
        self.squares[oldCol][oldRow].player = False
        self.squares[newCol][newRow].player = True
        self.squares[newCol][newRow].visited = True

    def updateStench(self,col,row):
        self.squares[col][row].stench = True
        
    def updateBreeze(self,col,row):
        self.squares[col][row].breeze = True
        
    def updateGlitter(self,col,row):
        self.squares[col][row].glitter = True
        self.squares[col][row].gold = True
        
def main(): #creates a kb and prints it out.
    kb = KnowledgeBase(DIMENSION) 
    kb.printBoard()
    
#main()
        
