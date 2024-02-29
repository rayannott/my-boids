import random
from typing import Iterator
from copy import copy

import numpy as np
from scipy.spatial import KDTree
from pygame import Rect, Vector2

from boids import Boid, FollowRules, EdgeBehavior
from objects import StationaryObject, ObjectType, Food, Obstacle
from utils import random_screen_position


class Simulation:
    def __init__(self, screen_rect: Rect):
        self.screen_rect = screen_rect
        self.boids: list[Boid] = []
        self.stationary_objects: list[StationaryObject] = [] # TODO: add other objects to affect the boids
        self.speed_up_factor = 1.
    
    def add_boid(self, boid: Boid):
        self.boids.append(boid)
    
    def add_object(self, obj):
        self.stationary_objects.append(obj)
    
    def add_n_random_boids(self,
            n: int, 
            n_classes: int = 1,
            edge_behavior: EdgeBehavior = EdgeBehavior.WRAP
        ):
        for _ in range(n):
            self.add_boid(
                Boid(
                    random_screen_position(self.screen_rect),
                    class_id=random.choice(list(range(n_classes))),
                    edge_behavior=edge_behavior
                )
            )
    
    def update_follow_rules(self, follow_rules: FollowRules):
        for boid in self.boids:
            boid.rule_flags = copy(follow_rules)
    
    def update_objects(self, time_delta: float):
        for obj in self.stationary_objects:
            boids_to_be_affected = self.get_neighbors_for_point(
                obj.pos, obj.effect_radius + obj.radius)
            for boid in boids_to_be_affected:
                obj.apply_effect_to_boid(boid)
            obj.update(time_delta)
    
    def update(self, time_delta: float):
        time_delta *= self.speed_up_factor

        # Update KDTree
        self.boids_tree = KDTree(np.array([boid.pos for boid in self.boids]))

        all_boids_neighbors = self.get_neighbors_for_all_boids()
        for boid, neighbors in zip(self.boids, all_boids_neighbors):
            boid.align_cohere_separate(neighbors)
            # boid.wander()

        # Update boids
        for boid in self.boids:
            # check edges:
            boid.check_edges(self.screen_rect)
            boid.update(time_delta)
        
        # Update objects
        self.update_objects(time_delta)
        
    def get_neighbors_for_all_boids(self) -> list[Iterator[Boid]]:
        neighbors: Iterator[Iterator[int]] = self.boids_tree.query_ball_point(
            np.array([boid.pos for boid in self.boids]),
            [boid.perception for boid in self.boids],
            p=2.
        )
        return [
            (
                self.boids[i] for i in neighbor
                # if (self.boids[i].pos - self.boids[boid_id].pos).dot(self.boids[boid_id].vel) > 0
            )
            for boid_id, neighbor in enumerate(neighbors)
        ]

    def get_neighbors_for_point(self, point: Vector2, radius: float) -> Iterator[Boid]:
        return (self.boids[i]
            for i in self.boids_tree.query_ball_point(np.array(point), radius, p=2.))

    def iterate_stationary_objects(self) -> Iterator[StationaryObject]:
        return (so for so in self.stationary_objects if so.alive)
