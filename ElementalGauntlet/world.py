'''
AI Elemental Gauntlet Project
World Class
keeps track of enemies and players' status and calculate the score

@authors: Hana, Madi, Cameron
Date Created: 04/15/2020
Date Last Modified: 05/12/2020

Change log - changes by Carol Browning
April 12, 2021 Change names of files and player AIs
March 10, 2022 Separated code more in model(World)view(Display)controller(main)
March 11, 2022 World now tracks player data independently
March 12, 2022 Created printing options
'''

import random

from enemy import Enemy

from pDonaldDuck import DonaldDuckAI # Starter code for playerAI subclass
from pHungryHippo import HungryHippoAI
from pInteractive import InteractiveAI

DAMAGE = 100
SPECIALDAMAGE = 200
SPECIALCOST= 20
HP = 1000
MANA = 100
NECTAR = 8
ETHER = 5

class World():
  def __init__(self,printingOn=False,query="test"):
    self.score = 0
    self.isOver = False
    self.turn = 1
    self.lastDamage = 0  # the last damage that the enemy took
    self.enemyNum = 15
    self.time = 0
    self.playerhp=HP
    self.playermp = MANA
    self.playerether = ETHER
    self.playernectar=NECTAR
    self.printingOn=printingOn
    self.justOneGame = query == "normal"
    
  def calcScore(self, enemyNum, hitPoints, manaPoints):
    # Returns score for how the player AI fought against enemies, equal to
    # the number of enemies defeated * 200 + remaining HP + remaining MP
    score = (15-enemyNum)*200 + hitPoints + manaPoints
    return score
  
  # This function returns the new instance object of Enemy class
  def getEnemy(self):
    enemy = Enemy(self.printingOn)
    return enemy

  # This method determines whether and which item is dropped
  def dropItem(self,display):
    itemList = ["ether","nectar",'']
    index = random.randrange(0, len(itemList))
    if(itemList[index] == "ether" or itemList[index] == "nectar"):
      if self.printingOn:
        display.tellUser("The enemy dropped "+itemList[index]+"!")
    return itemList[index]

  # Monitor the hitpoints of the player
  def playerDamage(self, damage):
    # When the player takes damage, subtract the damage
    # taken from the total HP, setting the current HP to that new number.
    self.playerhp = self.playerhp - damage
    if(self.playerhp<=0):
      self.playerhp = 0

  # Monitor the items the player picks up
  def playerTake(self, item):
    if(item.lower() == "nectar"):
      #add one nectar to the information about the player
      self.playernectar = self.playernectar + 1 
    if(item.lower() == "ether"):
      # add an ether to the information about the player
      self.playerether = self.playerether + 1 

  def playerConsume(self, itemType):
    # Update the information about the player when something is consumed.
    # If consume nectar, add back HP.
    # If consume ether, add back MP.
    # If player does not have the item, nothing is done.
    # Cannot exceed initial limits of HP or MP.
    
    if (itemType.lower() == "nectar" and self.playernectar > 0):
      #remove one nectar from the information about the player
      self.playernectar -= 1
      #the nectar adds back half of total hp count, up to limit
      self.playerhp += HP/2
      if self.playerhp > HP:
        self.playerhp = HP
        
    if (itemType.lower() == "ether" and self.playerether > 0):
      #remove one ether from the information about the player
      self.playerether -= 1
      #the ether adds most of total mp, up to limit.
      self.playermp += MANA-20
      if self.playermp > MANA:
        self.playermp = MANA

  def checkStatus(self,enemy,player,isFighting,playerToEnemy,display):
    #if player wins
    if (enemy.hp <=0):
      dropped = self.dropItem(display)
      player.takeItem(dropped)
      self.playerTake(dropped)
      if self.printingOn:
        display.tellUser("Player defeated the enemy!")
      self.enemyNum -= 1
      self.turn += 1
      self.lastDamage = playerToEnemy #can omit this line?
      player.enemyDefeated()
      #return False
    elif (self.enemyNum == 0):
      self.score = self.calcScore(self.enemyNum,self.playerhp,player.manaPoints)
      if self.printingOn or self.justOneGame:
        display.tellUser (player.name+" defeats every enemy with a score of "+str(self.score)+" points!")
      self.time = sum(player.time)/len(player.time)
      if self.printingOn or self.justOneGame:
        display.tellUser("Average time per turn to make a decision was: "+ str(self.time)+ " seconds.")
      self.isOver = True
      #return False

    #(if player loses)
    elif (self.playerhp <= 0):
      self.score = self.calcScore(self.enemyNum, self.playerhp,player.manaPoints)
      self.isOver = True
      if self.printingOn or self.justOneGame:
        display.tellUser (player.name+" ends the gauntlet defeating "+ str(15 - self.enemyNum) +
             " enemies with a score of " + str(self.score)+" points!")
      self.time = sum(player.time)/len(player.time)
      if self.printingOn or self.justOneGame:
        display.tellUser("Average time per turn to make a decision was: "+ str(self.time)+ " seconds.")
      return False
    else:
      return True

  def displayPoints(self,player,enemy,display):
    if self.printingOn:
      display.tellUser("Player: HP("+str(self.playerhp)+") MP("+str(player.manaPoints)+")")
      display.tellUser("Enemy: HP("+str(enemy.hp)+")")

  # this is the code for the battle. 
  def gameStart(self, player,display):
    if self.justOneGame:
      display.tellUser("********************************")
      display.tellUser(player.name+" is now playing!")
    #players can win if they beat 15 enemies
    self.enemyNum = 15 
    #reset world's information about player's hp,mp,nectar and ether
    self.playerhp=HP
    self.playermp = MANA
    self.playerether = ETHER
    self.playernectar=NECTAR

    while (self.isOver is False): 
      isFighting = True 
      enemy = self.getEnemy()
      if self.printingOn:
        display.tellUser("Enemy spawned! Are you ready?")
      self.displayPoints(player,enemy,display)
      while(isFighting == True):
        if(isFighting is True):
          if self.printingOn:
            display.tellUser("\nTurn: "+str(self.turn)+", "+str(self.enemyNum)+" enemies left")
            display.tellUser("Nectar: "+str(player.nectar)+" Ether: "+str(player.ether))
          lastDamage = enemy.lastDamage
          player.receiveDamageReport(enemy.lastDamage)
          #playerToEnemy = player.fight(enemy,lastDamage)
          playerToEnemy = player.fight(enemy)
          if (playerToEnemy == "nectar" or playerToEnemy == "ether"):
            if self.printingOn:
              display.tellUser("Player used "+playerToEnemy)
            self.playerConsume(playerToEnemy)
            enemy.lastDamage = 0
          elif playerToEnemy == "normal":
            enemy.hit(DAMAGE, "normal")
          elif player.getMana() >= SPECIALCOST:
            enemy.hit(SPECIALDAMAGE, playerToEnemy)
            player.setMana(player.getMana()-SPECIALCOST)
          elif self.printingOn:
            display.tellUser("Player does not have enough mana to sustain a special attack!")
          isFighting = self.checkStatus(enemy,player,isFighting,playerToEnemy,display)

        if(isFighting is True):
          enemyToPlayer = enemy.fight()
          player.takeDamage(enemyToPlayer)
          self.playerDamage(enemyToPlayer) #track player's hp in world
          player.setLastAction(enemy.lastAction)
          isFighting = self.checkStatus(enemy,player,isFighting,playerToEnemy,display)
          self.displayPoints(player,enemy,display)
          self.turn += 1
