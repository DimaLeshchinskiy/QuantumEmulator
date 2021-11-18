from qsim.qcircuit import QCircuit

circuit = QCircuit()

circuit.addQubit(initValue=0)

circuit.addH(index=0)

state = circuit.measureAll()

print(state)

