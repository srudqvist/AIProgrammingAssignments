'''
General Player class/script
@authors: Hana, Madi, Cameron
This is a general Player class, which is used to run the individual player AIs
in the game. Each has specific elements and attributes that are uniform
throughout, which are created here.

Change log
April 12, 2021 Carol Browning
Removed partial code for element type of player and for enemy special attacks
removed redundancies in setLastAction method
March 10, 2022
Made player class self-contained.  Player must track own set of information.
'''

class Player:
  #Constants for the player's attributes.
  DAMAGE = 100
  SPECIALDAMAGE = 200
  HP = 1000
  MANA = 100
  SPECIALCOST= 20
  NECTAR = 8
  ETHER = 5

  def __init__(self, name, hitPoints, manaPoints):
    self.name = name  #Used to differentiate between the player AIs in game
    self.hitPoints = self.HP  #Will be a set amount for all players
    self.manaPoints = self.MANA  #Also a set amount for all players
    self.nectar = self.NECTAR  #Each player starts with a certain amount, and can gain more throughout game
    self.ether = self.ETHER  #Similar to how nectar is handled.
    self.time = []

  def getMana(self):
    return self.manaPoints

  def setMana(self,value):
    if value <= self.MANA and value >= 0:
      self.manaPoints = value
  
  '''Process sensor data
  '''
  def takeDamage(self, damage):
    # This method is called from the world when an enemy acts.
    # It subtracts the amount of damage sustained by player from the total HP
    self.hitPoints = self.hitPoints - damage
    if(self.hitPoints<=0):
      self.hitPoints = 0

  def takeItem(self, item):
    # When an item is dropped, the world calls this method so the
    # player can take the item.  Add 1 to the number of nectar or ether.
    if(item.lower() == "nectar"):
      self.nectar = self.nectar + 1 #add one nectar to our total amount
    if(item.lower() == "ether"):
      self.ether = self.ether + 1 #add one ether to our total amount

  def consumeItem(self, itemType):
    # If we consume nectar, add back the required HP to player.
    # If we consume ether, add back the required MP to the player.
    # If player does not have the item, nothing is done.
    # Cannot exceed initial amounts of hp or mp.
    
    if (itemType.lower() == "nectar" and self.nectar > 0):
      #remove one nectar from our total amount
      self.nectar -= 1
      #the nectar adds back half of total hp, up to limit
      self.hitPoints += self.HP/2
      if self.hitPoints > self.HP:
        self.hitPoints = self.HP
    
    if (itemType.lower() == "ether" and self.ether > 0):
      #remove one ether from our total 
      self.ether -= 1
      #the ether adds most of total mp, up to limit.
      self.manaPoints += self.MANA-20
      if self.manaPoints > self.MANA:
        self.manaPoints = self.MANA

  def enemyDefeated(self):
    # This method is called from the world when an enemy is defeated.
    # Player will need to track information about the enemy and reset
    # it in this case.
    self.resetEnemyInfo()
    
  def resetEnemyInfo(self):
     # Use this method to reset your player's information about the enemy
    pass

  def receiveDamageReport(self,lastDamage):
    # Use this method to process information about how the enemy responded
    # to your last salvo.
    pass
  
  def setLastAction(self,lastAction):
    # This method is called from the world when an enemy takes an action.
    # Use this method to track the last action that the enemy took.
    self.enemyInfo.lastAction = lastAction

  ''' Select action to send to world; process data re last damage to enemy
      Note for future improvement: separate these two functions.
  '''
  def fight(self, enemy):
    # Overwrite this method in your playerAI subclass.
    # Change your information about the enemy given how much damage
    # was caused by your last attack.
    # Then decide what to do next, using your decision making process.
    # Return attackType for attack: "normal" for a normal attack
    # or "lightning", "fire", "ice", "earth" or "wind" for special attack
    # Return "nectar" or "ether" for healing.  
    pass

