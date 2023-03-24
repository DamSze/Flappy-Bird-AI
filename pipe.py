import pygame
import os


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('.\\assets\\sprites', image)).convert()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.scroll_speed = 3

    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.x <= -self.image.get_width():
            self.kill()



