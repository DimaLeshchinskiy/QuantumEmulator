from qsim.qconstants import I, ONE, ZERO, X
from qsim.qcolumn import QColumn
import numpy as np
from qsim.util.int2bin import intToBinArray


class QCircuit():
    def __init__(self):
        self.state = 1
        self.qbits_size = 0
        self.circuit = []

    def addQubits(self, *initValues):
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
    
    def addControlGate(self, controlIndexes, targetIndex, gate):
        column = QColumn(self.qbits_size)
        column.setControl(controlIndexes, targetIndex, gate)
        self.circuit.append(column)

    def addCNOT(self, controlIndex, targetIndex):
        self.addControlGate([controlIndex], targetIndex, X)

    def addToffoli(self, controlIndexes, targetIndex):
        self.addControlGate(controlIndexes, targetIndex, X)

    def simulate(self):
        self.state = self.circuit[0].matrix
        for i, column in enumerate(self.circuit):
            if i == 0:
                continue
            self.state = np.matmul(self.state, column.matrix)

    def _getProbabilty(self, vector):
        return np.matmul(np.array(vector, dtype=complex).conj(), self.state.transpose()) ** 2

    def _getCombinationsOfStates(self):
        states = []

        for i in range(2**self.qbits_size):
            binArr = intToBinArray(i, self.qbits_size)
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
