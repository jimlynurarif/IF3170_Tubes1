from objectiveFunctionSteepest import objectiveFunctionSteepest

def findSteepestNeighbor(array:list, objectiveValue:int) -> list:
    currentList = list(array)
    currentObjective = objectiveValue

    print("currentList:", currentList)
    print("currentObjectiive:", currentObjective)

    for i in range(125):
        for j in range(i+1, 125):
            tempArray = list(array)
            tempArray[i], tempArray[j] = tempArray[j], tempArray[i]
            tempObjective = objectiveFunctionSteepest(tempArray)

            # print("tempArray:", tempArray)
            # print("tempObj:", tempObjective)

            if tempObjective > currentObjective:
                currentList = tempArray
                currentObjective =tempObjective
    print("currentlist before return:", currentList)
    return currentList

def steepestAscent(array:list, objectiveValue:int) -> list:
    neighbor = findSteepestNeighbor(array, objectiveValue)
    # print("neighbor", neighbor)
    if neighbor == array:
        return neighbor
    else:
        return(steepestAscent(neighbor,objectiveFunctionSteepest(neighbor)))

a = [1 for i in range(125)]
b = [0 for i in range(125)]

d = [1, 7, 123, 54, 5, 31, 36, 78, 24, 35, 11, 17, 13, 9, 15, 40, 12, 18, 14, 20, 21, 27, 83, 44, 50, 26, 77, 28, 29, 16, 41, 32, 33, 34, 25, 46, 37, 38, 39, 30, 2, 42, 43, 19, 10, 96, 47, 48, 99, 45, 51, 107, 53, 49, 55, 81, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 22, 73, 74, 75, 76, 72, 8, 79, 80, 56, 82, 23, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 6, 97, 108, 4, 100, 101, 102, 103, 104, 105, 106, 52, 98, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 3, 124, 125]

for i in range(125):
    b[i] = i+1

c = b
c[5], c[6] = c[6], c[5]
# print("c:", c)

# print("steepest neighbor:", findSteepestNeighbor(b, objectiveFunction(b)))
# print("end steepest ascent:", steepestAscent(b, objectiveFunction(b)))

# print("1")
# print(findSteepestNeighbor(d, objectiveFunction(d)))