import pygame
from pygame import Color

from simulation import Simulation
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
    