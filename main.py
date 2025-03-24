import pygame
import random
from pygame import mixer

from pygame.examples.aliens import load_image

WIDTH = 1200
HEIGHT = 960
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE= (255,162,0)
NEON_GREEN = (11, 255, 1)
NEON_PURPLE = (254, 0, 246)
NEON_YELLOW = (253, 254, 1)
NEON_BLUE = (1, 30, 254)
NEON_PINK = (255, 110, 199)

font_name = pygame.font.match_font('arial')
def draw(surf, text,size,x,y,color):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 50 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_shield_bar(surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if pct>70:
            color=GREEN
        elif pct>30:
            color=NEON_YELLOW
        else:
            color=RED
        pygame.draw.rect(surf, color, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

def newmob():
    rock = Mob()
    all_sprites.add(rock)
    mobs.add(rock)

class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        #size
        self.width = 45
        self.height = 45
        #shape
        self.type = random.choice(['health', 'gun'])

            # self.image.fill(BLUE)
        # self.image = pygame.Surface((self.width,self.height))
        self.image = pygame.image.load("HealthPickup.png")
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        # self.image.fill(ORANGE)
        if self.type == 'gun':
            self.image = pygame.image.load("new_bullet.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        #self.image = pygame.image.load("Ammo000.png")
        #self.image = pygame.transform.scale(self.image,(self.width,self.height ))
        #rectangle
        self.rect = self.image.get_rect()
        #location on screen
        self.rect.center = center
        #set up move
        self.speedy = 5
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top>HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #size
        self.width = 20
        self.height = 40
        #shape
        #self.image = pygame.Surface((self.width,self.height))
        #self.image.fill(ORANGE)
        self.image = pygame.image.load("Ammo000.png")
        self.image = pygame.transform.scale(self.image,(self.width,self.height ))
        #rectangle
        self.rect = self.image.get_rect()
        #location on screen
        self.rect.centerx = x
        self.rect.bottom = y

        #set up move
        self.speedx = 0
        self.speedy = 10
    def update(self):

        self.rect.y -= self.speedy
        #self.rect.y += self.speedy
class Bullet2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #size
        self.width = 20
        self.height = 40
        #shape
        #self.image = pygame.Surface((self.width,self.height))
        #self.image.fill(ORANGE)
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image,(self.width,self.height ))
        #rectangle
        self.rect = self.image.get_rect()
        #location on screen
        self.rect.centerx = x
        self.rect.top= y

        #set up move
        self.speedx = 0
        self.speedy = -10
    def update(self):

        self.rect.y -= self.speedy
        #self.rect.y += self.speedy

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #size
        self.width = 70
        self.height = 100
        self.health = 30
        self.score = 0
        self.lives = 3
        self.mob_count=0
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        #shape
        # self.image = pygame.Surface((self.width,self.height))
        # self.image.fill(BLUE)
        self.image = pygame.image.load("Biomech Dragon Cannon.png")
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.mini_img = pygame.transform.scale(self.image, (40,60))
        #rectangle
        self.rect = self.image.get_rect()
        #location on screen
        self.rect.bottom = HEIGHT
        self.rect.centerx = WIDTH//2
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 200
       #set up move
        self.speedx = 0
        self.speedy = 3
        self.last_time = pygame.time.get_ticks()
    def shoot(self):
        pygame.mixer.Sound.play(crash_sound)
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power==1:

                b = Bullet(self.rect.centerx,self.rect.top)
                bullets.add(b)
                all_sprites.add(b)
            if self.power>=2:
                b1 = Bullet(self.rect.left, self.rect.top)
                b2 = Bullet(self.rect.right, self.rect.top)
                bullets.add(b1)
                all_sprites.add(b1)
                bullets.add(b2)
                all_sprites.add(b2)

    def update(self):
        if self.power>=2 and pygame.time.get_ticks()-self.power_time>5000:
            self.power -=1
            self.power_time=pygame.time.get_ticks()
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx = 20
        if keystate[pygame.K_LEFT]:
            self.speedx = -20
        if self.rect.right >= WIDTH:
           self.rect.right = WIDTH
        if self.rect.left <= 0:
           self.rect.left = 0
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        #self.rect.y += self.speedy

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #size
        self.width = 300
        self.height = 300
        self.health = 200
        self.score = 0
        self.lives = 3
        self.mob_count=0
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        #shape
        self.image = pygame.Surface((self.width,self.height))
        # self.image.fill(BLUE)
        self.image_orig = pygame.image.load("tribasepart1.png")

        self.image_orig = pygame.transform.scale(self.image_orig, (self.width,self.height))
        self.image = self.image_orig
        #rectangle
        self.rect = self.image.get_rect()
        #location on screen
        self.rect.bottom = -100
        self.rect.centerx = WIDTH//2
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 500
       #set up move
        self.speedx = 0
        self.speedy = 3
        self.enter = False
        self.shooting=False
        self.rot=0
        self.rot_speed=10
        self.move = True
        self.last_update = pygame.time.get_ticks()
        self.last_time = pygame.time.get_ticks()
    def shoot(self):
        pygame.mixer.Sound.play(crash_sound)

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now

            if self.health>70:
                b2 = Bullet2(self.rect.centerx,self.rect.bottom)
                bullets2.add(b2)
                all_sprites.add(b2)

            elif self.health>30:
                b2 = Bullet2(self.rect.centerx, self.rect.bottom)
                bullets2.add(b2)
                all_sprites.add(b2)
                b3 = Bullet2(self.rect.left, self.rect.bottom)
                b4 = Bullet2(self.rect.right, self.rect.bottom)
                bullets2.add(b3)
                all_sprites.add(b3)
                bullets2.add(b4)
                all_sprites.add(b4)
            else:
                b2 = Bullet2(self.rect.centerx, self.rect.bottom)
                bullets2.add(b2)
                all_sprites.add(b2)
                b3 = Bullet2(self.rect.left, self.rect.bottom)
                b4 = Bullet2(self.rect.right, self.rect.bottom)
                bullets2.add(b3)
                all_sprites.add(b3)
                bullets2.add(b4)
                all_sprites.add(b4)
                b5 = Bullet2(self.rect.left+50, self.rect.bottom)
                b6 = Bullet2(self.rect.right-50, self.rect.bottom)
                bullets2.add(b5)
                all_sprites.add(b5)
                bullets2.add(b6)
                all_sprites.add(b6)


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.y >= 50 and self.move == True:
            self.move = False
            self.speedy = 0
            self.speedx = 5

        if self.move == False:
            # self.rotate()

            if self.rect.centerx > WIDTH - 20:
                self.speedx *= -1
            if self.rect.centerx < 20:
                self.speedx *= -1
            self.shoot()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.width = 40
        self.height = 40
        # Need shooting
        self.expl_anim = {}
        self.expl_anim['sm'] = []
        self.expl_anim['lg'] = []
        self.expl_anim['xl'] = []
        self.load_image()
        self.image = pygame.Surface((self.width, self.height))
        # self.image.fill(BLUE)
        # self.player_img = pygame.image.load('club2.PNG')
        # self.player_img =pygame.transform.scale(self.player_img,(self.width,self.height))
        # self.image=self.player_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.center = center
        self.frame=0
        self.frame_rate = 75
        self.last_update = pygame.time.get_ticks()

    def load_image(self):
        for i in range(1,11):
            filename = 'boom/bubble_explo{}.png'.format(i)
            img = pygame.image.load(filename)
            img_lg = pygame.transform.scale(img,(150,150))
            self.expl_anim['lg'].append(img_lg)
            img_xl = pygame.transform.scale(img, (1000, 1000))
            self.expl_anim['xl'].append(img_xl)
            img_sm = pygame.transform.scale(img, (32,32))
            self.expl_anim['sm'].append(img_sm)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
        else:
            center = self.rect.center
            self.image = self.expl_anim[self.size][self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center




class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #size
        self.width = 40
        self.height = 40
        self.meteor_list = []
        self.load_image()
        #shape
        #self.image = pygame.Surface((self.width,self.height))
        #self.image.fill(RED)
        # self.image = pygame.image.load(".idea/Meteor/meteor1.png")
        # self.image = pygame.transform.scale(self.image,(self.width,self.height))
        #rectangle

        self.pick = random.choice(self.meteor_list)
        self.image = self.pick
        self.rect = self.image.get_rect()
        #location on screen
        self.rect.x = random.randrange(0, WIDTH - self.width)
        self.rect.centery = random.randrange(-200, -100)

        #set up move
        self.speedx = 0
        self.speedy = random.randrange(5, 20)
    def load_image(self):
        for i in range(1,5):
            if i != 2:
                self.height = 80
            else:
                self.height = 50
            filename = 'androids/android{}.png'.format(i)
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img,(self.width,self.height))
            self.meteor_list.append(img)
    def update(self):
        self.speedx = 0

        if self.rect.top >= HEIGHT:
            self.rect.x = random.randrange(0,WIDTH-self.width)
            self.rect.centery = random.randrange(-200,-100)
            self.speedy = random.randrange(5, 20)
        self.rect.y += self.speedy
        #self.rect.y += self.speedy

def Bosslevel():
    screen.fill(BLACK)
    draw(screen, "BOSSLEVEL", 64, WIDTH // 2, HEIGHT//4, WHITE)
    draw(screen, "Press A to begin", 32, WIDTH // 2, 3+HEIGHT//3, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_a]:
                    waiting = False

def level_up(level):
    screen.fill(BLACK)
    draw(screen, "level"+str(level), 64, WIDTH // 2, HEIGHT//4, WHITE)
    draw(screen, "Press A to begin", 32, WIDTH // 2, 3+HEIGHT//3, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_a]:
                    waiting = False

def start_screen():
    screen.fill(BLACK)
    draw(screen, "Start Game", 64, WIDTH // 2, HEIGHT//4, WHITE)
    draw(screen, "Use arrow keys to move", 32, WIDTH // 2, HEIGHT//2, WHITE)
    draw(screen, "Press A to begin", 32, WIDTH // 2, 3+HEIGHT//3, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_a]:
                    waiting = False
def win_screen():
    screen.fill(BLACK)
    draw(screen, "Winner", 64, WIDTH // 2, HEIGHT//4, WHITE)
    draw(screen, "Use arrow keys to move", 32, WIDTH // 2, HEIGHT//2, WHITE)
    draw(screen, "Press A to begin", 32, WIDTH // 2, 3+HEIGHT//3, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_a]:
                    waiting = False
pygame.init()
pygame.mixer.init()
mixer.music.load('stigma.mp3' )
mixer.music.play()
crash_sound = pygame.mixer.Sound("laserfire02.mp3")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()
start_screen()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullets2 = pygame.sprite.Group()
powers = pygame.sprite.Group()
bosss = pygame.sprite.Group()

background_img= pygame.image.load("gloomy_up.png")
background_img=pygame.transform.scale(background_img, (WIDTH,HEIGHT))
background_rect=background_img.get_rect()
# Game loop
running = True
new_game = True
while running:
    if new_game:
        boss_dead = False
        last_time = pygame.time.get_ticks()
        new_game = False
        ship = Player()
        all_sprites.add(ship)

        for i in range(12):
            newmob()
        end_level=False
        mob_count = 0
        level=4
        lev = 1
        boss_level=False

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    hit_by_boss = pygame.sprite.spritecollide(ship,bullets2,True)
    if hit_by_boss:
        for hit in hit_by_boss:
            ship.health -= random.randrange(5,10)

    hit_mobs = pygame.sprite.groupcollide(bullets,mobs,True,True)
    if hit_mobs:
        for hit in hit_mobs:
            if random.random()>.8:
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                powers.add(pow)
        ship.score += 2
        newmob()
        mob_count+=1
        # player score
    hit_player = pygame.sprite.spritecollide(ship,mobs,True)
    if hit_player:
        ship.health -= random.randrange(1,8)
        newmob()
        for hit in hit_mobs:
            if random.random()>.1:
                pow=Power(hit.rect.center)
                all_sprites.add(pow)
                powers.add(pow)
        #player damage
    hit_power =pygame.sprite.spritecollide(ship,powers,True)
    for hit in hit_power:
        if hit.type=='health':
            ship.health+=random.randrange(10,30)
            if ship.health>=100:
                ship.health=100
        if hit.type=="gun":
            ship.power+=1
            # hit_player = pygame.sprite.spritecollide(ship,mobs,True)

    if ship.health <= 0:
        ship.health = 30
        ship.lives -= 1
    if ship.lives <= 0:
        running = False
    if mob_count ==25:
        mob_count=0
        level += 1
        level_up(level)

        end_level = True
    if end_level:
        end_level=False
        for m in mobs:
            m.kill()
        for p in powers:
            p.kill()
        for b in bullets:
            b.kill()
        if level==2:
            lev = 14
        if level==3:
            lev = 16
        if level==4:
            lev = 18
        if level==5:
            lev = 0
            boss_level = True
            b = Boss()
            all_sprites.add(b)
            bosss.add(b)
            b.enter=True

        for i in range(lev):
            newmob()
    if boss_level:

        # hit_boss = pygame.sprite.groupcollide(bosss, bullets, False, True)
        # if hit_boss:
        #     for bo in hit_boss:
        #         bo.health -= random.randrange(2,6)
        hit_boss = pygame.sprite.spritecollide(b,bullets,True)
        if hit_boss:
            b.health-= random.randrange(2,6)
        if b.health <=0:
            expl=Explosion(b.rect.center,'xl')
            all_sprites.add(expl)
            b.kill()
            boss_level=False
            ship.last_time = pygame.time.get_ticks()
            boss_dead = True
    if boss_dead:
        now = pygame.time.get_ticks()
        if now - ship.last_time > 3000:
            last_time = now
            win_screen()
            boss_dead = False


    # Update
    all_sprites.update()

    # Draw / render
    #screen.fill(ORANGE)
    screen.blit(background_img,background_rect)
    all_sprites.draw(screen)
    #draw(screen, str(ship.health), 35, WIDTH // 2, 10, WHITE)
    draw(screen, str(ship.score), 35, 3*WIDTH // 4, 10, WHITE)
    #draw(screen, str(ship.lives), 35, WIDTH // 4, 10, WHITE)
    draw_shield_bar(screen, 10, 10, ship.health)
    draw_lives(screen, WIDTH - 150, 5, ship.lives, ship.mini_img)
    if boss_level:
        draw_shield_bar(screen, 10, 50, b.health//2)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()