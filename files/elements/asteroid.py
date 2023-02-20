import pygame


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

    def rotate(self):
        self.angle += self.rotateSpeed
        self.sprite = pygame.transform.rotate(self.initSprite, self.angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)

    def movement(self):
        self.x -= self.speed
        self.rect.center = (self.x, self.y)
        self.rotate()

        self.updateMask()

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def update(self):
        self.movement()
        self.draw()