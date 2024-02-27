import pygame
from pygame import Color

from simulation import Simulation
from gui_utils import ColorGradient, LIGHT_PURPLE, LIGHT_GREEN, LIGHT_YELLOW

COLOR_LIST = [LIGHT_GREEN, LIGHT_PURPLE, LIGHT_YELLOW]


WHITE = Color('white')
PURPLE_TO_GREEN = ColorGradient(LIGHT_PURPLE, LIGHT_GREEN)


class RenderManager:
    def __init__(self, 
        simulation: Simulation,
        surface: pygame.Surface
    ):
        self.simulation = simulation
        self.surface = surface

    
    def render(self):
        h = 20; a = 7
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
                    boid.pos + vel_normalized_orth_plus * a,
                    boid.pos + vel_normalized * h,
                    boid.pos + vel_normalized_orth_minus * a,
                ]
            )
    