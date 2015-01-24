import pygame

class Camera:
    def __init__(self, screen, world):
        self.screen = pygame.Rect(screen)
        self.world = pygame.Rect(world)
