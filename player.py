import pygame
from pygame import mixer
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.img_sprites = [pygame.image.load(os.path.join('.\\assets\sprites', 'bird1.png')).convert(),
                            pygame.image.load(os.path.join('.\\assets\sprites', 'bird2.png')).convert(),
                            pygame.image.load(os.path.join('.\\assets\sprites', 'bird3.png')).convert()]
        self._wing_audio_path = os.path.join('.\\assets\\audio', 'audio_wing.ogg')
        self._sprite_num = 0
        self._tick = 0
        self._max_vel = 24
        self._vel = self._max_vel
        self._is_jumping = False
        self._acc = 1.5
        self._gravity = 6
        self.rect = self.img_sprites[0].get_rect()
        self.rect.x, self.rect.y = 100, 404

    def jump(self, event_list):
        keys = pygame.key.get_pressed()
        for event in event_list:
            if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE] and self._is_jumping is False:
                self._is_jumping = True
                self.wing_sound()
        if self._is_jumping:
            self.rect.y -= self._vel
            self._vel -= self._acc
            if self._vel <= 0:
                self._is_jumping = False
                self._vel = self._max_vel
        self.rect.y += self._gravity

    def animate(self, screen):
        if self._sprite_num >= 2:
            self._sprite_num = 0
        if self._tick % 20 == 0:
            self._sprite_num += 1
        if self._tick >= 60:
            self._tick = 0
        self._tick += 1
        screen.blit(self.img_sprites[self._sprite_num], self.rect)

    def wing_sound(self):
        mixer.music.load(self._wing_audio_path)
        mixer.music.play()






