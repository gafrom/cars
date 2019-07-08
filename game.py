import math
from PIL import Image
import numpy as np
np.set_printoptions(threshold = 50000, linewidth = 500)
from car import Car

####################################################################################################

ids = None

while True:
  if Car.count > 0:
    ids = list(map(lambda x: int(x), input('Please enter parents IDs separated by commas: ').split(',')))

  race_map = np.array(Image.open('race_mask.png'))
  # print(f"Map dimensions: {race_map.shape}")

  cars = [Car(parents=ids).bind(race_map, 100, 100, -math.pi/4) for i in range(8)]

  for n, car in enumerate(cars):
    for i in range(700):
      car.move()
      race_map[car.j][car.i] = car.id

  print(race_map[70:130, 50:170])
