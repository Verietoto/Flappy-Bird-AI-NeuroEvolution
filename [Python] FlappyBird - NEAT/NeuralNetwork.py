"""Setting up for neural network function and parameters
"""
from Parameters import *
from numba import jit

class NeuralNetwork():
    def __init__(self, networkShape):
        self.shape = networkShape

    def feedForward(self, input, weight, biases):
        """
        Feed forward input
        :param input: list [xDistance, yDistance]
        :param weight: list [[Weights Layer 1],[Wights Layer 2] ....]
        :param biases: list [[Bias Layer1],[Bias Layer2]]
        :return: Output [value1, value2] value1 is stay, value2 is jump
        """
        self.weights = weight
        self.biasses = biases

        input = np.array(input).reshape(-1)

        FF = copy.deepcopy(input)

        #Feed Forward
        for i in range(len(self.weights)):
            FF = (np.dot(FF, self.weights[i]) + self.biasses[i])
        return FF

    def createBiasses(self):
        """
        create Bias
        :return: list [[Bias Layer1],[Bias Layer2]]
        """
        biasses = []
        for i in range(len(self.shape)-1):
            bias = np.random.uniform(-1,1,self.shape[i+1])
            biasses.append(bias)
        return np.array(biasses)

    def createWeight(self):
        """
        Create Weights
        :return: list [[Weights Layer 1],[Wights Layer 2] ....]
        """
        weights = []
        for i in range(len(self.shape)-1):
            weight = np.random.uniform(-1,1,(self.shape[i], self.shape[i+1]))
            weights.append(weight)
        return np.array(weights)

@jit(nopython=True)
def sigmoid(data):
     return 1/(1+np.exp(-data))

@jit(nopython=True)
def relu(FF):
    return  np.maximum(0,FF)


