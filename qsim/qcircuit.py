from turtle import st
from qsim.qconstants import I, ONE, ZERO, X
from qsim.qcolumn import QColumn
import numpy as np
from qsim.util.int2bin import binToInt, intToBinArray


class QCircuit():
    def __init__(self, qubit_size=0):
        self.state = 1
        self.qbits_size = qubit_size
        self.circuit = []

        self.all_combinations_cache = []

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
        if isinstance(controlIndexes, list): 
            column.setControl(controlIndexes, targetIndex, gate)
        else:
            column.setControl([controlIndexes], targetIndex, gate)
        self.circuit.append(column)

    def addCNOT(self, controlIndex, targetIndex):
        self.addControlGate(controlIndex, targetIndex, X)

    def addToffoli(self, controlIndexes, targetIndex):
        self.addControlGate(controlIndexes, targetIndex, X)
    
    def addSwap(self, index1, index2):
        self.addCNOT(index1, index2)
        self.addCNOT(index2, index1)
        self.addCNOT(index1, index2)
    
    def addCustomMatrix(self, matrix):
        column = QColumn(self.qbits_size)
        column.matrix = matrix
        self.circuit.append(column)

    def simulate(self):
        self.state = self.circuit[0].matrix
        for i, column in enumerate(self.circuit):
            if i == 0:
                continue
            self.state = np.matmul(self.state, column.matrix)

    def _getProbabilty(self, vector):
        return np.abs(np.matmul(np.array(vector, dtype=complex).conj(), self.state.transpose())) ** 2

    def _getCombinationsOfStates(self):
        if len(self.all_combinations_cache) > 0:
            return self.all_combinations_cache

        states = []

        for i in range(2**self.qbits_size):
            binArr = intToBinArray(i, self.qbits_size)
            states.append(binArr)

        return states

    def measure(self):
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
    
    def _measureAllPossible(self):
        vectorsOfPosibleStates = self._getCombinationsOfStates()
        possible = []

        for combination in vectorsOfPosibleStates:
            state = 1
            for bit in combination:
                qubit = ZERO
                if bit == 1:
                    qubit = ONE
                state = np.kron(state, qubit)
            
            probability = self._getProbabilty(state).real.flat[0]
            if probability > 0:
                possible.append((combination, probability))

        return possible

    def measureAll(self, indexes=[]):
        all_possible = self._measureAllPossible()
        if len(indexes) == 0:
            return all_possible

        groups = dict()
        
        for possible in all_possible:
            state, probability = possible

            part_of_state = []
            for index in indexes:
                part_of_state.append(state[index])
            
            part_decimal = binToInt(part_of_state)

            if part_decimal in groups:
                prob = groups[part_decimal][1]
                groups[part_decimal] = (part_of_state, probability + prob)
            else:
                groups[part_decimal] = (part_of_state, probability)

        return list(groups.values())