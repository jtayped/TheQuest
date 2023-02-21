import pygame, time


class Magazine:
    def __init__(self, screen, nBulletsInit, bulletImage) -> None:
        self.screen = screen
        self.nBulletsInit = nBulletsInit


        self.bulletImage = pygame.transform.rotate(bulletImage, 90)

        alpha = 128
        self.bulletImageShot = self.bulletImage.copy()
        self.bulletImageShot.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

        self.bulletImageWidth = self.bulletImage.get_width()


        self.bulletsInMagazine = self.nBulletsInit
        self.spacer = 20
        self.reloading = False
    
    def noBullets(self):
        return self.bulletsInMagazine <= 0

    def drawBulletsInMagazine(self, index):
        self.screen.blit(self.bulletImage, (self.spacer+index*self.bulletImageWidth+self.spacer*index, self.spacer))
    
    def drawBulletsShot(self, index):
        self.screen.blit(self.bulletImageShot, (self.spacer+index*self.bulletImageWidth+self.spacer*index, self.spacer))

    def reload(self):
        self.reloading = True
        self.reloadBulletStartTime = time.time()

    def reloadManager(self):
        if self.reloading:
            if time.time()-self.reloadBulletStartTime > 1 and not self.bulletsInMagazine == self.nBulletsInit:
                self.bulletsInMagazine += 1
                self.reloadBulletStartTime = time.time()
            
            if self.bulletsInMagazine == self.nBulletsInit: 
                self.reloading = False

    def draw(self):
        bulletsLeft = self.nBulletsInit-self.bulletsInMagazine
        for i in range(self.nBulletsInit):
            if bulletsLeft < i+1:
                self.drawBulletsInMagazine(i)
            else:
                self.drawBulletsShot(i)

    def update(self):
        self.reloadManager()
        self.draw()
        