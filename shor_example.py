from fractions import Fraction
from math import ceil, floor
from qsim.qcircuit import QCircuit
from qsim.qconstants import H, I, P
from qsim.util.int2bin import binToInt

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
        y = i & (2 ** n - 1) # low n bits

        # let z = (x, ya^x mod N)
        # (ya^x mod N) = (y*(a^x mod N) mod N), so for better performace
        # we will calculate (a^x mod N) separatly, because exponent could be large
        z = x << n
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
    n = ceil(log2(N)) # one register size
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

def Uf2(circuit, a, N):
    n1 = 2 * ceil(log2(N)) # one register size
    n2 = ceil(log2(N))
    # n = circuit.qbits_size // 2 # register size
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

        print(x, y, (y * func) % N, z)

        # insert 1 into column_i and row_z
        matrix[i, z] = 1
    
    # insert permutation matrix to the circuit
    circuit.addCustomMatrix(matrix)

def orderFinding2(a, N):
    n1 = 2 * ceil(log2(N)) # one register size
    n2 = ceil(log2(N))
    circuit = QCircuit()
    print(f"Start \t n1={n1} n2={n2}")

    # fill first(control) register of size n with state 0 (|000...000>)
    # fill second(target) register of size n with state 1 (|000...001>)
    register = [0] * (n1 + n2)
    register[-1] = 1
    print(register)
    circuit.addQubits(*register)
    print("after Init")

    # apply QFT to the control register
    # QFT(circuit, n)
    # or apply H, which has same behavior as QFT applied to |0⟩ ^ n
    # also it has faster implementation
    gatesH = [H] * n1
    gatesI = [I] * n2
    circuit.addGates([*gatesH, *gatesI])

    print("after H")

    # apply Uf
    Uf2(circuit, a, N)

    print("after Uf")

    # apply QFT_inverse to the control register
    QFT_inverse(circuit, n1)
    print("after QFT_inverse")

    circuit.simulate()
    print("after Simulate")

    for i in range(10):

        measure = circuit.measureAll()
        controlRegInt = binToInt(measure[:n1])

        print(controlRegInt, measure[:n1])

        frac = Fraction(controlRegInt, 2**n1).limit_denominator(N)
        print(measure)
        print(controlRegInt, 2**n1, controlRegInt / (2**n1))
        print(f"{frac.numerator}/{frac.denominator}")
        print("----------------------------")

# N = 35 max
orderFinding2(7, 15)

# import math
# import random

# #euklide algo
# def gcd(m, n):
#     if m < n: 
#         (m, n) = (n, m)
#     if(m % n) == 0:
#         return n 
#     else:
#         return (gcd(n, m % n))

# # https://tsmatz.wordpress.com/2019/06/04/quantum-integer-factorization-by-shor-period-finding-algorithm/
# def Factorization(N):
#     #step 1
#     if N % 2 == 0:
#         return (2, int(N / 2))

#     #step 2
#     log_2 = math.log(N, 2)
#     for j in range(2, int(log_2 + 1)):
#         for k in range(2, int(log_2 + 1)):
#             if math.pow(N, 1 / k) == j:
#                 return (j, int(N / j))

#     #step 3
#     checked_a = []
#     while True:
#         a = 0

#         while True:
#             a = random.randint(2, N - 1)
#             if a not in checked_a:
#                 checked_a.append(a)
#                 break

#         print("Random: ", a)
#         gcdRes = gcd(N, a)

#         #step 4
#         if gcdRes > 1:
#             return (gcdRes, int(N / gcdRes))
#         #step 5
#         else:
#             r = orderFinding2(a, N)

#             #step 6
#             if r == None or r % 2 == 0:
#                 continue
            
#             #step 7
#             a_pow = math.pow(a, r / 2)
#             if r % 2 == 1 and a_pow % N == N - 1:
#                 continue
#             else:
                
#                 #step 8
#                 signums = [-1, 1]
#                 for signum in signums:

#                     gcdRes = gcd(a_pow + signum, N)
#                     if gcdRes != 1 and gcdRes != N:
#                         return (a_pow + signum, int(N / a_pow + signum))

# # print("Factors are: ", Factorization(15))
