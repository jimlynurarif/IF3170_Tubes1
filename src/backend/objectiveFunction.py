# the three integer list below are just for initial testing. remove it later

arr = list(range(1, 126))
dummy = [1 for i in range(125)]
correct = [
    121, 108, 7, 20, 59,
    29, 28, 122, 125, 11,
    51, 15, 41, 124, 84,
    78, 54, 99, 24, 60,
    36, 110, 46, 22, 101,

    31, 53, 112, 109, 10,
    12, 82, 34, 87, 100,
    103, 3, 105, 8, 96,
    113, 57, 9, 62, 74,
    56, 120, 55, 49, 35,

    47, 61, 45, 76, 86,
    107, 43, 38, 33, 94,
    89, 68, 63, 58, 37,
    32, 93, 88, 83, 19,
    40, 50, 81, 65, 79,

    91, 77, 71, 6, 70,
    52, 64, 117, 69, 13,
    30, 118, 21, 123, 23,
    26, 39, 92, 44, 114,
    116, 17, 14, 73, 95,

    25, 16, 80, 104, 90,
    115, 98, 4, 1, 97,
    42, 111, 85, 2, 75,
    66, 72, 27, 102, 48,
    67, 18, 119, 106, 5
]


# the list must be a list of integer with length of exactly 125 elements
def rowValues(array:list) -> int:
    value = 0
    for i in range(0,25):
        j = i*5
        temp = array[j] + array[j+1] + array[j+2] + array[j+3] + array[j+4]
        # print("temp: ", temp)
        if temp != 315:
            value -= 1
    
    return value

def pillarValues(array:list) -> int:
    value = 0
    for i in range(0,25):
        temp = array[i] + array[i + 25] + array[i + 50] + array[i + 75] + array[i + 100]
        # print("temp:", temp)
        if temp != 315:
            value -= 1

    return value

def columnValues(array:list) -> int:
    value = 0
    for i in range(0, 101, 25):
        for j in range(i, i+5):
            temp = array[j] + array[j + 5] + array[j + 10] + array[j + 15] + array[j + 20]
            # print("temp:", temp)
            if temp != 315:
                value -= 1
            
        
    return value

def frontToBackSideDiagonalValues(array:list) -> int:
    value = 0
    for i in range(0, 101, 25):
        for j in range(i, i+5, 4):
            temp = 0
            if j % 5 == 0:
                temp = array[j] + array[j + 6] + array[j + 12] + array[j + 18] + array[j + 24]

            else:
                temp = array[j] + array[j + 4] + array[j + 8] + array[j + 12] + array[j + 16]
            # print("temp:", temp)
            if temp != 315:
                value -= 1

    return value

def leftToRightSideDiagonalValues(array:list) -> int:
    value = 0

    for i in range(0,5):
        for j in range(i, i+101, 100):
            # print(i,j)
            temp = 0
            if j == i:
                temp = array[j] + array[j + 30] + array[j + 60] + array[j + 90] + array[j + 120]
            else:
                temp = array[j] + array[j - 20] + array[j - 40] + array[j - 60] + array[j - 80]
            # print("temp:", temp)
            if temp != 315:
                value -= 1
 
    return value

def upToDownSideDiagonalValues(array:list) -> int:
    value = 0

    for i in range(0, 21, 5):
        for j in range(i, i+5, 4):
            # print(i,j)
            temp = 0
            if j % 5 == 0:
                temp = array[j] + array[j + 26] + array[j + 52] + array[j + 78] + array[j + 104]
            else:
                temp = array[j] + array[j + 24] + array[j + 48] + array[j + 72] + array[j + 96]
            # print("temp:", temp)
            if temp != 315:
                value -= 1  

    return value

def triagonalValues(array:list) -> int:
    value = 0
    first = array[0] + array[31] + array[62] + array[93] + array[124]
    second = array[4] + array[33] + array[62] + array[91] + array[120]
    third = array[20] + array[41] + array[62] + array[83] + array[104]
    fourth = array[24] + array[43] + array[62] + array[81] + array[100]

    # print(first)
    # print(second)
    # print(third)
    # print(fourth)

    if first != 315:
        value -=1

    if second != 315:
        value -=1

    if third != 315:
        value -=1

    if fourth != 315:
        value -=1

    return value

def objectiveFunction(array:list) -> int:
    value = 0
    value += rowValues(array)
    value += pillarValues(array)
    value += columnValues(array)
    value += frontToBackSideDiagonalValues(array)
    value += leftToRightSideDiagonalValues(array)
    value += upToDownSideDiagonalValues(array)
    value += triagonalValues(array)
    return value

# print("rows:", rowValues(correct))
# print("pillars:", pillarValues(correct))
# print("columns:", columnValues(correct))
# print("frontBack:", frontToBackSideDiagonalValues(correct))
# print("leftRight:", leftToRightSideDiagonalValues(correct))
# print("updown:", upToDownSideDiagonalValues(correct))
# print("triagonal:", triagonalValues(correct))



# print(objectiveFunction(dummy))
