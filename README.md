# QuantumEmulator

### Python library for Quantum Simulations

#### Example 1

This example shows how to use ths library. This code describes scheme with 1 qubit and 2 Hadamard gates which are inserted one after the other:

![Alt text](/images/two_h_gates_scheme.bmp?raw=true "Example scheme")

```python
from qsim.qcircuit import QCircuit
from qsim.qconstants import H

circuit = QCircuit()

circuit.addQubits(0) # create 1 qubit with init value 0
circuit.addGates(H, 0) # add 1 column of gates
circuit.addGates(H, 0) # add 2 column of gates

circuit.simulate() # make calculations

state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will be always 0
```

#### Example 2

This code describes scheme with 2 qubits. As empty gate i use I gate, which is called Identity gate. This gate does nothing to qubit.

![Alt text](/images/multiple_qubits_scheme.bmp?raw=true "Example2 scheme")

```python
from qsim.qcircuit import QCircuit
from qsim.qconstants import X
circuit = QCircuit()

circuit.addQubits(0, 0) # create 2 qubits with init value 0
circuit.addGates(X, 1) # add 1 column of gates
circuit.addGates([X, X]) # add 2 column of gates

circuit.simulate() # make calculations
state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will be always [1, 0]
```

#### Example 3

This code describes scheme with 3 qubits. I apply CNOT gate for qubits that are not neigbours

![Alt text](/images/cnot_scheme.bmp?raw=true "Example3 scheme")

```python
from qsim.qcircuit import QCircuit
circuit = QCircuit()

circuit.addQubits(1, 0, 0) # create 1 qubits with init value 1 and 2 qubits with init value 0
circuit.addCNOT(controlIndex=0, targetIndex=2) # add CNOT gate with 0 index qubit as control and 2 index as target

circuit.simulate() # make calculations
state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will be always [1, 0, 1]
```

#### Example 4

This code describes Bell state. This state has 0.5 probabilty to be measured in |00> or |11> states. Also it has probabily of 0 to be in one of this states: |01> or |10>

![Alt text](/images/bell_state_scheme.bmp?raw=true "Example4 scheme")

```python
from qsim.qcircuit import QCircuit
from qsim.qconstants import H
circuit = QCircuit()

circuit.addQubits(0, 0) # create 2 qubits with init value 0
circuit.addGates(H, 0)  # add 1 column of gates
circuit.addCNOT(controlIndex=0, targetIndex=1) # add CNOT gate with 0 index qubit as control and 1 index as target

circuit.simulate() # make calculations
state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will [0, 0] or [1, 1] with probability of 0.5
```

#### Example 5

This code show how to create Toffoli gate. In this case Toffoli gate is using like AND gate in normal boolean logic. If fisrt two qubits are setted to 1 then output witch is setted to 0 will be inverted.

![Alt text](/images/toffoli_scheme.bmp?raw=true "Example5 scheme")

```python
from qsim.qcircuit import QCircuit
circuit = QCircuit()

circuit.addQubits(1, 1, 1) # create 2 qubits with init value 0
circuit.addToffoli([0, 1], 2) # add Toffole gate with 0, 1 qubits as control and 2 qubit as target

circuit.simulate() # make calculations
state = circuit.measureAll() # get state of all qubits
print(state) # in this case output will be always [1, 1, 0]
```
