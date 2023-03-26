import pygame
from player import Player
from background import Background
import random
from pipe import Pipe
from ground import Ground
import os
import neat


class App:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self._running = True
        self.display_surf = None
        self.players = []
        self.background = None
        self.pipes = None
        self.score = None
        self.ground = None
        self.size = self.width, self.height = 864, 768
        self.timer = None

        self.local_dir = None
        self.config_path = None
        self.nets = []
        self.ge = []

    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Flappy bird AI")
        self.player = []
        self.background = Background()
        self.pipes = pygame.sprite.Group()
        self.ground = Ground()
        self._running = True
        self.timer = 0
        self.score = 0
        self.local_dir = os.path.dirname(__file__)
        self.config_path = os.path.join(self.local_dir, 'config.txt')

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self, event_list, genomes, config):
        for g in genomes:
            net = neat.nn.FeedForwardNetwork(g, config)
            self.nets.append(net)
            self.players.append(Player())
            g.fitness = 0
            self.ge.append(g)

        for x, player in enumerate(self.players):
            player.jump(event_list)
            if pygame.sprite.spritecollideany(player, self.pipes):
                self.ge[x] -= 1
                self.players.pop(x)
                self.nets.pop(x)
                self.ge.pop(x)
                self._running = False
                # self.on_execute()

            if pygame.sprite.collide_rect(player, self.ground):
                self.players.pop(x)
                self.nets.pop(x)
                self.ge.pop(x)

            for pipe in self.pipes:
                if pipe.rect.x == player.rect.x:
                    self.score += 0.5
                    self.ge[x].fitness += 5

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

    def run(self):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat. DefaultStagnation,
                                    self.config_path)
        pop = neat.Population(config)
        pop.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)

        winner = pop.run(self.on_execute(), 50)

    def on_execute(self, genomes, config):
        if self.on_init() is False:
            self._running = False

        while self._running:
            self.clock.tick(60)
            event_list = pygame.event.get()
            for event in event_list:
                self.on_event(event)
            self.on_loop(event_list)
            self.on_render()

        # self.on_cleanup()
