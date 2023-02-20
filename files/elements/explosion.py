import pygame


class Explosion:
    def __init__(self, screen, pos, spriteList, explosionSpeed, sfx) -> None:
        self.screen = screen
        self.x, self.y = pos
        self.spriteList = spriteList
        self.explosionSpeed = explosionSpeed
        self.sfx = sfx
        self.animationIndex = 0

        self.sprite = self.spriteList[self.animationIndex]
        self.spriteWidth, self.spriteHeight = self.sprite.get_width(), self.sprite.get_height()

        self.centerSprite()
        self.sfx.play()
    
    def finished(self):
        return self.animationIndex > len(self.spriteList)-1

    def centerSprite(self):
        self.x -= self.spriteWidth//2
        self.y -= self.spriteHeight//2

    def animation(self):
        self.animationIndex += self.explosionSpeed
        self.sprite = self.spriteList[int(self.animationIndex)]

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))

    def update(self):
        self.animation()
        self.draw()