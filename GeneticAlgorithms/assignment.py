# Assignment: create a genetic solution to the assignment problem.
# Read section 4.1.4 on page 126.

# 
import random

BOARD_SIZE = 4 # Use 4x4 boards, means we have 4 jobs and 4 people.
POPULATION_SIZE = 8 # How many boards are in the population? 
GENERATIONS = 40 # How many times will we cull, make children, and mutate?
MUTATION_FREQUENCY = 50 # What percentage of the time is there a mutation?
W1 = 20 # The weight we multiply cost by
W2 = 10 # The weight we multiply duplicate assignments by


PERSON1 = [9,1,4,5]
PERSON2 = [1,7,3,8]
PERSON3 = [5,4,1,2]
PERSON4 = [6,3,2,1]

# PERSON1 = [1,2,3,4]
# PERSON2 = [5,6,7,8]
# PERSON3 = [9,10,11,12]
# PERSON4 = [13,14,15,16]


ORIG_PERSON_LIST = [PERSON1, PERSON2, PERSON3, PERSON4]

# Job 1 will be pos 0 in the list
# Person one will be number 1 and it can be placed anywhere in the list
# What is the cost for each person doing each job?
# Then compare the cost of each person doing job 1 and pick one of them.

# Create a person with a name that is set elsewhere and an initial 
# cost of a random number between 1 and 10.


class Person:
    def __init__(self, name, costs):
        self.name = name
        # Make a list of the costs this person has for each job
        #self.cost = [random.randint(1,10) for i in range(0, BOARD_SIZE)]
        self.cost = costs

# Create a list of persons with 
def personList(boardSize):
    list = []
    for i in range(1, boardSize + 1):
        list.append(Person(i,ORIG_PERSON_LIST[i - 1]))
    return list
        

'''I think we can use this'''
class Board:
    def __init__(self):
        #self.list = [random.randint(1,BOARD_SIZE) for i in range(BOARD_SIZE)]
        # Pick a random person from the list for each position on the board. 
        # (A solution has only one of each)
        self.list = [random.choice(personList(BOARD_SIZE)) for i in range(BOARD_SIZE)]
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
    # def mutate(self):   
    #     if random.randint(1,100) < MUTATION_FREQUENCY:
    #         column = random.randint(1,BOARD_SIZE)
    #         #newValue = random.randint(1,BOARD_SIZE)
    #         personList = []
    #         for i in range(0, BOARD_SIZE):
    #             personList.append(self.list[i].name)
    #         #Make a set out of personList
    #         personSet = set(personList)
    #         #Find the difference in the length.
    #         duplicateCount = len(personList) - len(personSet)
    #         # Get a new random person and replace the person in a random job with it
    #         newPerson = random.choice(personList(BOARD_SIZE))
    #         self.list[column-1] = newPerson
    #         self.setValue()

    def mutate(self):   
        if random.randint(1,100) < MUTATION_FREQUENCY:
            column = random.randint(1,BOARD_SIZE)
            #newValue = random.randint(1,BOARD_SIZE)
            # Get a new random person and replace the person in a random job with it
            newPerson = random.choice(personList(BOARD_SIZE))
            self.list[column-1] = newPerson
            self.setValue()


# Look for conflicts, conflicts are bad

        

        '''Change the setValue method to work with the assignment problem'''
    # Hueristic for assignment problem is to take the two lowest cost for
    # the current job and compare them to the two lowest costs for the next job?

#Take a potential solution and judge how close it is to being good.
#Hueristic is: h(board) = W1cost + W2(something that measures duplicate people)
    def setValue(self): 
        # Find the value of cost
        self.value = 0
        cost = 0
        for i in range(0, BOARD_SIZE):
            cost = cost + self.list[i].cost[i]
          
        #Measure Duplciate People
        #Person List is a list of the name (number) of people
        personList = []
        for i in range(0, BOARD_SIZE):
            personList.append(self.list[i].name)
        #Make a set out of personList
        personSet = set(personList)
        #print(f"personSet: {personSet} \npersonList: {personList}" )
        #Find the difference in the length.
        duplicateCount = len(personList) - len(personSet)
      
        #Hueristic
        self.value = (W1 * cost) + (W2 * duplicateCount)
        #print(f"self.value: {self.value}")
        #print(f"Cost: {cost}")
        #print(f"duplicateCount: {duplicateCount}")


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
        #self.boards.sort(reverse = True, key = lambda x: x.value)
        for board in self.boards:
            board.setValue()
        self.boards.sort(reverse = False, key = lambda x: x.value)

    # If you have a large population, use boards[:5] to see the top 5.
    def printBestBoards(self):
        for board in self.boards[:5]: 
            #print(f"\nCurrent Board: {board.value}")
            newList = []
            for person in board.list:
                newList.append(person.cost)
            #print(board.list)
            print(newList,board.value//W1)
          
    '''Change this to a smarter culling procedure'''
    # Reduce the population size before adding in a new generation of
    # children boards.  This method removes the higher scoring half of
    # the population.
    def cull(self): 
        #self.boards = self.boards[POPULATION_SIZE//2:]
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
        children = []
        for kids in range(POPULATION_SIZE//2):
            '''change the choice of parents to a smarter approach'''
            board1 = random.choice(pop.boards)  
            board2 = random.choice(pop.boards)
            newChild = board1.makeChild(board2) 
            newChild.mutate() 
            children.append(newChild)
        pop.add(children)

    print("New generation:")
    pop.printBestBoards()        
        

def testCase(testNumber, expectedResult):
    print(f"\nTest {testNumber}")
    population = Population()

    for generations in range(GENERATIONS):
        population.cull()
        children = []
        for kids in range(POPULATION_SIZE//2):
            board1 = random.choice(population.boards)
            board2 = random.choice(population.boards)
            newChild = board1.makeChild(board2)
            newChild.mutate()
            children.append(newChild)
        population.add(children)

    boards = population.boards[5:]
    #boards2 = population.boards[:5]
    #boards2.reverse()

    for board in boards:
        #print(f"value of board: {board.value}")
        myList = []

        for person in board.list:
            myList.append(person.cost)
        #print(f"The person and their cost: {myList}")

    if boards[0].value == expectedResult:
        print(f"\nTest {testNumber} passed.")
        return True
    else:
        print(f"\nTest {testNumber} failed.")
        return False
        
    # for board in boards2:
    #     print(f"value of board (r): {board.value}")
        
def test():
    global PERSON1, PERSON2, PERSON3, PERSON4
    global ORIG_PERSON_LIST
    global POPULATION_SIZE
    global GENERATIONS
    PERSON1, PERSON2, PERSON3, PERSON4 = [1,1,1,1], [2,2,2,2], [3,3,3,3], [4,4,4,4]
    ORIG_PERSON_LIST = [PERSON1, PERSON2, PERSON3, PERSON4]
    testCase(1,10*W1)

    POPULATION_SIZE = 8
    testCase(2,10*W1)
    
    PERSON1, PERSON2, PERSON3, PERSON4 = [9,1,4,5], [1,7,3,8], [5,4,1,2], [6,3,2,1]
    ORIG_PERSON_LIST = [PERSON1, PERSON2, PERSON3, PERSON4]
    POPULATION_SIZE = 10
    testCase(3,4*W1)

    POPULATION_SIZE = 10
    testCase(4,4*W1)

    testNumber = 5
    testResult = True
    tries = 0
    while testResult:
        print(f"Population: {POPULATION_SIZE}")
        print(f"Generations: {GENERATIONS}")
        if not testCase(testNumber, 4*W1):
            if tries > 2:
                testResult = False
            else:
                POPULATION_SIZE += 1
            tries += 1

        if POPULATION_SIZE > 1 and tries < 1:
            POPULATION_SIZE -= 1
        if GENERATIONS > 1 and tries > 1:
            GENERATIONS -= 1
        
        testNumber += 1
    print(f"\nOptimal settings for Population and Generations are: {POPULATION_SIZE}, {GENERATIONS + 1}")


findGoodBoard()
#test()