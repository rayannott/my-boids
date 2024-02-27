import math
import random
from pygame import Vector2, Rect
import pygame


def random_screen_position(rect: Rect) -> Vector2:
    return Vector2(
        random.uniform(rect.left, rect.right),
        random.uniform(rect.top, rect.bottom)
    )


def random_unit_vector() -> Vector2:
    a = random.random() * 2 * math.pi
    return Vector2(math.cos(a), math.sin(a))


def current_mouse_position() -> Vector2:
    return Vector2(pygame.mouse.get_pos())
