import pygame

from simulation_screen import SimulationScreen


def main():
    pygame.init()
    # surface = pygame.display.set_mode((1000, 800))
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    simulation_screen = SimulationScreen(surface)
    simulation_screen.run()


if __name__ == '__main__':
    main()
