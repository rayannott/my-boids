from typing import Iterator
from copy import copy

import numpy as np
from scipy.spatial import KDTree
from pygame import Rect

from boids import Boid, FollowRules


class Simulation:
    def __init__(self, screen_rect: Rect):
        self.screen_rect = screen_rect
        self.boids: list[Boid] = []
        self.other_objects: list = [] # TODO: add other objects to affect the boids
        self.speed_up_factor = 1.
    
    def add_boid(self, boid: Boid):
        self.boids.append(boid)
    
    def update_follow_rules(self, follow_rules: FollowRules):
        for boid in self.boids:
            boid.rule_flags = copy(follow_rules)
    
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
        
    def get_neighbors_for_all_boids(self) -> list[Iterator[Boid]]:
        neighbors: Iterator[Iterator[int]] = self.boids_tree.query_ball_point(
            np.array([boid.pos for boid in self.boids]),
            [boid.perception for boid in self.boids],
            p=2.
        )
        return [
            (
                self.boids[i] for i in neighbor
                # add if within perception angle
            )
            for boid_id, neighbor in enumerate(neighbors)
        ]
    