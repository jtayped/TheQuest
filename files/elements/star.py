import pygame

class Star:
    def __init__(self, screen, pos, radius, speed, color) -> None:
        self.screen = screen
        self.x, self.y = pos
        self.radius = radius
        self.speed = speed
        self.color = color
    
    def onScreen(self):
        return self.x+self.radius*2 > 0

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
    
    def movement(self, dt):
        self.x -= self.speed*dt
    
    def update(self, dt):
        self.movement(dt)
        self.draw()
