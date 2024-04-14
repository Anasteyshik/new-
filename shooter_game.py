from pygame import *
from random import randint 
window  = display.set_mode((700,500))

background = transform.scale(image.load('galaxy.jpg'), (700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont('Arial', 36)
lose = font2.render('Вы проиграли',True, (255, 0, 0))
win = font2.render('Вы выиграли',True,(0,255,0))


class GameSprite(sprite.Sprite):
    def __init__(self, image_player, speed,x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(image_player), (width,height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def  update (self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x  -= self.speed
        elif keys_pressed[K_d] and self.rect.x < 600:
            self.rect.x  += self.speed
    def shoot(self):
        bullet = Bullet('bullet.png', 5, self.rect.centerx,self.rect.y,5, 10)
        bullets.add(bullet)
rocket= Player(image_player = 'rocket.png', speed = 10, x = 200, y=350,width= 80, height= 140)
# rocket= Player(image_player = 'rocket.png', speed = 10, x=0, y=320,width= 70, height= 150)
# ufo = Player (image_player = 'ufo.png', speed= 10, x=0, y=0)    

class Enemy(GameSprite):
    def update (self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,600)
            self.speed = randint(1,4)
class Bullet (GameSprite):
    def update (self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500

ufos= sprite.Group()
bullets= sprite.Group()
for i in range (5):
    ufo = Enemy('ufo.png', randint(1,4),randint(0,600), 0,80,50)
    ufos.add (ufo)
score = 0
lost = 0
fps= 60
game = True
clock = time.Clock()
finish = False

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                rocket.shoot()
    if not finish:    
        scoretext= font2.render('Счет: '+str(score),True,(255,255,255))
        window.blit(background, (0,0))
        losttext= font2.render('Пропущено: '+str(lost),True,(255,255,255))
        window.blit(scoretext,(30,40))
        window.blit(losttext,(30,70))

        rocket.update()
        rocket.reset()
        ufos.draw(window)
        ufos.update()
        bullets.draw(window)
        bullets.update()
        if sprite.groupcollide(ufos,bullets,True,True):
            score += 1
            ufo = Enemy('ufo.png', randint(1,4),randint(0,600), 0,80,50)
            ufos.add (ufo)

    display.update()
    clock.tick(fps)