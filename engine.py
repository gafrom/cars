import numpy as np
from scipy.stats import logistic

class Engine(object):
  def __init__(self):
    self.w1 = np.random.uniform(low=-1, high=1, size=(6, 5))
    self.w2 = np.random.uniform(low=-1, high=1, size=(5, 4))
    self.w3 = np.random.uniform(low=-1, high=1, size=(4, 2))

    self.b1 = np.random.uniform(low=-1, high=1, size=5)
    self.b2 = np.random.uniform(low=-1, high=1, size=4)
    self.b3 = np.random.uniform(low=-1, high=1, size=2)

  def predict(self, inputs):
    normed = logistic.cdf(inputs)
    layer1 = np.maximum(np.matmul(normed, self.w1) + self.b1, 0)
    layer2 = np.maximum(np.matmul(layer1, self.w2) + self.b2, 0)
    output = np.matmul(layer2, self.w3) + self.b3

    return np.tanh(output.flatten())
