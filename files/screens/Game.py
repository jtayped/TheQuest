import pygame, sys, os, random, time
from ..misc.settings import *
from ..elements.player import Player
from ..elements.asteroid import Asteroid
from ..elements.explosion import Explosion
from ..elements.bullet import Bullet
from ..elements.UI.UI_counter import Counter
from ..elements.star import Star


class Level:
    def __init__(self, screen, clock) -> None:
        # Init
        self.screen, self.clock = screen, clock
        self.dt = pygame.time.get_ticks()

        # Game Loop Vars
        self.gameOver = False
        self.pixelFont = pygame.font.Font(DIR_FONTS+'pixelFont.ttf', 50)
        self.levelIncrease = False
        self.levelStartTime = time.time()


        # Player
        self.lives = PLAYER_LIVES
        self.playerSprite = pygame.transform.scale_by(pygame.image.load(DIR_IMAGES+'players/'+random.choice(os.listdir(DIR_IMAGES+'players'))), WIDTH/900)

        self.player = Player(self.screen, self.playerSprite, PLAYER_INIT_POS, PLAYER_SPEED, self.lives)
        self.nLevel = 1
    

        # Asteroids
        self.asteroids = []

        self.asteroidSprites = []
        for asteroidSprite in os.listdir(DIR_IMAGES+'asteroids'):
            sprite = pygame.image.load(DIR_IMAGES+'asteroids/'+asteroidSprite)
            self.asteroidSprites.append(sprite)
        
        self.asteroidMinimumSpeed = ASTEROID_MIN_SPEED
        self.asteroidBufferScale = 2 # Buffer Space Multiplier for Width
        self.asteroidsOnScreen = int(5*self.asteroidBufferScale)

        self.asteroidsInit()

        self.explosionSounds = []
        for explosionSound in os.listdir(DIR_SFX+'explosions'):
            self.explosionSounds.append(pygame.mixer.Sound(DIR_SFX+'explosions/'+explosionSound))

        # Explosions
        self.explosions = []
        self.explosionSpriteList = getSpriteList(DIR_IMAGES+'explosionSpritesheet.png', 12)
    

        # Bullets
        self.bullets = []
        self.bulletImage = pygame.transform.scale_by(pygame.image.load(DIR_IMAGES+'bullet.png'), 0.025)
        self.shootCoolDownTimer = time.time()
        self.bulletAcceleration = BULLET_ACCELERATION

        self.shootSound = pygame.mixer.Sound(DIR_SFX+'shoot.wav')

        self.reload = False
        self.startReloadBulletTime = 0
        self.bulletReloadSound = pygame.mixer.Sound(DIR_SFX+'bulletReload.wav')
        self.reloadStart = pygame.mixer.Sound(DIR_SFX+"reloadStart.wav")

        # UI #
        # Lives UI
        livesUISpacer, livesUIMargin = 20, 40
        livesImage = pygame.transform.scale_by(self.playerSprite, 1.25)
        livesUITotalWidth = self.lives*livesImage.get_width()+(self.lives-1)*livesUISpacer

        x, y = WIDTH-livesUITotalWidth-livesUIMargin, livesUIMargin
        self.livesUI = Counter(self.screen, [x, y], self.lives, self.lives, livesImage, livesUISpacer, False)
        ####

        # Bullets UI
        bulletsUISpacer, bulletsUIMargin = 30, 40
        x, y = bulletsUIMargin, bulletsUIMargin
        bulletsImage = pygame.transform.rotate(pygame.transform.scale_by(self.bulletImage, 1.75), 90)
        self.bulletsUI = Counter(self.screen, [x, y], N_BULLETS_IN_MAGAZINE, N_BULLETS_IN_MAGAZINE, bulletsImage, bulletsUISpacer, True)

        ####

        # Stars
        self.stars = []
        self.starsInit()

    ################
    ##### Init #####
    ################

    def starsInit(self):
        for i in range(STARS_ON_SCREEN):
            self.createStar(init=True)

    def asteroidsInit(self):
        for i in range(self.asteroidsOnScreen):
            self.createAsteroid(init=True)

    ################
    ##### Stats ####
    ################

    def writeLevel(self):
        x, y = WIDTH//2, 5
        writeText(self.screen, self.pixelFont, f'{self.nLevel}', 'white', (x, y), align='centertop')
    
    def difficultyIncrease(self):
        self.asteroidsOnScreen += ADDITIONAL_ASTEROIDS_STEP
        self.asteroidMinimumSpeed *= 1.125

    def levelManager(self):
        if time.time() - self.levelStartTime > LEVEL_STEP_TIME:
            self.levelIncrease = True
            if len(self.asteroids) == 0:
                self.nLevel += 1
                self.levelIncrease = False
                self.difficultyIncrease()
                self.levelStartTime = time.time()


    ################
    ##### Stars ####
    ################

    def createStar(self, init=False):
        radius = random.uniform(1, 3)
        speed = radius/50

        grayScale = random.randint(150, 200)
        color = (grayScale, grayScale, grayScale)

        y = random.randint(0, int(HEIGHT-radius*2))
        if init:
            x = random.randint(0, WIDTH*1.25)
        else:
            x = random.randint(WIDTH, WIDTH*1.25)

        star = Star(self.screen, [x, y], radius, speed, color)
        self.stars.append(star)
    
    def starsUpdate(self):
        self.stars = [star for star in self.stars if star.onScreen()]
        for star in self.stars:
            star.update(self.dt)
        
    def starManager(self):
        self.starsUpdate()
        if len(self.stars) < STARS_ON_SCREEN:
            for i in range(STARS_ON_SCREEN - len(self.stars)):
                self.createStar()

    ################
    ### Bullets ####
    ################

    def reloadManager(self):
        if self.reload:
            if time.time()-self.startReloadBulletTime > BULLET_RELOAD_TIME:
                self.startReloadBulletTime = time.time()
                self.bulletsUI.nCurrentItems += 1
                self.bulletReloadSound.play()

                if self.bulletsUI.nCurrentItems >= self.bulletsUI.nTotalItems:
                    self.reload = False

    def shoot(self):
        if self.bulletsUI.nCurrentItems-1 >= 0 and not self.reload:
            x, y = self.player.rect.right, self.player.rect.centery
            bullet = Bullet(self.screen, self.bulletImage, [x, y], BULLET_ACCELERATION)
            self.bullets.append(bullet)
            self.bulletsUI.nCurrentItems -= 1

            self.shootSound.play()

    def controls(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and time.time()-self.shootCoolDownTimer > BULLET_COOLDOWN:
            self.shootCoolDownTimer = time.time()
            self.shoot()

    def bulletsUpdate(self):
        self.bullets = [bullet for bullet in self.bullets if bullet.onScreen()]
        for bullet in self.bullets:
            bullet.update(self.dt)


    ################
    ## Asteroids ###
    ################

    def createAsteroid(self, init=False):
        sprite = random.choice(self.asteroidSprites)
        sprite = pygame.transform.rotate(pygame.transform.scale_by(sprite, random.uniform(WIDTH/2000, WIDTH/550)), random.randint(0, 360))
        spriteHeight = sprite.get_height()

        speed = self.asteroidMinimumSpeed + random.uniform(0, 0.2)
        rotateSpeed = random.uniform(-0.025, 0.025)

        y = random.randint(spriteHeight//2, HEIGHT-spriteHeight//2)
        if init:
            x = random.randint(WIDTH//2, WIDTH*self.asteroidBufferScale)
        else:
            x = random.randint(WIDTH, WIDTH*self.asteroidBufferScale)

        asteroid = Asteroid(self.screen, sprite, [x, y], speed, rotateSpeed)
        self.asteroids.append(asteroid)

    def asteroidCreator(self):
        if len(self.asteroids) < self.asteroidsOnScreen and not self.levelIncrease:
            for i in range(self.asteroidsOnScreen - len(self.asteroids)):
                self.createAsteroid()

    def checkPlayerAsteroidCollision(self, asteroid):
        if asteroid.rect.x < self.player.rect.right+50 and self.player.rect.colliderect(asteroid.rect):
            asteroid.updateMask()

            offset = (asteroid.rect.x-self.player.rect.x, asteroid.rect.y-self.player.rect.y)
            overlap = self.player.mask.overlap(asteroid.mask, offset)

            if overlap != None:
                return overlap
        return None
    
    def checkBulletAsteroidCollision(self, bullet, asteroid):
        if (bullet.rect.right < asteroid.rect.left or
            bullet.rect.left > asteroid.rect.right or
            bullet.rect.bottom < asteroid.rect.top or
            bullet.rect.top > asteroid.rect.bottom):
            return None
        
        if not bullet.rect.colliderect(bullet.rect):
            return None

        asteroid.updateMask()
        offset = (asteroid.rect.x-bullet.rect.x, asteroid.rect.y-bullet.rect.y)
        overlap = bullet.mask.overlap(asteroid.mask, offset)

        if overlap != None:
            self.bullets.remove(bullet)
            return overlap
        return None


    def asteroidUpdate(self):
        self.asteroids = [asteroid for asteroid in self.asteroids if asteroid.onScreen()]
        for asteroid in self.asteroids:
            asteroid.update(self.dt)
            
            playerOverlap = self.checkPlayerAsteroidCollision(asteroid)
            if playerOverlap != None:
                self.createExplosion((playerOverlap[0]+self.player.rect.x, playerOverlap[1]+self.player.rect.y), self.explosionSpriteList)
                self.asteroids.remove(asteroid)

                self.player.lives -= 1
                self.livesUI.nCurrentItems -= 1

            if asteroid.onScreen():         
                for bullet in self.bullets:       
                    bulletOverlap = self.checkBulletAsteroidCollision(bullet, asteroid)
                    if bulletOverlap != None:
                        self.asteroids.remove(asteroid)
                        self.createExplosion((bulletOverlap[0]+asteroid.x, bulletOverlap[1]+asteroid.y), self.explosionSpriteList)


    def asteroidManager(self):
        self.asteroidUpdate()
        self.asteroidCreator()

    ################
    ## Explosions ##
    ################

    def explosionUpdate(self):
        self.explosions = [explosion for explosion in self.explosions if not explosion.finished(self.dt)]
        for explosion in self.explosions:
            explosion.update()
        
    def createExplosion(self, pos, spriteList):
        explosion = Explosion(self.screen, pos, spriteList, EXPLOSION_ANIMATION_SPEED, random.choice(self.explosionSounds))
        self.explosions.append(explosion)

    ################################
    ################################
    ################################

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not self.bulletsUI.nCurrentItems == self.bulletsUI.nTotalItems:
                    self.startReloadBulletTime = time.time()
                    self.reload = not self.reload

                    if self.reload:
                        self.reloadStart.play()

    def update(self):
        #pygame.display.set_caption(f'{round(self.clock.get_fps())}')
        self.events()
        self.screen.fill('#020018')

        #### Game Events ####

        self.controls()
        self.reloadManager()
        self.levelManager()

        self.starManager()
        self.asteroidManager()
        self.bulletsUpdate()
        self.player.update(self.dt)
        self.explosionUpdate()

        self.livesUI.update()
        self.bulletsUI.update()
        self.writeLevel()

        if self.player.lives <= 0:
            self.__init__(self.screen, self.clock)

        #writeText(self.screen, self.pixelFont, f'{round(self.clock.get_fps())}', 'red', (10, HEIGHT/3))

        #####################

        pygame.display.flip()
        self.dt = self.clock.tick(FPS)

    def run(self):
        while not self.gameOver:
            self.update()