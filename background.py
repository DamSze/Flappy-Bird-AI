import pygame
import math
import os


class Background:
    def __init__(self):
        self.img = pygame.image.load(os.path.join('.\\assets\sprites', 'bg.png')).convert()
        self.scroll_speed = 5
        self._pos = 0
        self.tiles = 2
        self.scroll = 0

    def draw_inf(self, screen):
        for i in range(0, self.tiles):
            screen.blit(self.img, (i * self.img.get_width() + self.scroll, 0))

        self.scroll -= self.scroll_speed

        if abs(self.scroll) > self.img.get_width():
            self.scroll = 0
