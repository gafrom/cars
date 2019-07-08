import numpy as np
from scipy.stats import logistic

class Engine(object):
  WEIGHT_SHAPE = {
    'w1': (6, 5),
    'w2': (5, 4),
    'w3': (4, 2),
    'b1': (5,),
    'b2': (4,),
    'b3': (2,)
  }

  def __init__(self, parents=None):
    if parents is None:
      for key, shape in self.WEIGHT_SHAPE.items():
        setattr(self, key, np.random.uniform(low=-1, high=1, size=shape))
    else:
      # evolution begins here...
      try:              iter(parents)
      except TypeError: self.evolve_from([parents])
      else:             self.evolve_from(parents)

  def predict(self, inputs):
    normed = logistic.cdf(inputs)
    layer1 = np.maximum(np.matmul(normed, self.w1) + self.b1, 0)
    layer2 = np.maximum(np.matmul(layer1, self.w2) + self.b2, 0)
    output = np.matmul(layer2, self.w3) + self.b3

    return np.tanh(output.flatten())

  def evolve_from(self, parents):
    num_parents = len(parents)
    for key, shape in self.WEIGHT_SHAPE.items():
      engines = np.array([getattr(engine, key) for engine in parents])
      random = np.random.randint(low=0, high=num_parents, size=shape)
      result = np.zeros(shape)
      for index in range(num_parents):
        result += engines[index] * (random == index)
      setattr(self, key, result)
