from statistics import mean, stdev
from collections import defaultdict
from typing import Any
from dataclasses import dataclass, field

from simulation import Simulation


@dataclass
class Stats:
    """
    Class to store statistics.

    directions: velocity angle with respect to the x-axis (grouped by class_id)
    """
    directions: list[defaultdict[int, list[float]]] = field(default_factory=list)
    speeds: list[defaultdict[int, list[float]]] = field(default_factory=list)

    def get_summary(self) -> list[dict[int, tuple[float, float]]]:
        """
        Returns a summary of the statistics:
        a list of dictionaries mapping each class_id to (mean, stdev) of the values.
        """
        raise NotImplementedError()


class StatsManager:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation

        self.stats = Stats()
        
    def update(self):
        _direction = defaultdict(list)
        _speed = defaultdict(list)
        for boid in self.simulation.iterate_boids():
            _direction[boid.class_id].append(boid.vel.as_polar()[1]) # could do math instead, but the performance difference is negligible
            _speed[boid.class_id].append(boid.vel.magnitude())
        self.stats.directions.append(_direction)
        self.stats.speeds.append(_speed) 
    