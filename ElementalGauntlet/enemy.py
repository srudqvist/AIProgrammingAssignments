"""
Enemy Script
@authors: Hana, Madi, Cameron
This script contains the enemy class for the Elemental Gauntlet project.
Enemy will choose random action each turn.

Change log
April 11 and 12, 2021 Carol Browning
removed partial code for special attacks by the enemy
"""

import random

WEAKNESS = 1.5 # Multiplier for attacks the enemy is weak to
RESISTANCE = 0.8 # Multiplier for attacks the enemy is resistant to
DAMAGEMIN = 90 # Minimum damage of an enemy attack
DAMAGEMAX = 110 # Maximum damage of an enemy attack


class Enemy:
    # types of attacks possibly used to hit Enemy
    attackTypes = ["lightning", "fire", "ice", "earth", "wind"]
    # all possible actions the enemy can choose to use, repeats for percentage chance
    # 60% chance to attack, 30% chance to use special attack, and 10% chance to heal
    actions = ["attack"]*9+["heal"]

    def __init__(self,printingOn):
        self.hp = 1000
        self.modifiers = self.create_weaknesses()
        self.lastDamage = 0
        self.lastAction = ""
        self.printingOn=printingOn

    # Randomly sets a weakness and resistance from the dictionary
    def create_weaknesses(self):
        attackTypesCopy = self.attackTypes.copy()
        modifiers = {"lightning": 1.0, "fire": 1.0, "ice": 1.0, "earth": 1.0, "wind": 1.0, "normal": 1.0}
        for i in range(0, 2):
            modifierIndex = random.randrange(0, len(attackTypesCopy))
            modifier = attackTypesCopy[modifierIndex]
            attackTypesCopy.remove(modifier)
            if i < 1:
                modifiers[modifier] = WEAKNESS
            else:
                modifiers[modifier] = RESISTANCE
        return modifiers
    
    '''Process sensor data
    '''
    # Takes a damage amount and attack type and the calculates and reduces the hp value
    def hit(self, damage, attackType):
        damage = damage * self.modifiers[attackType]
        self.hp -= damage
        if self.printingOn:
            print("Player attacks the enemy with "+str(attackType)+" for "+str(damage)+" damage!")
        self.damage = damage
        self.lastDamage = damage
        if(self.hp<0):
          self.hp = 0

    ''' Select action to send to world
    '''
    # randomly picks an action
    def choose_action(self):
        randIndex = random.randrange(0, len(self.actions))
        return self.actions[randIndex]

    # with a given action, outputs what the action does and returns the value.
    def fight(self):
        action = self.choose_action()
        self.lastAction = action
        if action == "attack":
          damage = random.randrange(DAMAGEMIN, DAMAGEMAX+1)
          if self.printingOn:
              print("The enemy attacks the player for " + str(damage) + " damage.")
          return damage
        elif action == "heal":
          if self.printingOn:
              print("The enemy restores 100 hp")
          self.hp += 100
          self.lastDamage -= 100
          return 0

      
