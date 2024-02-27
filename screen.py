from abc import ABC, abstractmethod
from statistics import mean, stdev

import pygame
from pygame import Color
import pygame_gui


class Screen(ABC):
    """Abstract class for all screens in the game."""
    def __init__(self,
            surface: pygame.Surface,
            bg_color: Color = Color('#101010'),
            framerate: int = 120
        ):
        self.surface = surface
        self.framerate = framerate
        self.window_size = self.surface.get_rect().size
        self.background = pygame.Surface(self.window_size)
        self.background.fill(Color(bg_color))
        self.manager = pygame_gui.UIManager(self.window_size)
        self.is_running = True

        # adding the quit button
        quit_button_rect = pygame.Rect(0, 0, 0, 0)
        quit_button_rect.size = (25, 25)
        quit_button_rect.topright = self.surface.get_rect().topright
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=quit_button_rect,
            text='',
            manager=self.manager
        )
        self.print_fps_info = True
        self.clock = pygame.time.Clock()
        self.fps_history: list[float] = []

    @abstractmethod
    def process_event(self, event: pygame.event.Event):
        ...
    
    @abstractmethod
    def update(self, time_delta: float):
        ...
    
    def post_run(self):
        if self.print_fps_info:
            print(
                f'''FPSInfo[{self.__class__.__name__}]:
                {mean(self.fps_history):.2f} ± {stdev(self.fps_history):.2f}
                with (min, max) = ({min(self.fps_history):.2f}, {max(self.fps_history):.2f})
                over {len(self.fps_history)} frames.''')

    def process_ui_event(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.quit_button:
                self.is_running = False
        ...
    
    def run(self):
        """Main loop."""
        while self.is_running:
            time_delta = self.clock.tick(self.framerate) * 0.001
            self.fps_history.append(1 / time_delta)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.process_ui_event(event)
                if not self.manager.process_events(event):
                    self.process_event(event)
            self.surface.blit(self.background, (0, 0))
            self.manager.update(time_delta)
            self.update(time_delta)
            self.manager.draw_ui(self.surface)
            pygame.display.update()
        self.post_run()
