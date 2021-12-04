import numpy as np
from qsim.qconstants import ZERO, ONE, I
from qsim.util.int2bin import intToBinArray

class QColumn():
    def __init__(self, size=0):
        self.matrix = None
        self.size = size
    
    def set(self, values=[]):
        self.matrix = 1
        for value in values:
            self.matrix = np.kron(self.matrix, value)
    
    def setControl(self, controlIndexes, targetIndex, gate):
        self.matrix = 0

        allStates = [1 for i in range(2**len(controlIndexes))]
        binaryNums = [intToBinArray(i, len(controlIndexes)) for i in range(2**len(controlIndexes))]
        controlCounter = 0

        for i in range(0, self.size):
            if i in controlIndexes:
                for j, matrix in enumerate(allStates):
                    state = 1
                    if binaryNums[j][controlCounter] == 0:
                        state = np.matmul(np.array([ZERO]).transpose(), np.array([ZERO]).conj())
                    else:
                        state = np.matmul(np.array([ONE]).transpose(), np.array([ONE]).conj())
                    allStates[j] = np.kron(matrix, state)
                controlCounter += 1
            elif i == targetIndex:
                for j, matrix in enumerate(allStates[:-1]):
                    allStates[j] = np.kron(matrix, I)

                allStates[-1] = np.kron(allStates[-1], gate)
            else:
                for j, matrix in enumerate(allStates):
                    allStates[j] = np.kron(matrix, I)

        for matrix in allStates:
            self.matrix += matrix
