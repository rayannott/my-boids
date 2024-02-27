import pygame
from pygame import Color

from screen import Screen
from boids import EdgeBehavior, FollowRules
from simulation import Simulation
from gui_utils import ColorGradient, LIGHT_PURPLE, LIGHT_GREEN, LIGHT_YELLOW


WHITE = Color('white')
PURPLE_TO_GREEN = ColorGradient(LIGHT_PURPLE, LIGHT_GREEN)


N_CLASSES = 3

COLOR_LIST = [LIGHT_YELLOW, LIGHT_PURPLE, LIGHT_GREEN]


class SimulationScreen(Screen):
    def __init__(self, surface: pygame.Surface):
        self.simulation = Simulation(surface.get_rect())
        self.simulation.add_n_random_boids(
            n=100, 
            n_classes=N_CLASSES,
            edge_behavior=EdgeBehavior.WRAP
        )
        super().__init__(surface)
        self.paused = False
        self.follow_rules = FollowRules()

    def update(self, time_delta: float):
        if not self.paused:
            self.simulation.update(time_delta)
        self.render()
        return super().update(time_delta)

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

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4:
                self.simulation.speed_up_factor += 0.05
            elif event.button == 5:
                self.simulation.speed_up_factor -= 0.05
            print(f'speedup: {self.simulation.speed_up_factor:.2f}')
        if event.type == pygame.KEYDOWN:
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
            else:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_SPACE:
                    self.simulation.add_n_random_boids(10, n_classes=N_CLASSES)
    

def main():
    pygame.init()
    # surface = pygame.display.set_mode((1000, 800))
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    simulation_screen = SimulationScreen(surface)
    simulation_screen.run()


if __name__ == '__main__':
    main()
