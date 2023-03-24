import pygame
import math
import os


class Ground:
    def __init__(self):
        self.img = pygame.image.load(os.path.join('.\\assets\sprites', 'base.png')).convert()
        self.scroll_speed = 3
        self.rect = self.img.get_rect()
        self.rect.y = 768 - self.img.get_height()
        self.tiles = math.ceil(864/self.img.get_width()) + 3
        self.scroll = 0

    def draw(self, screen):
        for i in range(0, self.tiles):
            screen.blit(self.img, (i * self.img.get_width() + self.scroll, 768 - self.img.get_height()))


        self.scroll -= self.scroll_speed

        if abs(self.scroll) > self.img.get_width():
            self.scroll = 0