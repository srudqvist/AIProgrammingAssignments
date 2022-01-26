import time
def addNCheck(myset, aSubset, sumSoFar, goal, answerList):
  currentValue = myset.pop()
  newSubset = aSubset + [currentValue]
  newSum = sumSoFar + currentValue
  print(f"newSum: {newSum}")
  if newSum == goal:
      print(f"newSubset: {newSubset} is the solution!")
      answerList.append(1)
      #return newSubset
  if len(myset) != 0 and len(answerList) < 1: #If the list has found a single solution, will not play the rest!
    #print("above if statement")
    myset2 = myset.copy()
    if newSum < goal: 
      addNCheck(myset, newSubset, newSum, goal, answerList)
      addNCheck(myset2, aSubset, sumSoFar, goal, answerList)

s = time.time()
addNCheck([1,2,3,4,5,6,7,8,9,10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],[], 0, 784, [])
e = time.time()
print(e-s)
