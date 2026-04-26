import sys

import pygame as pg

from Game import Game
from settings import *


class App:
    def __init__(self):
        # screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Alquerque")

        # clock
        self.clock = pg.time.Clock()

        # game
        self.game = Game(self.screen)

    def run(self):
        # main loop
        while True:
            # event loop
            for event in pg.event.get():
                # exit
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            # delete previous frame
            self.screen.fill(WHITE)

            self.game.run()

            # update display and limit frame rate
            pg.display.flip()
            self.clock.tick(TICTAC)
