from fractions import Fraction
from math import ceil
from qsim.qcircuit import QCircuit
from qsim.qconstants import H, I, P
from qsim.util.int2bin import binToInt
import random

from numpy import log2, pi, zeros

# euclide algo
def gcd(m, n):
    if m < n: 
        (m, n) = (n, m)
    if(m % n) == 0:
        return n 
    else:
        return (gcd(n, m % n))

# return controlled phaseGate incerse R
def controlled_phaseGate_inverse(m):
    return P(-(2 * pi) / (2 ** m))

def QFT_inverse(circuit, n):
    phaseGates = [controlled_phaseGate_inverse(i) for i in range(2, n + 1)]

    for i in range(n // 2):
        circuit.addSwap(i, n - i - 1)

    for i in range(n, 0, -1):
        for phaseGateIndex in range(n - i, 0, -1):
            circuit.addControlGate(i - 1, phaseGateIndex + i - 1, phaseGates[phaseGateIndex - 1])

        circuit.addGate(H, i - 1)

def Uf(circuit, a, N):
    n1 = 2 * ceil(log2(N)) # first register size
    n2 = ceil(log2(N)) # second register size
    matrix = zeros((2 ** circuit.qbits_size, 2 ** circuit.qbits_size)) # fill matrix with zeros

    for i in range(2 ** circuit.qbits_size):
        x = i >> n2 # high n bits
        y = i & (2 ** n2 - 1) # low n bits

        # let z = (x, ya^x mod N)
        # (ya^x mod N) = (y*(a^x mod N) mod N), so for better performace
        # we will calculate (a^x mod N) separatly, because exponent could be large
        z = x << n2
        if y < N:
            func = pow(base=a, exp=x, mod=N) 
            z = z | ((y * func) % N) 
        else:
            z = z | y

        # insert 1 into column_i and row_z
        matrix[i, z] = 1
    
    # insert permutation matrix to the circuit
    circuit.addCustomMatrix(matrix)

def orderFinding(a, N):
    n1 = 2 * ceil(log2(N)) # first register size
    n2 = ceil(log2(N)) # second register size
    circuit = QCircuit()

    # fill first(control) register of size n with state 0 (|000...000>)
    # fill second(target) register of size n with state 1 (|000...001>)
    # this array represents two registers
    registers = [0] * (n1 + n2)
    registers[-1] = 1
    circuit.addQubits(*registers)

    # apply QFT to the control register
    # or apply H, which has same behavior as QFT applied to |0⟩ ^ n
    # also it has faster implementation
    gatesH = [H] * n1
    gatesI = [I] * n2
    circuit.addGates([*gatesH, *gatesI])

    # apply Uf
    Uf(circuit, a, N)

    # apply QFT_inverse to the control register
    QFT_inverse(circuit, n1)

    circuit.simulate()

    all_r = set()
    measurments = circuit.measureAll(range(8))
    for measurement in measurments:
        state, probability = measurement
        controlRegInt = binToInt(state)

        frac = Fraction(controlRegInt, 2**n1).limit_denominator(N)
        all_r.add(frac.denominator)
    
    return all_r

# https://en.wikipedia.org/wiki/Shor%27s_algorithm
def Factorization(N):
    # step 0, if N is even
    if N % 2 == 0:
        return (2, int(N / 2))

    # step 1
    checked_a = []
    while True:
        a = 0

        while True:
            a = random.randint(2, N - 1)
            if a not in checked_a:
                checked_a.append(a)
                break

        K = gcd(a, N)

        # step 2, 3
        if K != 1:
            return (K, int(N // K))
        # step 4
        else:
            all_r = orderFinding(a, N)

            # step 5, 6, 7 
            for r in all_r:
                if r % 2 == 0 and pow(base=a, exp=r, mod=N) == 1:
                    p = gcd(pow(base=a, exp=r // 2) - 1, N)
                    q = gcd(pow(base=a, exp=r // 2) + 1, N)
                    print(f"r = {r}")
                    return (p, q)

# N = 15 max
print("Factors are: ", Factorization(15))
