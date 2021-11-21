from qsim.qcircuit import QCircuit
from qsim.qconstants import H, I
circuit = QCircuit()

circuit.addQubits([0, 0])
circuit.addGates([H, I])
circuit.addCNOT(controlIndex=0, targetIndex=1) 

circuit.simulate()
state = circuit.measureAll()
print(state)



