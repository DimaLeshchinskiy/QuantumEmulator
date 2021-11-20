# QuantumEmulator

### Python library for Quantum Simulations


#### Example 1
This example shows how to use ths library. This code describes scheme with 1 qubit and 2 Hadamard gates which are inserted one after the other:

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


#### Example 2
This code describes scheme with 2 qubits. As empty gate i use I gate, which is called Identity gate. This gate does nothing to qubit.

![Alt text](/images/multiple_qubits_scheme.bmp?raw=true "Example2 scheme")

```python
from qsim.qcircuit import QCircuit
from qsim.qconstants import X, I
circuit = QCircuit()

circuit.addQubits([0, 0]) # create 2 qubits with init value 0
circuit.addGates([I, X]) # add 1 column of gates
circuit.addGates([X, X]) # add 2 column of gates

circuit.simulate() # make calculations
state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will be always [1, 0]
```
