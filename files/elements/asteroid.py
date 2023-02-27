import pygame
from ..misc.settings import *

class Asteroid:
    def __init__(self, screen, initSprite, pos, speed, rotateSpeed) -> None:
        self.screen = screen
        self.initSprite = initSprite
        self.x, self.y = pos
        self.speed = speed
        self.rotateSpeed = rotateSpeed
        self.angle = 0

        self.sprite = initSprite
        self.rect = self.sprite.get_rect(topleft=pos)

        self.mask = pygame.mask.from_surface(self.sprite)

    def onScreen(self):
        return self.rect.right > 0

    def updateMask(self):
        self.mask = pygame.mask.from_surface(self.sprite)

    def rotate(self, dt):
        self.angle += self.rotateSpeed*dt
        self.sprite = pygame.transform.rotate(self.initSprite, self.angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)

    def movement(self, dt):
        self.x -= self.speed*dt
        self.rect.center = (self.x, self.y)
        self.rotate(dt)

        #self.updateMask()

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def update(self, dt):
        self.movement(dt)
        self.draw()
