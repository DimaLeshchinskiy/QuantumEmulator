import numpy as np

#parametrised gates
def P(angle):
    return np.matrix([[1, 0], [0, np.e ** (1j * angle)]], dtype=complex)

def U(theta, fi, _lambda):
    return np.matrix([[np.cos(theta / 2), (-np.e ** (1j * _lambda)) * np.sin(theta / 2)], 
                      [(np.e ** (1j * fi)) * np.sin(theta / 2), (np.e ** (1j * (_lambda  +fi))) * np.cos(theta / 2)]], dtype=complex) 

#states
ZERO = np.array([1, 0], dtype=complex).transpose()
ONE = np.array([0, 1], dtype=complex).transpose()
PLUS = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)], dtype=complex).transpose()
MINUS = np.array([1 / np.sqrt(2), -1 / np.sqrt(2)], dtype=complex).transpose()

#gates
I = np.matrix([[1, 0], [0, 1]], dtype=complex)
X = np.matrix([[0, 1], [1, 0]], dtype=complex)
Y = np.matrix([[0, -1j], [1j, 0]], dtype=complex)
Z = np.matrix([[1, 0], [0, -1]], dtype=complex)
H = 1 / np.sqrt(2) * np.matrix([[1, 1], [1, -1]], dtype=complex)
S = P(np.pi / 2) # sqrt(Z_gate)
SDG = P(-np.pi / 2)
T = P(np.pi / 4)
TDG = P(-np.pi / 4)