'''
AI Elemental Gauntlet Project
Display Class
Handles the user interface

@authors: Hana, Madi, Cameron
Date Created: 04/15/2020
Date Last Modified: 04/03/2022 by Browning

Change log
April 12, 2021 Carol Browning
Change names of files and player AIs

March 10, 2022 Carol Browning
Separated code into model (World) view (Display) and controller (main)

'''
class Display():
    #def __init__(self):
    def askUser(self,question):
        return input(question)
    def tellUser(self,info):
        print(info)
        
