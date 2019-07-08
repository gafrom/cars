import math
import numpy as np

from engine import Engine

class Car(object):
  T = 0.1 # seconds to drive in one move
  EYES = [-math.pi/2, -math.pi/4, 0, math.pi/4, math.pi/2]
  MIN_NUM_MOVES = 1000 # no matter how small the map might come we need at least that many moves

  # let's keep in memory all cars manufactured
  count = 0
  all = {}

  def __init__(self, v=0, a=0, s=0, rr=0.1, parents=None):
    self.v     = v     # velocity, moves per second
    self.a     = a     # acceleration (positive) or slowing down (negative); a ∈ R[-1..1]
    self.s     = s     # steer left (negative) or right (positive); s ∈ R[-1..1]
    self.rr    = rr    # rolling resistance; rr ∈ R[0..1]
    self.stuck = False # stuck or free to move
    self.engine = Engine(parents=self.engines_of(parents))

    self.__class__.count += 1
    self.id = self.__class__.count
    self.__class__.all[self.id] = self

  def bind(self, map, x = 0, y = 0, angle = 0, scale = None):
    self.map       = map # a racing map
    self.xlen, self.ylen = map.shape
    self.angle     = angle # in relation to X axis
    self.scale     = self.calc_scale() if scale is None else scale
    self.norm      = self.MIN_NUM_MOVES / 5 # to feed sigmoid(x) with x ∈ R[-5..5]
    self.i, self.j = x, y # indices on map
    self.x, self.y = x/self.scale, y/self.scale # position ∈ R

    return self

  def move(self, t=T):
    if self.stuck: return

    distances = self.look_around()
    self.correct_behavior(distances, t)
    self.advance(t)

  def look_around(self):
    return [self.look_into_direction(angle) for angle in self.EYES]

  def look_into_direction(self, angle):
    x, y = self.x, self.y
    look_at = self.angle + angle

    while True:
      x += math.cos(look_at) / self.scale
      y += math.sin(look_at) / self.scale

      i, j = self.pos_on_map(x, y)

      if not (0 <= j < self.ylen and 0 <= i < self.xlen and self.map[j][i] != 1): break

    return math.sqrt((x - self.x)**2 + (y - self.y)**2) # distance

  def correct_behavior(self, distances, t):
    feed_data = np.array([distances + [self.v]]) / self.norm
    predictions = self.engine.predict(feed_data)

    self.a, self.s = predictions

    self.v += self.a * t
    self.angle += self.s * t

  def advance(self, t):
    self.x += math.cos(self.angle) * self.v * t
    self.y += math.sin(self.angle) * self.v * t
    self.i, self.j = self.pos_on_map(self.x, self.y)

    if self.map[self.j][self.i] == 1: self.stuck = True

  def calc_scale(self):
    return self.map.shape[0]/self.MIN_NUM_MOVES

  def pos_on_map(self, x, y):
    return [int(x * self.scale), int(y * self.scale)]

  def engines_of(self, ids):
    if not ids: return
    elif ids.__class__ == list: return [self.engine_of(id) for id in ids]
    elif ids.__class__ == self.__class__: return [self.engine]
    elif ids.__class__ == int: return [self.engine_of(ids)]
    elif ids.__class__ == str: return [self.engine_of(str(id))]
    else: raise f"Ooouch! Don't know how to get an engine out of {ids.__class__} instance."

  def engine_of(self, id):
    return Car.all[id].engine

  def __str__(self):
    return f"Car[{self.id}]({self.i}, {self.j}) @ {self.angle * 180}°"
