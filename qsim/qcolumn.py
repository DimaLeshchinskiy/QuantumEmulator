import numpy as np

class QColumn():
    def __init__(self):
        self.matrix = 1
    
    def set(self, values=[]):
        for value in values:
            self.matrix = np.kron(self.matrix, value)
    
    def setControl(self, indexControl, indexTarget, gate):
        pass