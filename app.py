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
        self.pop = None
        self.nets = []
        self.ge = []
        self.pipe_gap = 150

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

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            self.on_cleanup()

    def on_loop(self, event_list, genomes, config):
        for player in list(self.players):
            self.ge[self.players.index(player)].fitness += 0.05
            output = self.nets[self.players.index(player)].activate((player.rect.y,
                                            abs(player.rect.y + player.img_sprites[0].get_height()/2 - self.pipes_up.sprites()[0].rect.y
                                                - self.pipes_up.sprites()[0].image.get_height()/3.73),
                                            abs(player.rect.y + player.img_sprites[0].get_height()/2 - self.pipes_down.sprites()[0].rect.y
                                                + self.pipes_down.sprites()[0].image.get_height() + self.pipe_gap)))
            if output[0] > 0.5:
                player.jump(event_list)

            player.move()
            if len(self.players) == 0:
                self._running = False

            # pipe collision
            if pygame.sprite.spritecollideany(player, self.pipes_down) or pygame.sprite.spritecollideany(player, self.pipes_up):
                self.ge[self.players.index(player)].fitness -= 1
                self.nets.pop(self.players.index(player))
                self.ge.pop(self.players.index(player))
                self.players.pop(self.players.index(player))
            # ground collision and out of screen
            if pygame.sprite.collide_rect(player, self.ground) or player.rect.y <= 0:
                self.nets.pop(self.players.index(player))
                self.ge.pop(self.players.index(player))
                self.players.pop(self.players.index(player))

            # increasing fitness when passing through the pipe
            for pipe in self.pipes_down:
                if pipe.rect.x == player.rect.x:
                    self.ge[self.players.index(player)].fitness += 5

        # increasing the score
        if len(self.players) > 0:
            if self.pipes_down.sprites()[0].rect.x == self.players[0].rect.x:
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

        myfont = pygame.font.SysFont("monospace", 40)

        # render text
        label_score = myfont.render("Score: " + str(int(self.score)), True, (0, 0, 0))
        self.display_surf.blit(label_score, (500, 0))

        label_pop = myfont.render("Population: " + str(len(self.players)), True, (0, 0, 0))
        self.display_surf.blit(label_pop, (500, 50))

        label_gen = myfont.render("Generation: " + str(self.pop.generation), True, (0, 0, 0))
        self.display_surf.blit(label_gen, (500, 100))

        # moving pipes
        if self.timer <= 0:
            x_top, x_bottom = 880, 880
            y_bottom = random.randint(-400, -100)
            y_top = y_bottom + self.pipe_gap + 560
            self.pipes_up.add(Pipe(x_top, y_top, 'pipe_up.png'))
            self.pipes_down.add(Pipe(x_bottom, y_bottom, 'pipe_dwn.png'))
            self.timer = random.randint(140, 200)
        self.timer -= 1

        for player in self.players:
            player.animate(self.display_surf)
            pygame.draw.line(self.display_surf,
                             start_pos=(player.rect.x + player.img_sprites[0].get_width()/2,
                                        player.rect.y + player.img_sprites[0].get_height()/2),
                             end_pos=(self.pipes_down.sprites()[0].rect.x,
                                      self.pipes_down.sprites()[0].rect.y
                                      + self.pipes_down.sprites()[0].image.get_height() + self.pipe_gap),
                             color=(255, 160, 122), width=1)

            pygame.draw.line(self.display_surf,
                             start_pos=(player.rect.x + player.img_sprites[0].get_width()/2,
                                        player.rect.y + player.img_sprites[0].get_height()/2),
                             end_pos=(self.pipes_up.sprites()[0].rect.x, self.pipes_up.sprites()[0].rect.y
                                      - self.pipes_up.sprites()[0].image.get_height()/3.73),
                             color=(240, 248, 255), width=1)

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()


    def run(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config.txt')
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat. DefaultStagnation,
                                    config_path)
        self.pop = neat.Population(config)
        self.pop.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.pop.add_reporter(stats)

        winner = self.pop.run(self.on_execute, 50)

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
