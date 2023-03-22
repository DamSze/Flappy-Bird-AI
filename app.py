import pygame
from player import Player
from background import Background


class App:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self._running = True
        self._display_surf = None
        self.player = None
        self.background = None
        self.size = self.width, self.height = 864, 768

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Flappy bird AI")
        self.player = Player()
        self.background = Background()
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self, event_list):
        self.player.jump(event_list)



    def on_render(self):
        self._display_surf.blit(self.background.img, (0, 0))
        self._display_surf.blit(self.player.img, self.player.pos)
        pygame.display.flip()

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
