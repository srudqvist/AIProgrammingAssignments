'''
Player AI Donald Duck
by Carol Browning
April 12, 2021

Donald Duck just attacks a normal attack every turn.
This is an example player AI subclass of Player.  You should use this
as starting code for your AI player.

April 25, 2021  Greedy version - consume if possible.
Attack randomly.

April 3, 2022 Adjusted to work with updated code.

'''

from generalPlayer import Player
import time
import random

class DonaldDuckAI(Player):

  #attackTypes possibly used by player.
  attackTypes = ["lightning", "fire", "ice", "earth", "wind"]

  def __init__(self):
    Player.__init__(self, "Donald Duck", Player.HP, Player.MANA)
    self.enemyInfo = EnemyInfo()
    # OTHER ATTRIBUTES YOU WANT CAN GO HERE

  # This function asks users for how much damage the AI gave in the last
  # turn and updates its knowledge of enemy's HP, weakness, and resistance.
  def receiveDamageReport(self, lastDamage):
    # YOUR CODE GOES HERE
    pass 

  def enemyDefeated(self):
    # YOUR CODE GOES HERE
    self.enemyInfo = EnemyInfo()
    self.defeatedLastTurn = True

  # Player does a turn of the fight, 
  # output: damage value and action type
  # KEEP THE FIRST TWO AND LAST THREE LINES OF CODE
  def fight(self, enemy):
    start = time.time()
    
    
    #YOUR CODE GOES HERE
    # code that updates my information about last damage
    # code that sets the action to return.  Examples:
    if self.hitPoints < 500 and self.nectar >0:
      self.consumeItem("nectar")
      action = "nectar"
    elif self.manaPoints >0:
      action = self.attackTypes[random.randint(0,4)]
    elif self.manaPoints<40 and self.ether > 0:
      self.consumeItem("ether")
      action = "ether"
    else:
      action ="normal"
    end = time.time()
    self.time.append(end - start)
    return action

# Knowledge the player knows about the enemy
class EnemyInfo():
  def __init__(self):
    #OTHER ATTRIBUTES OF INTEREST CAN GO HERE
    self.lastAction = ""
