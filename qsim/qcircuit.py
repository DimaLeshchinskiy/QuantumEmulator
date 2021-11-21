from qsim.qconstants import ONE, ZERO, X
from qsim.qcolumn import QColumn
import numpy as np


class QCircuit():
    def __init__(self):
        self.state = 1
        self.qbits_size = 0
        self.circuit = []

    def addQubits(self, initValues=[]):
        column = QColumn()
        values = []
        for value in initValues:
            if value == 1:
                values.append(ONE)
            else:
                values.append(ZERO)
        column.set(values)
        self.circuit.append(column)
        self.qbits_size = len(initValues)

    def addGates(self, gates=[]):
        column = QColumn()
        column.set(gates)
        self.circuit.append(column)
    
    def addControlGate(self, controlIndex, targetIndex, gate):
        column = QColumn(self.qbits_size)
        column.setControl(controlIndex, targetIndex, gate)
        self.circuit.append(column)

    def addCNOT(self, controlIndex, targetIndex):
        self.addControlGate(controlIndex, targetIndex, X)

    def simulate(self):
        self.state = self.circuit[0].matrix

        for i, column in enumerate(self.circuit):
            if i == 0:
                continue

            self.state = np.matmul(self.state, column.matrix)

    def _getProbabiltyOfOne(self, index):
        vector = []
        for i in range(0, 2 ** self.qbits_size):
            if (i & 2 ** (self.qbits_size - index - 1)) > 0:
                vector.append(1)
            else:
                vector.append(0)

        return np.matmul(np.array(vector, dtype=complex).conj(), self.state.transpose()) ** 2

    def measure(self, index):
        probabilityOfOne = np.real(self._getProbabiltyOfOne(index).item(0))
        return np.random.choice(a=[0, 1], size=1, p=[1 - probabilityOfOne, probabilityOfOne])[0]
    
    def measureAll(self):
        all = []
        for i in range(self.qbits_size):
            all.append(self.measure(i))

        return all            
