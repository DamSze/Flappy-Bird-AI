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
        self.pipes_down = None
        self.pipes_up = None
        self.score = None
        self.ground = None
        self.size = self.width, self.height = 864, 768
        self.timer = None

        self.config_path = None
        self.nets = []
        self.ge = []
        self.pipe_index = None

    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Flappy bird AI")
        self.players = []
        self.background = Background()
        self.pipes_up = pygame.sprite.Group()
        self.pipes_down = pygame.sprite.Group()
        self.ground = Ground()
        self._running = True
        self.timer = 0
        self.score = 0
        self.pipe_index = 0

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            self.on_cleanup()

    def on_loop(self, event_list, genomes, config):
        for player in list(self.players):
            self.ge[self.players.index(player)].fitness += 0.05
            player.move()
            output = self.nets[self.players.index(player)].activate((player.rect.y,
                                            abs(player.rect.y + player.img_sprites[0].get_height()/2 - self.pipes_up.sprites()[self.pipe_index].rect.y
                                                - self.pipes_up.sprites()[self.pipe_index].image.get_height()/3),
                                            abs(player.rect.y + player.img_sprites[0].get_height()/2 - self.pipes_down.sprites()[self.pipe_index].rect.y
                                                + self.pipes_down.sprites()[self.pipe_index].image.get_height() + 180)))
            pygame.draw.line(self.display_surf,start_pos=(player.rect.x + player.img_sprites[0].get_width()/2, player.rect.y + player.img_sprites[0].get_height()/2), end_pos= (self.pipes_down.sprites()[self.pipe_index].rect.x, self.pipes_down.sprites()[self.pipe_index].rect.y
                                                + self.pipes_down.sprites()[self.pipe_index].image.get_height() + 180), color=(255,160,122), width=1)
            pygame.draw.line(self.display_surf, start_pos=(player.rect.x + player.img_sprites[0].get_width()/2, player.rect.y + player.img_sprites[0].get_height()/2), end_pos=(
            self.pipes_up.sprites()[self.pipe_index].rect.x, self.pipes_up.sprites()[self.pipe_index].rect.y
                                                - self.pipes_up.sprites()[self.pipe_index].image.get_height()/3), color=(240,248,255), width=1)
            pygame.display.update()
            if output[0] > 0.5:
                player.jump(event_list)

            if pygame.sprite.spritecollideany(player, self.pipes_down) or pygame.sprite.spritecollideany(player, self.pipes_up):
                self.ge[self.players.index(player)].fitness -= 1
                self.nets.pop(self.players.index(player))
                self.ge.pop(self.players.index(player))
                self.players.pop(self.players.index(player))
                # self._running = False
                # self.on_execute()

            if pygame.sprite.collide_rect(player, self.ground) or player.rect.y <= 0:
                self.nets.pop(self.players.index(player))
                self.ge.pop(self.players.index(player))
                self.players.pop(self.players.index(player))

            for pipe in self.pipes_down:
                if pipe.rect.x == player.rect.x:
                    self.ge[self.players.index(player)].fitness += 5

        if len(self.players) > 0:
            if self.pipes_down.sprites()[self.pipe_index].rect.x == self.players[0].rect.x:
                self.score += 1
        else:
            self._running = False

    def on_render(self):
        self.background.draw_inf(self.display_surf)
        self.pipes_up.draw(self.display_surf)
        self.pipes_down.draw(self.display_surf)
        self.pipes_up.update()
        self.pipes_down.update()
        self.ground.draw(self.display_surf)
        for player in self.players:
            player.animate(self.display_surf)

        myfont = pygame.font.SysFont("monospace", 40)

        # render text
        label = myfont.render(str(int(self.score)), 1, (255,255,255), (0,0,0))
        self.display_surf.blit(label, (0, 0))

        if self.timer <= 0:
            x_top, x_bottom = 880, 880
            y_bottom = random.randint(-400, -100)
            y_top = y_bottom + 180 + 560
            self.pipes_up.add(Pipe(x_top, y_top, 'pipe_up.png'))
            self.pipes_down.add(Pipe(x_bottom, y_bottom, 'pipe_dwn.png'))
            self.timer = random.randint(140, 200)
        self.timer -= 1

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def get_pipe_index(self):
        if len(self.players) > 0:
            if len(self.pipes_down.sprites()) > 1 and self.players[0].rect.x > self.pipes_down.sprites()[0].rect.x + self.pipes_down.sprites()[0].image.get_width():
                self.pipe_index = 1
        else:
            self._running = False

    def run(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config.txt')
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat. DefaultStagnation,
                                    config_path)
        pop = neat.Population(config)
        pop.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)

        winner = pop.run(self.on_execute, 50)

    def on_execute(self, genomes, config):
        if self.on_init() is False:
            self._running = False

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.nets.append(net)
            self.players.append(Player())
            g.fitness = 0
            self.ge.append(g)

        while self._running:
            self.clock.tick(60)
            event_list = pygame.event.get()
            for event in event_list:
                self.on_event(event)
            self.on_render()
            self.on_loop(event_list, genomes, config)

        # self.on_cleanup()
