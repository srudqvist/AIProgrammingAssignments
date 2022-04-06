'''
Genetic algorithm for n queens
For A.I. class
Dr. Browning,
March 3,2020

Updates March 4, 2020: fix the setValue method; value updates for
   children; removed magic 8's.

Updates March 18, 2021: clarified comments; fix the setValue
   method further.  Also played with the constant values.
'''

from graphics import *
import random

# Identify constants.
'''Can get excellent results using the constants 8, 50, 100, 70.
How can we make better choice so we can minimize population size
and number of generations and still get excellent results?
'''
BOARD_SIZE = 8 # Use 8x8 boards
POPULATION_SIZE = 10 # How many boards are in the population? Original 10, our change: 30
GENERATIONS = 25 # How many times will we cull, make children, and mutate? Original 20, our change: 100
MUTATION_FREQUENCY = 70 # What percentage of the time is there a mutation? Original 20, our change: 70

# The model of a game board is a list of numbers 1-8.  The first number
# indicates the row of the queen in column 1, second for column 2, etc.
# A random starting configuration is provided.  

class Board:
    
    # A board consists of a list of row numbers for the queens and maintains
    # the value of the heuristic function.
    def __init__(self): #Create a new game board
        self.list = [random.randint(1,BOARD_SIZE) for i in range(BOARD_SIZE)]
        self.value = 0
        self.setValue()

    # Each board has a makeChild method that takes a second existing board.
    # It generates a split point and then creates a new board that consists of
    # the first part of the current board, up to and including the split point,
    # and the second part of the second board, from the split point on.
    def makeChild(self,board2):
        ''' Change the split point range for different results.'''
        splitPoint = random.randint(1,BOARD_SIZE-1)  
        board = Board()
        board.list = self.list[:splitPoint]+board2.list[splitPoint:]
        self.setValue()
        return board

    # Determine if this board should mutate. If so, change a random column 
    # to a random new value.
    ''' Change the mutation frequency for different results.'''
    def mutate(self):   
        if random.randint(1,100) < MUTATION_FREQUENCY:
            column = random.randint(1,BOARD_SIZE)
            newValue = random.randint(1,BOARD_SIZE)
            self.list[column-1]=newValue
            self.setValue()


    # The setValue method computes the heuristic = the number of pairs
    # of queens that can't capture each other on this board.
    '''Is this code correct??'''
    def setValue(self): 
        n = BOARD_SIZE
        # Best possible value for 8 queens board is 28. Why?
        self.value = n*(n-1)//2
        # Check each possible pair of queens.
        for i in range(n):
            for j in range(i+1,n):
                difference = self.list[i]-self.list[j]
                if difference == 0:
                    # These two queens are on the same row.
                    self.value = self.value - 1
                elif abs(difference) == j-i:
                    # These two queens are on the same diagonal.
                    self.value = self.value - 1 

# The population consists of a number of boards, sorted in decreasing order
# of heuristic value.
class Population:

    # Create a random population.
    def __init__(self): 
        self.boards = [Board() for i in range(POPULATION_SIZE)]
        self.sortBoards()

    # Sort the population in decreasing order by value of the heuristic
    # function.    
    def sortBoards(self): 
        self.boards.sort(reverse = True, key = lambda x: x.value)

    # If you have a large population, use boards[:5] to see the top 5.
    def printBestBoards(self):
        for board in self.boards[:5]: 
            print(board.list,board.value)

    '''Change this to a smarter culling procedure'''
    # Reduce the population size before adding in a new generation of
    # children boards.  This method removes the lower scoring half of
    # the population.
    def cull(self): 
        self.boards = self.boards[:POPULATION_SIZE//2]

    # When we add a collection of children to the population, we then need
    # to resort the boards. Here children is a list of children.
    def add(self,children):
        self.boards = self.boards + children
        self.sortBoards()

# Here is the main program.  Create a population.  For several generations,
# cull, generate children, and consider mutations.  Print the initial 
# population best boards and the final population best boards.  
def findGoodBoard():
    pop = Population()
    pop.printBestBoards()

    for gens in range(GENERATIONS): 
        pop.cull()
        pop.cull()

        children = []
        for kids in range(POPULATION_SIZE//2):
            '''change the choice of parents to a smarter approach'''
            board1 = pop.boards[0]
            board2 = pop.boards[1]
            # board1 = random.choice(pop.boards)  
            # board2 = random.choice(pop.boards)
            newChild = board1.makeChild(board2) 
            newChild.mutate() 
            children.append(newChild)
        pop.add(children)



    print("New generation:")
    pop.printBestBoards()        
        
     
findGoodBoard()

