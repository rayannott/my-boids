import math
import random

import pygame

from screen import Screen
from render_manager import RenderManager
from boids import EdgeBehavior, FollowRules
from objects import Food, Obstacle
from simulation import Simulation
from utils import current_mouse_position


N_CLASSES = 4


class SimulationScreen(Screen):
    def __init__(self, surface: pygame.Surface):
        self.simulation = Simulation(surface.get_rect())
        self.simulation.add_n_random_boids(
            n=100, 
            n_classes=N_CLASSES,
            edge_behavior=EdgeBehavior.WRAP
        )
        super().__init__(surface)
        self.follow_rules = FollowRules()

        self.paused = False

        self.render_manager = RenderManager(self.simulation, self.surface)

    def update(self, time_delta: float):
        if not self.paused:
            self.simulation.update(time_delta)
        self.render()
        return super().update(time_delta)

    def render(self):
        self.render_manager.render()

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button in {4, 5}:
                self.simulation.speed_up_factor += 0.05 * (1 if event.button == 4 else -1)
                print(f'speedup: {self.simulation.speed_up_factor:.2f}')
            elif event.button == 1:
                for boid in self.simulation.get_neighbors_for_point(current_mouse_position(), 150):
                    boid.vel = boid.vel.rotate_rad(random.random() * 2 * math.pi)
                
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                # control follow rules:
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
                elif event.key == pygame.K_f:
                    self.simulation.add_object(Food(current_mouse_position(), 10))
                elif event.key == pygame.K_o:
                    self.simulation.add_object(Obstacle(current_mouse_position(), 20, 100))

    