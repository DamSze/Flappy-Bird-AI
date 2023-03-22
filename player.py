import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load(os.path.join('.\\assets', 'bird1.png')).convert()
        self._max_vel = 20
        self._vel = self._max_vel
        self._is_jumping = False
        self._acc = 1
        self._gravity = 6.5
        self.pos = pygame.math.Vector2((100, 404))


    def jump(self, event_list):
        keys = pygame.key.get_pressed()
        for event in event_list:
            if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE]:
                self._is_jumping = True
        if self._is_jumping:
            self.pos.y -= self._vel
            self._vel -= self._acc
            if self._vel <= 0:
                self._is_jumping = False
                self._vel = self._max_vel
        self.pos.y += self._gravity


    def animate(self):
        animation_rate = 99





