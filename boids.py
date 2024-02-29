from dataclasses import dataclass, field
import math, random
from enum import Enum, auto
from typing import Iterable

from pygame import Vector2, Rect

from utils import random_unit_vector


def random_vector() -> Vector2:
    ruv = random_unit_vector()
    ruv.scale_to_length(random.random() * MAX_SPEED)
    return ruv


MAX_SPEED = 450
MAX_ACC = 200

SEPARATION = 30
ALIGNMENT = 60
COHESION = 80
PERCEPTION = 90

REPELL_FRIENDS_COEF = 8.
REPELL_ENEMIES_COEF = 30.


class EdgeBehavior(Enum):
    WRAP = auto()
    BOUNCE = auto()
    IGNORE = auto()
    AVOID = auto() # steer away from the edge when too close


@dataclass
class FollowRules:
    ALIGN: bool = True
    COHERE: bool = True
    SEPARATE: bool = True


class GeneSequence:
    ...


@dataclass(slots=True)
class Boid:
    pos: Vector2
    vel: Vector2 = field(default_factory=random_vector)
    acc: Vector2 = field(default_factory=Vector2)
    max_speed: float = MAX_SPEED
    max_acc: float = MAX_ACC
    perception: float = PERCEPTION # neighborhood: radius of the circle that defines the boid's perception

    separation: float = SEPARATION # distance at which the boid will start to avoid other boids
    alignment: float = ALIGNMENT # distance at which the boid will start to align with other boids
    cohesion: float = COHESION # distance at which the boid will start to move towards other boids
    rule_flags: FollowRules = field(default_factory=FollowRules)

    class_id: int = 0 # determines the friend class of the boid

    edge_behavior: EdgeBehavior = EdgeBehavior.WRAP

    class_id: int = 0
    rule_flags: FollowRules = field(default_factory=FollowRules, init=False)
    last_num_of_neighbors: int = field(default=0, init=False)
    score: int = field(default=0, init=False)

    def update(self, time_delta: float):
        self.vel += self.acc * time_delta
        self.vel = self.vel.normalize() * min(self.vel.magnitude(), self.max_speed)
        self.pos += self.vel * time_delta
        self.acc *= 0.
    
    def check_edges(self, screen_rect: Rect):
        if self.edge_behavior == EdgeBehavior.IGNORE:
            return
        if self.edge_behavior == EdgeBehavior.WRAP:
            if self.pos.x < screen_rect.left:
                self.pos.x = screen_rect.right
            elif self.pos.x > screen_rect.right:
                self.pos.x = screen_rect.left
            if self.pos.y < screen_rect.top:
                self.pos.y = screen_rect.bottom
            elif self.pos.y > screen_rect.bottom:
                self.pos.y = screen_rect.top
        elif self.edge_behavior == EdgeBehavior.BOUNCE:
            # TODO: fix getting stuck in the edges
            if self.pos.x < screen_rect.left or self.pos.x > screen_rect.right:
                self.vel.x *= -1
            if self.pos.y < screen_rect.top or self.pos.y > screen_rect.bottom:
                self.vel.y *= -1
            # self.pos += self.vel
        elif self.edge_behavior == EdgeBehavior.AVOID:
            # raise NotImplementedError('EdgeBehavior.AVOID')
            MARGIN = 150; ACC_MAGNITUDE = MAX_ACC * 3
            if self.pos.x < screen_rect.left + MARGIN:
                self.acc += Vector2(ACC_MAGNITUDE, 0)
            elif self.pos.x > screen_rect.right - MARGIN:
                self.acc += Vector2(-ACC_MAGNITUDE, 0)
            if self.pos.y < screen_rect.top + MARGIN:
                self.acc += Vector2(0, ACC_MAGNITUDE)
            elif self.pos.y > screen_rect.bottom - MARGIN:
                self.acc += Vector2(0, -ACC_MAGNITUDE)
    
    def get_steering_acc(self, pos: Vector2) -> Vector2:
        desired = pos - self.pos
        if not desired.magnitude_squared(): return Vector2()
        steering = desired.normalize() * self.max_speed - self.vel
        if not steering.magnitude_squared(): return Vector2()
        return steering.normalize() * self.max_acc

    def steer(self, pos: Vector2):
        self.acc += self.get_steering_acc(pos)
    
    def avoid(self, pos: Vector2):
        self.acc -= self.get_steering_acc(pos)
    
    def accelerate_towards(self, pos: Vector2, magnitude: float = MAX_ACC):
        self.acc += (pos - self.pos).normalize() * magnitude

    def align_cohere_separate(self, boids: Iterable['Boid']):
        center_of_mass, count = Vector2(), 0
        align_accumulate_vel, count_align = Vector2(), 0
        for boid in boids:
            if boid is self: continue
            dist_to_boid = (boid.pos - self.pos).magnitude()
            weighted_acceleration = (boid.pos - self.pos) / dist_to_boid**2
            weighted_acceleration *= self.max_acc
            if self.class_id != boid.class_id:
                self.acc -= weighted_acceleration * REPELL_ENEMIES_COEF # repell enemies
                continue
            center_of_mass += boid.pos; count += 1
            if dist_to_boid < self.separation:
                if self.rule_flags.SEPARATE:
                    self.acc -= weighted_acceleration * REPELL_FRIENDS_COEF # SEPARATE
            elif dist_to_boid < self.alignment:
                align_accumulate_vel += boid.vel; count_align += 1
        if count_align:
            align_accumulate_vel /= count_align
            if self.rule_flags.ALIGN:
                self.steer(self.pos + align_accumulate_vel) # ALIGN
        if count:
            # this is the cohesion part
            center_of_mass /= count
            dist_to_com_sq = (center_of_mass - self.pos).magnitude_squared()
            if dist_to_com_sq < self.cohesion ** 2:
                if self.rule_flags.COHERE:
                    self.steer(center_of_mass) # COHERE
        self.last_num_of_neighbors = count
    
    def wander(self):
        # TODO: implement this
        ...
    