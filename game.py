import math
from PIL import Image
import numpy as np
np.set_printoptions(threshold = 50000, linewidth = 500)


from car import Car

map = np.array(Image.open('race_mask.png'))
print(f"Map dimensions: {map.shape}")

cars = [Car().bind(map, 100, 100, -math.pi/4) for i in range(8)]
# car = Car().bind(map, 100, 100, -math.pi/4)

for n, car in enumerate(cars):
  map[car.j][car.i] = n + 2
  # print(map[50:140, 50:140])

  for i in range(1000):
    car.move()
    map[car.j][car.i] = n + 2

print(map[70:130, 50:170])
