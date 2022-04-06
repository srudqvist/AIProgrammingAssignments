'''
Interactive Player
by Carol Browning
May 13, 2021

Updated April 3, 2022 to work with code changes.
'''

from generalPlayer import Player
import time
import random

class InteractiveAI(Player):

  #attackTypes possibly used by player.
  attackTypes = ["lightning", "fire", "ice", "earth", "wind"]

  def __init__(self):
    Player.__init__(self, "InteractivePlayer", Player.HP, Player.MANA)
    self.enemyInfo = EnemyInfo()

  # This function asks users for how much damage the AI gave in the last
  # turn and updates its knowledge of enemy's HP, weakness, and resistance.
  def receiveDamageReport(self, lastDamage):
    pass 

  def enemyDefeated(self):
    self.enemyInfo = EnemyInfo()
    self.defeatedLastTurn = True

  # Player does a turn of the fight, 
  # output: damage value and action type
  def fight(self, enemy):
    start = time.time()
    
    print("Enter the number of your choice: \n 1 consume nectar \n 2 consume ether")
    print(" 3 normal attack \n 4 special attack")
    selection = input("Your choice: ")
    print("You entered "+selection+".")
    if selection == "1":
      self.consumeItem("nectar")
      action = "nectar"
    elif selection == "2":
      self.consumeItem("ether")
      action = "ether"
    elif selection == "3":
      action = "normal"
    elif selection == "4":
      print("The attack types are lightning, fire, ice, earth, and wind.")
      thisAttack = input("Which attack type? ")
      action = thisAttack
    else:
      print("I didn't understand your selection, so I'll do a normal attack")
      action = "normal"

    end = time.time()
    self.time.append(end - start)
    return action

# Knowledge the player knows about the enemy
class EnemyInfo():
  def __init__(self):
    self.lastAction = ""
