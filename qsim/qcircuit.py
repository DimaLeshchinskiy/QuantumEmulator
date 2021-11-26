from qsim.qconstants import I, ONE, ZERO, X
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

    def addGate(self, gate, index):
        gates = [I] * self.qbits_size
        gates[index] = gate
        self.addGates(gates)
    
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

    def _IntToBinArray(self, number, size=0):
        bitArray = []
        size -= 1

        while size >= 0:
            if 2 ** size > number:
                bitArray.append(0)
            else:
                bitArray.append(1)
                number -= 2 ** size

            size -= 1

        return bitArray

    def _getProbabilty(self, vector):
        return np.matmul(np.array(vector, dtype=complex).conj(), self.state.transpose()) ** 2

    def _getCombinationsOfStates(self):
        states = []

        for i in range(2**self.qbits_size):
            binArr = self._IntToBinArray(i, self.qbits_size)
            states.append(binArr)

        return states

    def measureAll(self):
        vectorsOfPosibleStates = self._getCombinationsOfStates()
        probabilities = []

        for combination in vectorsOfPosibleStates:
            state = 1
            for bit in combination:
                qubit = ZERO
                if bit == 1:
                    qubit = ONE
                state = np.kron(state, qubit)
            probabilities.append(self._getProbabilty(state).real.flat[0])

        resultIndex = np.random.choice(a=len(vectorsOfPosibleStates), size=1, p=probabilities)[0]
        return vectorsOfPosibleStates[resultIndex]
