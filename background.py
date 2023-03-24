import pygame
import math
import os


class Background:
    def __init__(self):
        self.bg_img = pygame.image.load(os.path.join('.\\assets\sprites', 'bg.png')).convert()
        self.scroll_speed = 5
        self._pos = 0
        self.tiles = 2
        self.scroll = 0

    def draw_inf(self, screen):
        for i in range(0, self.tiles):
            screen.blit(self.bg_img, (i * self.bg_img.get_width(), 0))

