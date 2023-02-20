import pygame
from ..misc.settings import *


class Bullet:
    def __init__(self, screen, image, pos, speed) -> None:
        self.screen = screen
        self.image = image
        self.x, self.y = pos
        self.speed = speed

        self.x -= self.image.get_width()
        self.y -= self.image.get_height()

        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def onScreen(self):
        return self.x < WIDTH

    def movement(self):
        self.rect.topleft = (self.x, self.y)
        self.x += self.speed
    
    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.movement()
        self.draw()
        self.screen.blit(self.mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 0, 0, 200)), (self.rect.topleft))