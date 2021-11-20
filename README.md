# QuantumEmulator

### Python library for Quantum Simulations


#### Example
This example shows how to use ths library. This code describe scheme with 1 qubit and 2 Hadamard gates which are inserted one after the other:

![Alt text](/images/two_h_gates_scheme.bmp?raw=true "Example scheme")

```python
from qsim.qcircuit import QCircuit
from qsim.qconstants import H

circuit = QCircuit()

circuit.addQubits([0]) # create 1 qubit with init value 0
circuit.addGates([H]) # add 1 column of gates
circuit.addGates([H]) # add 2 column of gates

circuit.simulate() # make calculations

state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will be always 0
```
