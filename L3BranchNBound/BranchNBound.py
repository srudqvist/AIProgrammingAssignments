import time
#Branch and Bound Search Algorithm
#
# Algorithm in Notes:
#call addNCheck([3,5,6,7], [ ], 0, 15)
#def addNCheck(myset, aSubset, sumSoFar, goal):
#	currentValue = pop an element from the set
#	newSubset = aSubset + [currentValue]
#	newSum = sumSoFar + currentValue
#	if newSum == goal: newSubset is the solution!!
#	if myset isn’t empty:
#		if newSum < goal: addNCheck(myset, newSubset, newSum, goal)
#		addNCheck(myset, aSubset, sumSoFar,goal)
#
# Our set:
# 1 - 20

# I added a list that keeps track of how many answers we found. I tried using a bool and it didn't work.Issac helped me realize that a bool wouldn't work and suggested doing the same thing, but with a list. 
def addNCheck(myset, aSubset, sumSoFar, goal, answerList):
  #print(f"myset: {myset}")
  currentValue = myset.pop()
  newSubset = aSubset + [currentValue]
  newSum = sumSoFar + currentValue
  if newSum == goal:
      #print(f"newSubset: {newSubset} is the solution!")
      answerList.append(1)
      #return newSubset
  if len(myset) != 0 and len(answerList) < 1: #If the list has found a single solution, will not play the rest!
    #print("above if statement")
    myset2 = myset.copy()
    if newSum < goal: 
      addNCheck(myset, newSubset, newSum, goal, answerList)
      addNCheck(myset2, aSubset, sumSoFar, goal, answerList)


#addNCheck([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],[], 0, 60, [])


def testCaseA(testNumber, seet, goal):
  #try:
    startTime = time.time()
    addNCheck(seet, [], 0, goal, [])
    endTime = time.time()
    totTime = endTime - startTime
    print(f"The time for test A{testNumber} was {totTime}.")
    return totTime
  #except:
    print(f"No solution for test A{testNumber}.")


def testCaseB(testNumber, seet, goal):
  #try:
    startTime = time.time()
    addNCheck(seet, [], 0, goal, [])
    endTime = time.time()
    totTime = endTime - startTime
    print(f"The time for test B{testNumber} was {totTime}.")
    return totTime

  #except:
    #endTime = time.time()
    #print(f"No solution for test B{testNumber}.")
    #totTime = endTime - startTime
    #return totTime

def testA():
  timesA = []
  for n in range(10,29):
    testNumber = n - 9
    
    seet = list(range(1, n + 1))

    goalA = int(n * (n + 1)/2)
    print(f"GoalA: {goalA} ")
    timeA = testCaseA(testNumber, seet, goalA)
    print(timeA)
    timesA.append(timeA)
  return timesA


def test(timesA):
  timesA = timesA
  timesB = []
  for n in range(10,29):
    testNumber = n - 9
    
    seet = list(range(1, n + 1))

    goalB = int(n * n)
    print(f"GoalB: {goalB} ")
    timeB = testCaseB(testNumber, seet, goalB)
    print(timeB)
    timesB.append(timeB)

  print()
  print("{:^8}{:^25}{:^9}{:^10}".format("#","A","|","B"))
  print("-" * 70)
  for i in range(0, len(timesA)):
    print("{:^8}{:<25}{:^9}{:^10}".format(i + 1, str(timesA[i]), "|", str(timesB[i])))

  for i in range(0, len(timesA)):
    difference = timesA[i] - timesB[i]
    print(difference)

timesA = testA()
test(timesA)



