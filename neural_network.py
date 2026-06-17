import numpy as np


class NeuralNetwork:
    def __init__(self):
        self.weights = np.random.uniform(-1, 1, (7, 2))
        
    def predict(self, inputs):
        return np.dot(inputs, self.weights)
    
