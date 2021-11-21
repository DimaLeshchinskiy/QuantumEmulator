import numpy as np
from qsim.qconstants import ZERO, ONE, I

class QColumn():
    def __init__(self, size=0):
        self.matrix = 1
        self.size = size
    
    def set(self, values=[]):
        for value in values:
            self.matrix = np.kron(self.matrix, value)
    
    def setControl(self, controlIndex, targetIndex, gate):
        zeroState = 1
        oneState = 1

        for i in range(0, self.size):
            if i == controlIndex:
                zeroState = np.kron(zeroState, np.matrix([[1, 0], [0, 0]], dtype=complex))
                oneState = np.kron(oneState, np.matrix([[0, 0], [0, 1]], dtype=complex))
            elif i == targetIndex:
                zeroState = np.kron(zeroState, I)
                oneState = np.kron(oneState, gate)
            else:
                zeroState = np.kron(zeroState, I)
                oneState = np.kron(oneState, I)
        
        self.matrix = zeroState + oneState