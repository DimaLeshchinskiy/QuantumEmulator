from qsim.qconstants import *
import numpy as np


class QCircuit():
    def __init__(self):
        self.state = 1
        self.gates = 1
        self.qbits_size = 0
    
    def addQubit(self, initValue=0):
        qbit = ZERO
        if initValue == 1:
            qbit = ONE

        self.state = np.kron(self.state, qbit)
        self.qbits_size += 1

    def addQubits(self, count, initValue=0):
        for i in range(count):
            self.addQubit(initValue)
        
    def addH(self, index):
        for i in range(self.qbits_size):
            if index == i:
                self.gates = np.kron(self.gates, H)
            else:
                self.gates = np.kron(self.gates, I)

    def _getProbabiltyOfOne(self, index):
        state = np.matmul(self.gates, self.state)
        vector = []
        index += 1
        for i in range(0, 2 ** self.qbits_size):
            if (i & index) > 0:
                vector.append(1)
            else:
                vector.append(0)

        print(state)
        print(np.array([vector], dtype=complex).conj())
        
        return np.matmul(np.array([vector], dtype=complex).conj(), state.transpose()) ** 2

    def measure(self, index):
        probabilityOfOne = np.real(self._getProbabiltyOfOne(index).item(0))
        print(probabilityOfOne)
        return np.random.choice(a=[0, 1], size=1, p=[1 - probabilityOfOne, probabilityOfOne])
    
    def measureAll(self):
        all = []
        for i in range(self.qbits_size):
            all.append(self.measure(i)[0])

        return all            
