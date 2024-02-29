import pygame
from pygame import Color

from simulation import Simulation
from objects import ObjectType
from gui_utils import ColorGradient, LIGHT_PURPLE, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_RED

COLOR_LIST = [LIGHT_GREEN, LIGHT_PURPLE, LIGHT_YELLOW, LIGHT_RED]


WHITE = Color('white')
PURPLE_TO_GREEN = ColorGradient(LIGHT_PURPLE, LIGHT_GREEN)

H = 20
A = 7

class RenderManager:
    def __init__(self, 
        simulation: Simulation,
        surface: pygame.Surface
    ):
        self.simulation = simulation
        self.surface = surface

    
    def render(self):
        for obj in self.simulation.iterate_stationary_objects():
            pygame.draw.circle(self.surface, Color('black'), obj.pos, obj.effect_radius, 1)
            if obj.type == ObjectType.FOOD:
                pygame.draw.circle(self.surface, Color('green'), obj.pos, 10)
            elif obj.type == ObjectType.OBSTACLE:
                pygame.draw.circle(self.surface, Color('red'), obj.pos, 10)
        for boid in self.simulation.boids:
            # color = PURPLE_TO_GREEN(boid.vel.magnitude() / boid.max_speed)
            # color = PURPLE_TO_GREEN(boid.last_num_of_neighbors / 10)
            color = COLOR_LIST[boid.class_id]

            vel_normalized = boid.vel.normalize()
            vel_normalized_orth_plus = vel_normalized.rotate(115)
            vel_normalized_orth_minus = vel_normalized.rotate(-115)
            pygame.draw.polygon(
                self.surface,
                color,
                [
                    boid.pos,
                    boid.pos + vel_normalized_orth_plus * A,
                    boid.pos + vel_normalized * H,
                    boid.pos + vel_normalized_orth_minus * A,
                ]
            )
    