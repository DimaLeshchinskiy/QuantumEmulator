import math 
from int2bin import intToBinArray

def getANF(input=[]):
    result = []
    inputCount = math.log2(len(input))

    triangle = getPascalTriangle(input)
    for i, row in enumerate(triangle):
        if row[0] == 1:
            bitArray = intToBinArray(i, inputCount)
            indexes = [i for i, x in enumerate(bitArray) if x == 1]
            result.append(indexes)
    
    return result

def getPascalTriangle(input=[]):
    triangle = [input]
    for i in range(len(input) - 1):
        row = []
        for j in range(1, len(triangle[i])):
            row.append((triangle[i][j - 1] + (triangle[i][j])) % 2)
        triangle.append(row)
    return triangle

if __name__ == "__main__":
    # inserted array represents output of function f: [0,0,0]=>0; [0,0,1]=>0 ... [1,1,1]=>1
    anf = getANF([0,0,0,1,0,1,1,1])
    # print: [[1, 2], [0, 2], [0, 1]] => (X1 & X2) XOR (X0 & X2) XOR (X0 & X1)
    print(anf) 