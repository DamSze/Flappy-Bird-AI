import pygame
import os


class Background:
    def __init__(self):
        self.img = pygame.image.load(os.path.join('.\\assets', 'bg.png')).convert()
