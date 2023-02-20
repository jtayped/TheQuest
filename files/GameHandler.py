import pygame
from .misc.settings import *
from .screens.Game import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()

        self.defaultFont = pygame.font.SysFont("arial", 40)
    
    def run(self):
        level = Level(self.screen, self.clock)
        level.run()

        pygame.quit()