import pygame, math
from ..misc.settings import *

class Player:
    def __init__(self, screen, initSprite, initPos, movementSpeed, lives) -> None:
        self.screen = screen
        self.initSprite = initSprite
        self.x, self.y = initPos
        self.movementSpeed = movementSpeed
        self.lives = lives

        self.sprite = pygame.transform.rotate(self.initSprite, 90)
        self.rect = self.sprite.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.sprite)

        self.sinN = 0

    ################
    ### Movement ###
    ################

    def controls(self, dt):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.rect.y -= self.movementSpeed*dt
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.rect.y += self.movementSpeed*dt
        
    def borders(self):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def movement(self, dt):
        self.controls(dt)
        self.borders()
    



    ################
    ### Display ####
    ################

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def update(self, dt):
        self.movement(dt)
        self.draw()
