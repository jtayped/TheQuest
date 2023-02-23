import pygame

class Counter:
    def __init__(self, screen, pos, nTotalItems, nCurrentItems, itemImage, spacerX, directionRight) -> None:
        self.screen = screen
        self.x, self.y = pos
        self.nTotalItems = nTotalItems
        self.nCurrentItems = nCurrentItems
        self.itemImage = itemImage
        self.spacerX = spacerX
        self.directionRight = directionRight

        self.imageWidth = self.itemImage.get_width()

        self.transparentItemImage = self.itemImage.copy()
        self.transparentItemImage.fill((255, 255, 255, 75), None, pygame.BLEND_RGBA_MULT)
    
    def drawImage(self, transparent, pos):
        self.screen.blit(self.transparentItemImage if transparent else self.itemImage, pos)

    def draw(self):
        if self.directionRight:
            for i in range(self.nTotalItems):
                x, y = self.x + i*self.imageWidth + i*self.spacerX, self.y
                if i < self.nCurrentItems:
                    self.drawImage(False, (x, y))
                    
                else:
                    self.drawImage(True, (x, y))

        else:
            for i in range(self.nTotalItems):
                x, y = self.x+i*self.imageWidth+i*self.spacerX, self. y
                if i+1 > self.nTotalItems - self.nCurrentItems:
                    self.drawImage(False, (x, y))
                else:
                    self.drawImage(True, (x, y))

    def update(self):
        self.draw()
