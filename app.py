import pygame
from player import Player
from background import Background
import random
from pipe import Pipe
from ground import Ground


class App:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self._running = True
        self.display_surf = None
        self.player = None
        self.background = None
        self.pipes = None
        self.score = None
        self.ground = None
        self.size = self.width, self.height = 864, 768
        self.timer = None

    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Flappy bird AI")
        self.player = Player()
        self.background = Background()
        self.pipes = pygame.sprite.Group()
        self.ground = Ground()
        self._running = True
        self.timer = 0
        self.score = 0

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self, event_list):
        self.player.jump(event_list)
        if pygame.sprite.spritecollideany(self.player, self.pipes):
            self._running = False

        if pygame.sprite.collide_rect(self.player, self.ground):
            self._running = False

        for pipe in self.pipes:
            if pipe.rect.x == self.player.rect.x:
                self.score += 0.5

            if pipe.rect.x + pipe.image.get_width() < 0:
                pipe.kill()

    def on_render(self):
        self.background.draw_inf(self.display_surf)
        self.pipes.draw(self.display_surf)
        self.pipes.update()
        self.ground.draw(self.display_surf)
        self.player.animate(self.display_surf)

        myfont = pygame.font.SysFont("monospace", 40)

        # render text
        label = myfont.render(str(int(self.score)), 1, (255,255,255), (0,0,0))
        self.display_surf.blit(label, (0, 0))

        if self.timer <= 0:
            x_top, x_bottom = 880, 880
            y_bottom = random.randint(-400, -100)
            y_top = y_bottom + 180 + 560
            self.pipes.add(Pipe(x_top, y_top, 'pipe.png'))
            self.pipes.add(Pipe(x_bottom, y_bottom, 'pipe_dwn.png'))
            self.timer = random.randint(140, 200)
        self.timer -= 1

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            self.clock.tick(60)
            event_list = pygame.event.get()
            for event in event_list:
                self.on_event(event)
            self.on_loop(event_list)
            self.on_render()

        self.on_cleanup()
