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


def addNCheck(myset, aSubset, sumSoFar, goal):
    currentValue = myset.pop()
    newSubset = aSubset+ [currentValue]
    newSum = sumSoFar + currentValue
    if newSum == goal:
        print(f"newSubset: {newSubset} is the solution!")
        return newSubset
    if len(myset) != 0:
#        print(aSubset)
        if newSum < goal: addNCheck(myset.copy(), newSubset, newSum, goal)
        addNCheck(myset.copy(), aSubset, sumSoFar, goal)


addNCheck(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    [], 0, 60)