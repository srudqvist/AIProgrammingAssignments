'''
Main Function for Wumpus World            
Dr. Browning January 9,2022

I have six files for this game:
WWWMainFunction.py    the code to play the game
WWWPlayer.py          the code for the player superclass
WWWKnowledgeBase.py   the code for the kb for the player
WWWBoardGenerator.py  the code to generate the game boards
and my own players WWWSmartyPants.py and WWGentleWinner.py
'''

from WWPlayer import *
#from WWSmartyPants import *
#from WWGentleWinner import *
#from WWPlayer import *
#from WWPlayerNoPrint import *
#from WWPlayerNoPrint2 import *
from BestBackUp import *

NUMBEROFGAMES = 10000
REPORTINGINTERVAL = 5000
gameBoard = Board(DIMENSION)
#gameBoard.printBoard()
#myPlayer = SmartyPants()
#myPlayer = BraveFool()
#myPlayer = ScaredyCat()
#myPlayer = Human()

def competition(numberOfGames,reportInterval):
    #competitors = [SmartyPants,GentleWinner,ScaredyCat,BraveFool]
    competitors = [ScaredyCat,BraveFool, JimmyDean]
    runningTotal=[0]*len(competitors)
    for vier in competitors:
        runningTotal[competitors.index(vier)]=0
    for game in range(numberOfGames):
        gameBoard = Board(DIMENSION)
        #gameBoard.printBoard()
        for vier in competitors:
            score = oneGame(gameBoard,vier(),printKBs=False)
            runningTotal[competitors.index(vier)]+=score
        if (game+1)%reportInterval == 0:
            print("\nAfter",game+1,"games, the average scores are:")
            for vier in competitors:
                total = runningTotal[competitors.index(vier)]
                print(vier,int(total/(game+1)))
        

def singleGame():
    gameBoard = Board(DIMENSION)
    #myPlayer = Human()
    myPlayer = JimmyDean()
    print("score =", oneGame(gameBoard,myPlayer,True))
    
def oneGame(gameBoard,myPlayer,printKBs=False): #plays one game given a board and a player
    #print("\n\nNew Game")
    if printKBs:
        gameBoard.printBoard()
        myPlayer.kb.printBoard()

    # Initialize the game.
    playerCol = 0
    playerRow = 0        
    hasGold = False
    hasArrow = True
    score = 0
    gameOver = False
    screamHeard = False
    wumpusAlive = True

    # Main event loop.
    while not gameOver:
        # Send sensors to player and get move back
        sensors = gameBoard.squares[playerCol][playerRow].getSensors()
        sensors = sensors + [screamHeard]
        screamHeard = False # reset this each time
        nextMove=myPlayer.move(sensors)

        # next move can be moveTo, climb, grab, or shootToward
        if nextMove[0] == "moveTo":
            score = score - 1
            newCol = nextMove[1]
            newRow = nextMove[2]
            
            #make sure moving to adjacent square
            # note - should also check newCol and newRow are in 0..3
            if ((playerCol==newCol and
                 playerRow-newRow in [1,-1])
                or (playerRow == newRow and
                    playerCol-newCol in [1,-1])):
                playerCol = newCol
                playerRow = newRow               
                #if wumpus or pit is in new location, you lose.
                if ((gameBoard.squares[playerCol][playerRow].wumpus and
                     wumpusAlive) or
                    gameBoard.squares[playerCol][playerRow].pit):
                    score = score-1000
                    gameOver = True
                    if printKBs:
                        if gameBoard.squares[playerCol][playerRow].pit:
                            print("Fell into a pit")
                        else:
                            print("Eaten by Wumpus")

        # If move is climb, make sure player is in 0,0.
        elif nextMove == "climb":
            score = score - 1
            if playerCol==0 and playerRow==0:
                gameOver = True
                if hasGold:
                    score = score+1000

        # if move is grab, make sure player is with gold.
        elif nextMove == "grab":
            score = score - 1
            if gameBoard.squares[playerCol][playerRow].gold:
                hasGold = True

        # if move is shoot, make sure player has an arrow
        elif nextMove[0] == "shootToward":
            score = score - 1
            if hasArrow:
                score = score -10
                hasArrow = False # only get one arrow
                
                # Determine if scream is heard or not.
                # see if shooting from playerCol, playerRow 
                # toward nextMove[1],nextMove[2] eventually
                # hits the wumpus
                arrowCol = nextMove[1]
                arrowRow = nextMove[2]
                colChange = nextMove[1] - playerCol
                rowChange = nextMove[2] - playerRow
                hit = False
                # Keep arrow on game board.
                while (0<=arrowCol<DIMENSION and
                       0<=arrowRow<DIMENSION and not hit):
                    # if arrow is in wumpus's square,it's a gonner
                    if gameBoard.squares[arrowCol][arrowRow].wumpus:
                        screamHeard = True
                        wumpusAlive = False
                        hit=True
                    else: # otherwise arrow keeps flying
                        arrowCol = arrowCol+colChange
                        arrowRow = arrowRow + rowChange
        '''
        "uncle" move is useful in testing while player
        is in development but will not be used in the contest:
        
        elif nextmove == "uncle":
            score = score - 1000000
            gameOver = True
        '''
        
        if printKBs:
            myPlayer.kb.printBoard()
    return(score)

#singleGame()

competition(NUMBEROFGAMES,REPORTINGINTERVAL)
