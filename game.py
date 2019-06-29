import math
from PIL import Image
import numpy as np
np.set_printoptions(threshold = 50000, linewidth = 500)


from car import Car

map = np.array(Image.open('race_mask.png'))
print(f"Map dimensions: {map.shape}")


car = Car(v = 5).bind(map, 100, 100, -math.pi/4)

map[car.pos()[1]][car.pos()[0]] = 7
# print(map[50:140, 50:140])

for i in range(10):
  car.move()
  map[car.pos()[1]][car.pos()[0]] = 7

car.angle += math.pi/4
car.v += 2
for i in range(10):
  car.move()
  map[car.pos()[1]][car.pos()[0]] = 6

car.angle += math.pi/4
car.v += 2
for i in range(10):
  car.move()
  map[car.pos()[1]][car.pos()[0]] = 5

car.angle += math.pi/4
car.v += 2
for i in range(30):
  car.move()
  map[car.pos()[1]][car.pos()[0]] = 4

print(map[70:130, 50:170])
