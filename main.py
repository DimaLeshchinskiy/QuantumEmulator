from qsim.qcircuit import QCircuit

circuit = QCircuit()

circuit.addQubits([1, 0, 0])
circuit.addCNOT(controlIndex=0, targetIndex=2) 

circuit.simulate()
state = circuit.measureAll()
print(state)



