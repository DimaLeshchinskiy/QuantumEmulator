from qsim.qcircuit import QCircuit
from qsim.qconstants import H, I, X
circuit = QCircuit()

circuit.addQubits([0, 0, 0, 1])
circuit.addGates([H, H, H, H])


# BEGIN Uf - function constant
# circuit.addGate(X, 3)
# END Uf

# BEGIN Uf - function balanced
circuit.addCNOT(controlIndex=0, targetIndex=3)
circuit.addCNOT(controlIndex=1, targetIndex=3)
circuit.addCNOT(controlIndex=2, targetIndex=3)
# END Uf

circuit.addGates([H, H, H, I])

circuit.simulate()
state = circuit.measureAll()

print(state)
if state[:-1] == [1, 1, 1]:
    print("Function is balanced")
else:
    print("Function is constant")



