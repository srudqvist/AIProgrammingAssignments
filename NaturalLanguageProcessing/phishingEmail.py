# phishingEmail.py
# Authors: Kayanna, Micah, Sam
# Date: April, 28, 2022



from random import*
numberOfEmails = 1


#List of different phrases used for the different paragraphs
greetingPhrase=[("Hello Professor!",0.1),("Greetings Student!",0.2), ("Hi Dr.Bronwing!", 0.6),("Good Evening Dr.Segman!", 0.2)]

determinantPhrase = [("This is", 1.0)]

hackerName= [("Drury IT.", 0.2), ("Drury Help Desk.", 0.45), ("IT Services.", 0.2), ("Federal Bureau of Investigations.", 0.1), 
             ("Phil.", 0.05)]

hackerEmail = [("hacker@drury.scam", 0.2), ("helpdesk@drory.com", 0.2), ("noreply@drurymail.com", 0.2), ("phishingemail@gmail.com", 0.4)]

timeAdv =[("Recently,", 0.5), ("Lately,", 0.5)]
adv = [("Never forget,", 0.5), ("Always remember,", 0.5)]
adj =[("many", 1.0)]

plnoun = [("accounts",0.2),("passwords", 0.2),("credentials", 0.2),("PINS",0.2),("private information", 0.2)]

noun = [("account",0.6),("password", 0.2),("credential", 0.2)]

pastvp =[("have been hacked.",0.5),("have been compromised.",0.5)]

commandPhrase = [("Please, follow these steps", 0.6), ("Follow these tips", 0.2), ("Use these tips", 0.2)]

orderPhrase = [("please click here:", 0.6), ("copy the link to your browser", 0.2), ("use this link:", 0.2)]

prepPhrase =[("to secure your account.", 0.5), ("to varify your account is safe.", 0.5)]

verbPhrase = [("change your password.", 0.1),("use the same password.", 0.2), ("tell someone else your password.", 0.2), 
              ("check for suspicious texts or words.", 0.2), ("follow random links from a suscpicous source.", 0.2),
              ("We know what you did two years ago.", 0.2)] 

introPrepPhrase = [("In order to", 0.5), ("To", 0.5)]
accountvp = [("reset your", 0.2), ("access your", 0.6), ("delete your", 0.2)]

graditudes = [("Thank you for your", 0.2), ("We appreciate your", 0.2), ("We are grateful for your", 0.2), 
              ("We are gracious for your", 0.2),("We couldn't have done it without your",0.1), 
              ("We can't thank you enough for your",0.1)]

phoneNumbers = [("+1 (666) 666-HACK", 0.2), ("+1-603-413-4124", 0.3), ("+1 (605)-475-6960", 0.4),("+1 (417) 882-3303",0.1)]
links = [("www.clickhere.com", 0.4), ("www.youraccount.com", 0.4), ("www.dontclickhere.com", 0.2)]


#Makes the greeting as well as the intro to the email.
#Provides different ways of writting the first paragraph and 
#selects the best phrases to make the most sense.
def paragraphOne():
  t = random()
  if t <.8:
    return selector(greetingPhrase)+ " "+ selector(determinantPhrase)+" "+selector(hackerName)+ "\n\n" + selector(timeAdv)+" "+selector(adj)+" "+selector(plnoun)+" "+selector(pastvp)+" "+selector(commandPhrase)+" "+selector(prepPhrase)+"\n\n"
  else:
    return selector(greetingPhrase)+" "+selector(plnoun)+" "+selector(pastvp)+" "+selector(commandPhrase) + "\n\n"

#Makes the "safety" tips paragraph
def paragraphTwo():
    sentences=4
    sentenceList = ""
    for i in range(sentences):
        sentenceList += selector(adv) + " " + selector(verbPhrase)+ "\n"

    return sentenceList
   

#makes the final paragraph given the user the fake link.
def paragraphThree():
    sentences = randint(4,6)
    paragraph = "\n"
    paragraph += selector(introPrepPhrase) + " " + selector(accountvp) + " " + selector(noun) + " "
    paragraph += selector(orderPhrase) + " " + selector(links) + "\n"
    for i in range(sentences):
        pass
        #paragraph += selector(somePhrase) + " " + selector(otherPhrase) + " " + selector(noun2)
    return paragraph

#Makes statments of gratitude and acknowlegments as well as the footer
def paragraphFour():
    t = random()
    sentences = randint(4,6)
    paragraph = ""
    for i in range(sentences):
        mySomeWords = selector(graditudes)
        myNoun = selector(plnoun)
        mySomeWords2 = selector(graditudes)
        myNoun2 = selector(plnoun)
        if mySomeWords not in paragraph and myNoun not in paragraph:
            paragraph += mySomeWords + " " + myNoun + ". "
            
        elif mySomeWords2 not in paragraph and myNoun2 not in paragraph:
            paragraph += mySomeWords2 + " " + myNoun2 + ". "
            
        else:
            paragraph += selector(graditudes) + " " + selector(plnoun) + ". "
            
    # Creates the footer of the email
    paragraph += "\n\n------------------------"
    paragraph += "\n" + selector(hackerName) + "\n"
    paragraph += selector(hackerEmail) + "\n"
    paragraph += selector(phoneNumbers)
      
    return paragraph
# Given a list of pairs, where the second element in each pair is a
# probability, return an element using the probabilities.
def selector(mylist):
    # Generate a random number t between 0 and 1
    t = random()
    # Go through the list until the sum of probabilities is at least t
    sumSoFar = 0
    index = 0
    while sumSoFar < t and index < len(mylist):
        sumSoFar += mylist[index][1]
        index = index + 1
    return mylist[index-1][0]

for i in range(numberOfEmails):
    # Plus sign so that it won't indent the other paragraphs
    print(paragraphOne() + paragraphTwo() + paragraphThree() + paragraphFour() + "\n")
    