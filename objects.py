from abc import ABC, abstractmethod
from enum import Enum, auto

from pygame import Vector2

from boids import Boid


class ObjectType(Enum):
    FOOD = auto()
    OBSTACLE = auto()


class StationaryObject(ABC):
    def __init__(self,
        pos: Vector2,
        type: ObjectType,
        radius: float,
        effect_radius: float
        # lifetime: float = float('inf')
    ):
        self.pos = pos
        self.type = type
        self.radius = radius
        self.effect_radius = effect_radius
        self.alive = True
        # self.lifetime = lifetime
    
    @abstractmethod
    def update(self, time_delta: float):
        pass

    @abstractmethod
    def apply_effect_to_boid(self, boid: Boid):
        pass

    def kill(self):
        self.alive = False


class Food(StationaryObject):
    def __init__(self, pos: Vector2, radius: float = 10., effect_radius: float = 50.):
        super().__init__(pos, ObjectType.FOOD, radius, effect_radius)
    
    def update(self, time_delta: float):
        pass

    def apply_effect_to_boid(self, boid: Boid):
        boid.steer(self.pos)
        if boid.pos.distance_to(self.pos) < self.radius:
            self.kill()
            boid.score += 1


class Obstacle(StationaryObject):
    def __init__(self, pos: Vector2, radius: float = 10., effect_radius: float = 50.):
        super().__init__(pos, ObjectType.OBSTACLE, radius, effect_radius)
    
    def update(self, time_delta: float):
        pass

    def apply_effect_to_boid(self, boid: Boid):
        # boid.avoid(self.pos)
        boid.acc += (boid.pos - self.pos).normalize() * 600
    