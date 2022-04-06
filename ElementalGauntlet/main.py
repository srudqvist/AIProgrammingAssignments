'''
AI Elemental Gauntlet Project
main program
@auhors: Hana, Madi, Cameron
Date Created: 04/15/2020
Date Last Modified: 05/13/2020

Change log
April 12, 2021 Carol Browning
Changed names of files and player AIs
March 11, 2022 Carol Browning
World now tracks player data independently
'''

# Main script for accepting input on game settings.

from pDonaldDuck import DonaldDuckAI # Starter code for playerAI subclass
from pHungryHippo import HungryHippoAI
from pInteractive import InteractiveAI

import random
from world import World
from display import Display
import time

REPORTING_INTERVAL=1000

def getPlayer(display):
    # get the player AI
    while True:
      playername = display.askUser("Which player? (E.g., DonaldDuck,HungryHippo,Interactive)")
      if(playername.lower() == "donaldduck"):
        player = DonaldDuckAI()
        break
      elif(playername.lower() == "hungryhippo"):
        player = HungryHippoAI()
        break
      elif(playername.lower() == "interactive"):
        player = InteractiveAI()
        break
    return player

def resetPlayer(name):
    if name == "DonaldDuck":
        return(DonaldDuckAI())
    elif name == "HungryHippo":
        return(HungryHippoAI())
    elif name == "Interactive":
        return(InteractiveAI())

def main():
  display = Display() 
  query = display.askUser("Normal game or run test bench?")
  averageTime = []
  if "normal" in query.lower():
    player = getPlayer(display)
    printingOn = "y" in display.askUser("Printing on(y/n)?  ").lower()
    world = World(printingOn,"normal")
    world.gameStart(player,display)
  if "test" in query.lower():
    start = time.time()
    gamesQuery = int(display.askUser("How many games do you want to play?"))
    games = 0
    totalScore = 0
    world = World()
    player = getPlayer(display)
    display.tellUser("********************************")
    display.tellUser(player.name+" is now playing!")
    while games < gamesQuery:
      world = World()
      world.gameStart(player,display)
      games += 1
      if games%REPORTING_INTERVAL==0:
          display.tellUser("Now playing game "+str(games))
          display.tellUser("Average score per game "+str(int(totalScore/games)))
      totalScore += world.score
      averageTime.append(world.time)
      player = resetPlayer(player.name)
        
    averageTime.append(world.time)
    end = time.time()
    
    display.tellUser("Total score was: "+str(totalScore))
    display.tellUser("The average score per game was: "+str(totalScore/gamesQuery))
    display.tellUser("The total average time to make a decision was: " + str(sum(averageTime)/len(averageTime)) + " seconds")
    display.tellUser("Total time to test was: "+ str(end - start) + " seconds.")

if __name__ == "__main__":
  main()
