from math import ceil
from qsim.qcircuit import QCircuit
from qsim.qconstants import H, I, P

from numpy import log2, pi, zeros

# return controlled phaseGate R
def controlled_phaseGate(m):
    return P((2 * pi) / (2 ** m))

def controlled_phaseGate_inverse(m):
    return P(-(2 * pi) / (2 ** m))

def QFT(circuit, n):
    phaseGates = [controlled_phaseGate(i) for i in range(2, n + 1)]

    for i in range(1, n + 1):
        circuit.addGate(H, i - 1)

        for phaseGateIndex in range(n - i):
            circuit.addControlGate(i - 1, phaseGateIndex + i, phaseGates[phaseGateIndex])

def QFT_inverse(circuit, n):
    phaseGates = [controlled_phaseGate_inverse(i) for i in range(2, n + 1)]

    for i in range(n, 0, -1):
        for phaseGateIndex in range(n - i, 0, -1):
            circuit.addControlGate(i - 1, phaseGateIndex + i - 1, phaseGates[phaseGateIndex - 1])

        circuit.addGate(H, i - 1)

def Uf(circuit, a, N):
    n = circuit.qbits_size // 2 # register size
    matrix = zeros((2 ** circuit.qbits_size, 2 ** circuit.qbits_size)) # fill matrix with zeros

    # iterate over 2 ^ (2n)
    # all possible combinations of x and y
    for i in range(2 ** circuit.qbits_size):
        x = i >> n # high n bits
        y = i & 2 ** (n + 1) - 1 # low n bits

        # let z = (x, ya^x mod N)
        # (ya^x mod N) = (y*(a^x mod N) mod N), so for better performace
        # we will calculate (a^x mod N) separatly, because exponent could be large
        func = pow(base=a, exp=x, mod=N) 
        z = x << n
        z = z | ((y * func) % N) 

        # insert 1 into column_i and row_z
        matrix[i, z] = 1
    
    # insert permutation matrix to the circuit
    circuit.addCustomMatrix(matrix)


def orderFinding(a, N):
    n = 2 * ceil(log2(N)) # one register size
    circuit = QCircuit()
    print(f"Start \t n={n}")

    # fill first(control) register of size n with state 0 (|000...000>)
    # fill second(target) register of size n with state 1 (|000...001>)
    register = [0] * (2 * n)
    register[-1] = 1
    circuit.addQubits(*register)
    print("after Init")

    # apply QFT to the control register
    # QFT(circuit, n)
    # or apply H, which has same behavior as QFT applied to |0⟩ ^ n
    # also it has faster implementation
    gatesH = [H] * n
    gatesI = [I] * n
    circuit.addGates([*gatesH, *gatesI])

    print("after H")

    # apply Uf
    Uf(circuit, a, N)

    print("after Uf")

    # apply QFT_inverse to the control register
    QFT_inverse(circuit, n)
    print("after QFT_inverse")

    circuit.simulate()
    print("after Simulate")
    print(circuit.measureAll())

orderFinding(3, 6)



