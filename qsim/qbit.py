import numpy as np
from qconstants import ZERO, ONE

class QBit():
    def __init__(self, initValue=0):
        if initValue == 0:
            self.state = ZERO
        elif initValue == 1:
            self.state = ONE

    def setState(self, newState):
        if newState[0] ** 2 + newState[1] ** 2 == 1:
            self.state = newState.transpose()

    def _getProbabiltyOfZero(self):
        return np.matmul(ZERO.conj(), self.state) ** 2
    
    def getMeasure(self):
        probabilityOfZero = self._getProbabiltyOfZero()
        return np.random.choice(a=[0, 1], size=1, p=[probabilityOfZero, 1 - probabilityOfZero])
