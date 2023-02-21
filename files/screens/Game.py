import pygame, sys, os, random, time
from ..misc.settings import *
from ..elements.player import Player
from ..elements.asteroid import Asteroid
from ..elements.explosion import Explosion
from ..elements.bullet import Bullet
from ..elements.magazine import Magazine


class Level:
    def __init__(self, screen, clock) -> None:
        # Init
        self.screen, self.clock = screen, clock

        # Game Loop Vars
        self.gameOver = False


        # Player
        self.playerMoveSpeed = 5
        self.playerInitPos = WIDTH//15, HEIGHT//2
        self.playerSprite = pygame.transform.scale_by(pygame.image.load(DIR_IMAGES+'players/'+random.choice(os.listdir(DIR_IMAGES+'players'))), 1.25)

        self.player = Player(self.screen, self.playerSprite, self.playerInitPos, self.playerMoveSpeed)
    

        # Asteroids
        self.asteroids = []

        self.asteroidSprites = []
        for asteroidSprite in os.listdir(DIR_IMAGES+'asteroids'):
            sprite = pygame.image.load(DIR_IMAGES+'asteroids/'+asteroidSprite)
            self.asteroidSprites.append(sprite)
        
        self.asteroidBufferScale = 1.5 # Buffer Space Multiplier for Width
        self.asteroidsOnScreen = int(5*self.asteroidBufferScale)

        self.asteroidsInit()

        self.explosionSounds = []
        for explosionSound in os.listdir(DIR_SFX+'explosions'):
            self.explosionSounds.append(pygame.mixer.Sound(DIR_SFX+'explosions/'+explosionSound))

        # Explosions
        self.explosions = []
        self.explosionSpeed = 0.3
        self.explosionSpriteList = getSpriteList(DIR_IMAGES+'explosionSpritesheet.png', 12)
    

        # Bullets
        self.bullets = []
        self.bulletSpeed = 5
        self.bulletImage = pygame.transform.scale_by(pygame.image.load(DIR_IMAGES+'bullet.png'), 0.025)

        self.shootCoolDownTimer = 0
        self.shootCoolDownTime = 0.5

        self.shootSound = pygame.mixer.Sound(DIR_SFX+'shoot.wav')

        self.reload = False
        self.magazine = Magazine(self.screen, 5, self.bulletImage)

    
    ################
    ##### Init #####
    ################

    def asteroidsInit(self):
        for i in range(self.asteroidsOnScreen):
            self.createAsteroid(init=True)


    ################
    ### Bullets ####
    ################

    def shoot(self):
        x, y = self.player.rect.right, self.player.rect.centery
        bullet = Bullet(self.screen, self.bulletImage, [x, y], self.bulletSpeed)
        self.bullets.append(bullet)

        self.magazine.bulletsInMagazine -= 1

        self.shootSound.play()

    def controls(self):
        self.shootCoolDownTimer += 1
        
        noBullets = self.magazine.noBullets()

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.shootCoolDownTimer > self.shootCoolDownTime*FPS and not noBullets and not self.magazine.reloading:
            self.shootCoolDownTimer = 0
            self.shoot()
        else:
            if self.reload and not self.magazine.reloading:
                self.magazine.reload()

    def bulletsUpdate(self):
        self.bullets = [bullet for bullet in self.bullets if bullet.onScreen()]
        for bullet in self.bullets:
            bullet.update()


    ################
    ## Asteroids ###
    ################

    def createAsteroid(self, init=False):
        sprite = random.choice(self.asteroidSprites)
        sprite = pygame.transform.rotate(pygame.transform.scale_by(sprite, random.uniform(0.5, 1.5)), random.randint(0, 360))
        spriteWidth, spriteHeight = sprite.get_width(), sprite.get_height()

        speed = random.uniform(2, 6)
        rotateSpeed = random.uniform(-0.5, 0.5)

        y = random.randint(0, HEIGHT-spriteHeight)
        if init:
            x = random.randint(WIDTH//2, WIDTH*self.asteroidBufferScale)
        else:
            x = random.randint(WIDTH, WIDTH*self.asteroidBufferScale)

        asteroid = Asteroid(self.screen, sprite, [x, y], speed, rotateSpeed)
        self.asteroids.append(asteroid)

    def asteroidCreator(self):
        if len(self.asteroids) < self.asteroidsOnScreen:
            for i in range(self.asteroidsOnScreen - len(self.asteroids)):
                self.createAsteroid()

    def asteroidUpdate(self):
        self.asteroids = [asteroid for asteroid in self.asteroids if asteroid.onScreen()]
        for asteroid in self.asteroids:
            asteroid.update()
            
            if asteroid.onScreen():
                offset = (asteroid.rect.x-self.player.rect.x, asteroid.rect.y-self.player.rect.y)
                overlap = self.player.mask.overlap(asteroid.mask, offset)

                if overlap != None:
                    self.createExplosion((overlap[0]+self.player.rect.x, overlap[1]+self.player.rect.y), self.explosionSpriteList)
                    self.asteroids.remove(asteroid)
                    self.player.lives -= 1
                
                for bullet in self.bullets:
                    offset = (asteroid.rect.x-bullet.rect.x, asteroid.rect.y-bullet.rect.y)
                    overlap = bullet.mask.overlap(asteroid.mask, offset)

                    if overlap != None:
                        self.bullets.remove(bullet)
                        self.asteroids.remove(asteroid)
                        self.createExplosion((overlap[0]+bullet.x, overlap[1]+bullet.y), self.explosionSpriteList)


    def asteroidManager(self):
        self.asteroidUpdate()
        self.asteroidCreator()

    ################
    ## Explosions ##
    ################

    def explosionUpdate(self):
        self.explosions = [explosion for explosion in self.explosions if not explosion.finished()]
        for explosion in self.explosions:
            explosion.update()
        
    def createExplosion(self, pos, spriteList):
        explosion = Explosion(self.screen, pos, spriteList, self.explosionSpeed, random.choice(self.explosionSounds))
        self.explosions.append(explosion)

    ################################
    ################################
    ################################

    def events(self):
        self.reload = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reload = True

    def update(self):
        pygame.display.set_caption(f'{round(self.clock.get_fps())}')
        self.events()
        self.screen.fill('#020018')

        #### Game Events ####

        self.controls()
        self.asteroidManager()
        self.bulletsUpdate()
        self.player.update()
        self.explosionUpdate()
        self.magazine.update()

        if self.player.lives <= 0:
            self.__init__(self.screen, self.clock)

        #####################

        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self):
        while not self.gameOver:
            self.update()