from qsim.qcircuit import QCircuit
from qsim.qconstants import H, I, X
circuit = QCircuit()

circuit.addQubits(0, 0, 0, 1)
circuit.addGates([H, H, H, H])

# BEGIN Uf - function constant
# circuit.addGate(X, 3)
# END Uf

# BEGIN Uf - function balanced
circuit.addToffoli([0, 1], 3)
circuit.addCNOT(2, 3)
# END Uf

circuit.addGates([H, H, H, I])

circuit.simulate()
state = circuit.measureAll()

print(state)