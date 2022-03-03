import math
import random


class City:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'({round(self.x, 2)}, {round(self.y, 2)}, {round(self.z, 2)})'

    @staticmethod
    def distance_symmetric(c1, c2):
        return math.sqrt((c1.x-c2.x)**2 + (c1.y-c2.y)**2 + (c1.z-c2.z)**2)

    @staticmethod
    def distance_asymmetric(c1, c2):
        multiplier = 1
        if c1.z > c2.z:
            multiplier = 0.9
        elif c1.z < c2.z:
            multiplier = 1.1
        return City.distance_symmetric(c1, c2) * multiplier

    @staticmethod
    def generate(count, x_range, y_range, z_range, seed=None):
        if seed:
            random.seed(seed)
        return [City._generate_single(x_range, y_range, z_range) for _ in range(0, count)]

    @staticmethod
    def _generate_single(x_range, y_range, z_range):
        x = random.random() * (x_range[1]-x_range[0]) + x_range[0]
        y = random.random() * (y_range[1]-y_range[0]) + y_range[0]
        z = random.random() * (z_range[1]-z_range[0]) + z_range[0]
        return City(x, y, z)
