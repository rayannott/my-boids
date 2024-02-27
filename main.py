import random

import pygame
from pygame import Surface, Vector2, Color

from screen import Screen
from boids import Boid, FollowRules
from simulation import Simulation
from gui_utils import ColorGradient, LIGHT_PURPLE, LIGHT_GREEN


WHITE = Color('white')
PURPLE_TO_GREEN = ColorGradient(LIGHT_PURPLE, LIGHT_GREEN)


def random_screen_position(surface: Surface) -> Vector2:
    return Vector2(
        random.uniform(0, surface.get_width()),
        random.uniform(0, surface.get_height())
    )


def current_mouse_position() -> Vector2:
    return Vector2(pygame.mouse.get_pos())


class SimulationScreen(Screen):
    def __init__(self, surface: pygame.Surface):
        self.simulation = Simulation(surface.get_rect())
        for _ in range(300):
            self.simulation.add_boid(
                Boid(
                    random_screen_position(surface),
                    # edge_behavior=random.choice([EdgeBehavior.WRAP, EdgeBehavior.BOUNCE])
                )
            )
        super().__init__(surface)
        self.paused = False
        self.follow_rules = FollowRules()

    def update(self, time_delta: float):
        # boids make a line
        # for i, boid in enumerate(self.simulation.boids):
        #     if i == 0:
        #         boid.steer(current_mouse_position())
        #     else:
        #         boid.steer(self.simulation.boids[i-1].pos)
        if not self.paused:
            self.simulation.update(time_delta)
        self.render()
        return super().update(time_delta)

    def render(self):
        h = 20; a = 7
        for boid in self.simulation.boids:
            # color = PURPLE_TO_GREEN(boid.vel.magnitude() / boid.max_speed)
            color = PURPLE_TO_GREEN(boid.last_num_of_neighbors / 10)
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

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            # if scroll:
            if event.button == 4:
                self.simulation.speed_up_factor += 0.05
            elif event.button == 5:
                self.simulation.speed_up_factor -= 0.05
            print(f'speedup: {self.simulation.speed_up_factor:.2f}')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.paused = not self.paused
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if event.key == pygame.K_a:
                    self.follow_rules.ALIGN = not self.follow_rules.ALIGN
                    print('new follow rules:', self.follow_rules)
                elif event.key == pygame.K_c:
                    self.follow_rules.COHERE = not self.follow_rules.COHERE
                    print('new follow rules:', self.follow_rules)
                elif event.key == pygame.K_s:
                    self.follow_rules.SEPARATE = not self.follow_rules.SEPARATE
                    print('new follow rules:', self.follow_rules)
                self.simulation.update_follow_rules(self.follow_rules)                
    

def main():
    pygame.init()
    # surface = pygame.display.set_mode((1000, 800))
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    simulation_screen = SimulationScreen(surface)
    simulation_screen.run()


if __name__ == '__main__':
    main()
