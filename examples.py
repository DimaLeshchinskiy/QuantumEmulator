from qsim.qcircuit import QCircuit

#EXAMPLE 1
from qsim.qconstants import H
circuit = QCircuit()

circuit.addQubits(0) # create 1 qubits with init value 0
circuit.addGate(H, 0) # add 1 column of gates
circuit.addGate(H, 0) # add 2 column of gates

circuit.simulate() # make calculations
state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will be always 0


#EXAMPLE 2
from qsim.qconstants import X
circuit = QCircuit()

circuit.addQubits(0, 0) # create 2 qubits with init value 0
circuit.addGate(X, 1) # add 1 column of gates
circuit.addGates([X, X]) # add 2 column of gates

circuit.simulate() # make calculations
state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will be always [1, 0]


#EXAMPLE 3
circuit = QCircuit()

circuit.addQubits(1, 0, 0) # create 2 qubits with init value 0
circuit.addCNOT(controlIndex=0, targetIndex=2) # add CNOT gate with 0 index qubit as control and 2 index as target

circuit.simulate() # make calculations
state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will be always [1, 0, 1]


#EXAMPLE 4
from qsim.qconstants import H, I
circuit = QCircuit()

circuit.addQubits(0, 0) # create 2 qubits with init value 0
circuit.addGates([H, I])  # add 1 column of gates
circuit.addCNOT(controlIndex=0, targetIndex=1) # add CNOT gate with 0 index qubit as control and 1 index as target

circuit.simulate() # make calculations
state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will [0, 0] or [1, 1] with probability of 0.5


#EXAMPLE 5
circuit = QCircuit()

circuit.addQubits(1, 1, 1) # create 2 qubits with init value 0
circuit.addToffoli([0, 1], 2) # add Toffole gate with 0, 1 qubits as control and 2 qubit as target

circuit.simulate() # make calculations
state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will be always [1, 1, 0]