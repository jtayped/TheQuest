import pygame, math
from ..misc.settings import *

class Player:
    def __init__(self, screen, initSprite, initPos, movementSpeed) -> None:
        self.screen = screen
        self.initSprite = initSprite
        self.x, self.y = initPos
        self.movementSpeed = movementSpeed

        self.sprite = pygame.transform.rotate(self.initSprite, 90)
        self.rect = self.sprite.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.sprite)

        self.lives = 3
        self.sinN = 0

    ################
    ### Movement ###
    ################

    def controls(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.rect.y -= self.movementSpeed
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.rect.y += self.movementSpeed
        
    def borders(self):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def movement(self):
        self.controls()
        self.borders()
    



    ################
    ### Display ####
    ################

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def update(self):
        self.movement()
        self.draw()
