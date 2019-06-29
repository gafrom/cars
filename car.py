import math

class Car(object):
  T = 100 # miliseconds to drive in one move
  EYES = [-math.pi/2, -math.pi/4, 0, math.pi/4, math.pi/2]
  MIN_NUM_MOVES = 1000 # no matter how small the map might come we need at least that many moves

  def __init__(self, v = 0, a = 0, rr = 0):
    self.v     = v     # velocity, moves per second
    self.a     = a     # acceleration (+) or slowing down (-), [-1..1]
    self.rr    = rr    # rolling resistance, [0..1]
    self.stuck = False # stuck or free to move

  def bind(self, map, x = 0, y = 0, angle = 0, scale = None):
    self.map       = map # a racing map
    self.xlen, self.ylen = map.shape
    self.angle     = angle # in relation to X axis
    self.scale     = self.calc_scale() if scale is None else scale
    self.x, self.y = x/self.scale, y/self.scale # position

    return self

  def pos(self):
    return self.pos_on_map(self.x, self.y)

  def move(self):
    if self.stuck: return

    distances = self.look_around()
    self.adjust_parameters(distances)
    self.advance()

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

  def adjust_parameters(self, distances):
    print(list(map(lambda x: int(x), distances)))

  def advance(self, t = T):
    self.x += math.cos(self.angle) * self.v * t/1000
    self.y += math.sin(self.angle) * self.v * t/1000

  def calc_scale(self):
    return self.map.shape[0]/self.MIN_NUM_MOVES

  def pos_on_map(self, x, y):
    return [int(x * self.scale), int(y * self.scale)]

  def __str__(self):
    return f"({self.x}, {self.y}) @ {self.angle * 180}°"
