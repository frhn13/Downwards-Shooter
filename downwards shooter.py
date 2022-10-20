import pygame as py
import random
import os
py.init()
py.font.init()
width,height=1600,900
win=py.display.set_mode((width,height))
py.display.set_caption("Downwards Shooter")

#images and sound
bg=py.transform.scale(py.image.load(os.path.join("img","space.png")),(width,height)).convert()
playerImg=py.transform.scale(py.image.load(os.path.join("img","player.png")),(75,60)).convert()
blueLaser=py.image.load(os.path.join("img","laserBlue.png")).convert()
enemyImg=py.transform.scale(py.image.load(os.path.join("img","enemy.png")),(75,60)).convert()
redLaser=py.image.load(os.path.join("img","laserRed.png")).convert()
laserBeamImg=py.image.load(os.path.join("img","laserBeam.png")).convert()
laserWarningImg=py.image.load(os.path.join("img","warning2.png")).convert()
strongerLaser=py.image.load(os.path.join("img","laserGreen.png")).convert()
healthSign=py.image.load(os.path.join("img","healthSign.png")).convert()
strongerEnemyImg=py.image.load(os.path.join("img","strong enemy.png")).convert()
strongerLaser2=py.image.load(os.path.join("img","powLaserRed.png")).convert()
missile=py.image.load(os.path.join("img","missile.jpg")).convert()

powerupImg={}
powerupImg["health"]=py.transform.scale(py.image.load(os.path.join("img","healthPickup.png")),(50,50)).convert()


#classes and objects
class Player(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image=playerImg
        self.rect=self.image.get_rect()
        self.rect.center=(width//2,100)
        self.speedY=3
        self.speedX=10
        self.health=100
        self.maxHealth=100
        self.image.set_colorkey((0,0,0))
        self.radius=(self.rect.height//2)
        self.lastShot=py.time.get_ticks()
        self.shootDelay=400
        self.jumpCount=10
        self.jump=False

    def update(self):
        key=py.key.get_pressed()
        if self.jump==False:
            self.rect.y+=self.speedY
            self.speedY+=0.1
        if key[py.K_LEFT] and self.rect.left>10:
            self.rect.x-=self.speedX
        if key[py.K_RIGHT] and self.rect.right<width-10:
            self.rect.x+=self.speedX
        if key[py.K_z]:
            self.shoot()

    def shoot(self):
        now=py.time.get_ticks()
        if now-self.lastShot>self.shootDelay:
            self.lastShot=now
            self.jump=True
            laser=Laser(self.rect.centerx,self.rect.bottom)
            allSprites.add(laser)
            playerWeapons.add(laser)
            for x in range(30):
                self.rect.y-=5
                self.speedY=3
            if self.rect.y<=20:
                self.rect.y=20
            self.jump=False


class Laser(py.sprite.Sprite):
    def __init__(self,x,y):
        py.sprite.Sprite.__init__(self)
        self.image=blueLaser                                
        self.rect=self.image.get_rect()
        self.speed=10
        self.rect.center=(x,y)
        self.image.set_colorkey((0,0,0))

    def update(self):
        self.rect.y+=self.speed
        if self.rect.top>=height:
            self.kill()


class Platform(py.sprite.Sprite):
    def __init__(self):
        py.Sprite.sprite.__init__(self)
        self.image=platform
        self.rect=self.image.get_rect()


class Enemy(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image=enemyImg
        self.rect=self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.speedX=random.choice([-2,2,0])
        self.rect.x=random.randint(0,width)
        self.rect.y=random.randint(height,height+500)
        self.radius=(self.rect.height//2)
        self.speedY=7

    def update(self):
        self.rect.y-=self.speedY
        self.rect.x+=self.speedX
        if self.rect.bottom<=0:
            self.kill()
        if random.random()>0.995:
            self.shoot()

    def shoot(self):
        elaser=enemyLaser(self.rect.centerx,self.rect.bottom)
        allSprites.add(elaser)
        enemyWeapons.add(elaser)


class enemyLaser(py.sprite.Sprite):
    def __init__(self,x,y):
        py.sprite.Sprite.__init__(self)
        self.image=redLaser
        self.rect=self.image.get_rect()
        self.speedY=10
        self.rect.center=(x,y)
        self.image.set_colorkey((0,0,0))

    def update(self):
        self.rect.y-=self.speedY
        if self.rect.bottom<=0:
            self.kill()


class LaserWarning(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image=py.transform.scale(laserWarningImg,(100,100))
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=random.randint(0,height-150)
        self.image.set_colorkey((255,255,255))
        self.limit=1000
        self.getTime=py.time.get_ticks()

    def update(self):
        now=py.time.get_ticks()
        if now-self.getTime>self.limit:
            self.getTime=now
            self.kill()
            laserBeam=LaserBeam(self.rect.left,self.rect.centery)
            beam.add(laserBeam)
            allSprites.add(laserBeam)


class LaserBeam(py.sprite.Sprite):
    def __init__(self,x,y):
        py.sprite.Sprite.__init__(self)
        self.image=py.transform.scale(laserBeamImg,(width*2,100))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.limit=2000
        self.time=py.time.get_ticks()

    def update(self):
        now=py.time.get_ticks()
        if now-self.time>self.limit:
            self.time=now
            self.kill()


class ZapWarning(py.sprite.Sprite):
    player=Player()

    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image=py.transform.scale(laserWarningImg,(50,50))
        self.rect=self.image.get_rect()
        self.rect.x=player.rect.x
        self.rect.y=height-50
        self.limit=1000
        self.getTime=py.time.get_ticks()
        self.image.set_colorkey((255,255,255))

    def update(self):
        if self.rect.x!=player.rect.x:
            self.rect.x=player.rect.x
        now=py.time.get_ticks()
        if now-self.getTime>self.limit:
            self.getTime=now
            self.kill()
            zap=Zap(self.rect.centerx,self.rect.top)
            allSprites.add(zap)
            strongerWeapons.add(zap)


class Zap(py.sprite.Sprite):
    def __init__(self,x,y):
        py.sprite.Sprite.__init__(self)
        self.image=strongerLaser
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.image.set_colorkey((255,255,255))

    def update(self):
        self.rect.y-=30
        if self.rect.bottom<=0:
            self.kill()


class PowerUp(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.type=random.choice(["health"])
        self.image=powerupImg[self.type]
        self.rect=self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.rect.x=width
        self.rect.y=random.randint(0,height-100)

    def update(self):
        self.rect.x-=7
        if self.rect.right<=0:
              self.kill()


class StrongerEnemy(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image=strongerEnemyImg
        self.rect=self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.rect.x=random.randint(0,width-100)
        self.rect.y=random.randint(height,height+500)
        self.radius=(self.rect.height//2)
        self.speedX=random.choice([2,-2,0])
        self.speedY=10

    def update(self):
        self.rect.x+=self.speedX
        self.rect.y-=self.speedY
        if self.rect.bottom<=0:
            self.kill()
        if random.random()>0.995:
            strongerLaser1=StrongerLaser(self.rect.right,self.rect.centery)
            allSprites.add(strongerLaser1)
            enemyWeapons.add(strongerLaser1)
            strongerLaser2=StrongerLaser(self.rect.left,self.rect.centery)
            allSprites.add(strongerLaser2)
            enemyWeapons.add(strongerLaser2)


class StrongerLaser(py.sprite.Sprite):
    def __init__(self,x,y):
        py.sprite.Sprite.__init__(self)
        self.image=strongerLaser2
        self.rect=self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.rect.center=(x,y)
        self.speedY=15

    def update(self):
        self.rect.y-=self.speedY
        if self.rect.bottom<=0:
            self.kill()


class Missiles(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image=py.transform.scale(missile,(60,20))
        self.rect=self.image.get_rect()
        self.image.set_colorkey((255,255,255))
        self.rect.x=width
        self.rect.y=random.randint(0,height-20)
        self.speedX=10

    def update(self):
        self.rect.x-=self.speedX
        if self.rect.right<=0:
            self.kill()
#main
running=True
gameOver=True
clock=py.time.Clock()


def startUp():
    fps=60
    win.blit(bg,(0,0))
    titleFont=py.font.SysFont("comicsans",70)
    label=titleFont.render("Press this box to begin!",1,(0,0,0))
    py.draw.rect(win,(255,0,0),(width//2-300,height//2-25,600,100))
    win.blit(label,(width//2-275,height//2))
    wait=True
    py.display.update()
    while wait:
        mouse=py.mouse.get_pos()
        for event in py.event.get():
            if event.type==py.QUIT:
                py.quit()
            if event.type==py.MOUSEBUTTONDOWN:
                if width//2-300<mouse[0]<width//2+300 and height//2-25<mouse[1]<height//2+75:
                    wait=False


def newEnemy():
    enemy=Enemy()
    allSprites.add(enemy)
    enemies.add(enemy)


def redrawWindow(score):
    win.blit(bg,(0,bgY))
    win.blit(bg,(0,bgY2))
    allSprites.draw(win)
    py.draw.rect(win,(255,0,0),(player.rect.x,player.rect.y+playerImg.get_height()-80,playerImg.get_width(),10))
    py.draw.rect(win,(0,255,0),(player.rect.x,player.rect.y+playerImg.get_height()-80,playerImg.get_width()*(player.health/player.maxHealth),10))
    scoreFont=py.font.SysFont("comicsans",40)
    score=scoreFont.render("Score: "+str(score),1,(255,255,255))
    win.blit(score,(50,50))
    allSprites.update()
    py.display.update()


while running:
    if gameOver:
        startUp()
        gameOver=False
        fps=60
        bgY=0
        bgY2=bg.get_height()
        zap=False
        zap2=False
        stronger=False
        weaker=True
        missileActive=False
        player=Player()
        allSprites=py.sprite.Group()
        playerWeapons=py.sprite.Group()
        enemies=py.sprite.Group()
        enemyWeapons=py.sprite.Group()
        strongerWeapons=py.sprite.Group()
        beam=py.sprite.Group()
        Powerups=py.sprite.Group()
        allSprites.add(player)
        py.time.set_timer(py.USEREVENT+1,5000)
        py.time.set_timer(py.USEREVENT+2,10000)
        py.time.set_timer(py.USEREVENT+3,4000)
        py.time.set_timer(py.USEREVENT+0,20000)
        py.time.set_timer(py.USEREVENT+4,30000)
        py.time.set_timer(py.USEREVENT+5,1000)
        py.time.set_timer(py.USEREVENT+6,50000)
        score=0
        noEnemies=5
        noEnemies2=7
        for i in range(noEnemies):
            newEnemy()
    redrawWindow(score)
    for event in py.event.get():
        if event.type==py.QUIT:
            py.quit()
        if event.type==py.USEREVENT+1:
            noEnemies+=2
            if noEnemies>=15:
                noEnemies=15
            if weaker:
                for i in range(noEnemies):
                    newEnemy()
            if stronger:
                noEnemies2+=2
                if noEnemies2>=15:
                    noEnemies2=15
                for i in range(noEnemies2):
                    strongerEnemy=StrongerEnemy()
                    allSprites.add(strongerEnemy)
                    enemies.add(strongerEnemy)
        if event.type==py.USEREVENT+2:
            zap=True
        if event.type==py.USEREVENT+3 and zap==True:
            laserWarning=LaserWarning()
            allSprites.add(laserWarning)
            if zap2:
                zapWarning=ZapWarning()
                allSprites.add(zapWarning)
        if event.type==py.USEREVENT+0:
            zap2=True
        if event.type==py.USEREVENT+4:
            stronger=True
            weaker=False
            missileActive=True
        if event.type==py.USEREVENT+5 and missileActive:
            missiles=Missiles()
            allSprites.add(missiles)
            strongerWeapons.add(missiles)
    if random.random()>0.995 and zap2:
        powerup=PowerUp()
        allSprites.add(powerup)
        Powerups.add(powerup)
    if player.jump:
        bgY+=100
        bgY2+=100
    else:
        bgY-=player.speedY
        bgY2-=player.speedY
    if bgY<bg.get_height()*-1:
        bgY=bg.get_height()
    if bgY2<bg.get_height()*-1:
        bgY2=bg.get_height()
    #player x enemy weapons
    hits=py.sprite.spritecollide(player,enemyWeapons,True,py.sprite.collide_circle)
    for hit in hits:
        player.health-=10
    #player weapons x enemy weapons
    hits=py.sprite.groupcollide(enemyWeapons,playerWeapons,True,True)
    #enemy x player weapons
    hits=py.sprite.groupcollide(playerWeapons,enemies,True,True,py.sprite.collide_circle)
    for hit in hits:
        score+=1
        print(score)
    #enemy x player
    hits=py.sprite.spritecollide(player,enemies,True,py.sprite.collide_circle)
    for hit in hits:
        player.health-=10
    #player x beam
    hits=py.sprite.spritecollide(player,beam,False)
    for hit in hits:
        player.health-=1 
    #laser beam x enemy lasers
    hits=py.sprite.groupcollide(beam,enemyWeapons,False,True)
    #tracking laser x player
    hits=py.sprite.spritecollide(player,strongerWeapons,True,py.sprite.collide_circle)
    for hit in hits:
        player.health-=20
    #player x powerups
    hits=py.sprite.spritecollide(player,Powerups,True,py.sprite.collide_circle)
    for hit in hits:
        if hit.type=="health":
            player.health+=20
            if player.health>=100:
                player.health=100
    #player weapons x stronger weapons
    hits=py.sprite.groupcollide(playerWeapons,strongerWeapons,True,True)
    #player weapons x powerups
    hits=py.sprite.groupcollide(Powerups,playerWeapons,True,True)
    for hit in hits:
        if hit.type=="health":
            player.health+=20
            if player.health>=100:
                player.health=100
    if player.rect.bottom>=height or player.health<=0:
        gameOver=True
    clock.tick(fps)
