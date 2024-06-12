from random import randint
from time import time as get_time
from pygame import *
SCREEN_SIZE = (1200, 800)
SPRITE_SIZE = 60

def show_text(text, x, y, text_color=(255, 255, 255), text_size=40, font_name='Verdana'):
        f = font.SysFont(font_name, text_size)
        image = f.render(text, True, text_color)
        window.blit(image, (x, y))


class GameSprite(sprite.Sprite):
    def __init__ (self, image_name, x, y, speed, image_scale=1):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (SPRITE_SIZE // image_scale, SPRITE_SIZE // image_scale))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

font.init()
class Counter:
    def __init__(self, x, y, text):
        self.pos = (x, y)
        self.text = text
        self.count = 0
    
    def render_text(self, text_color=(255, 255, 255), text_size=40, font_name='Verdana'):
        f = font.SysFont(font_name, text_size)
        self.image = f.render(self.text + str(self.count), True, text_color)

    def reset(self):
        window.blit(self.image, self.pos)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)

class Enemy(GameSprite):
    def __init__(self, image_name, x, y, speed):
        if speed > 1:
            super().__init__(image_name, x, y, speed, 2)
        else:
            super().__init__(image_name, x, y, speed)
        self.set_hp()

    def set_hp(self):
        if self.speed == 3 or self.speed == 2:
            self.hp = 1
        else:
            self.hp = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
            missed_counter.count += 1
            missed_counter.render_text()

class Bullet(GameSprite):
    def __init__(self, image_name, x, y, speed, direction=0):
        super().__init__(image_name, x, y, speed)
        self.direction = direction

    def update(self):
        self.rect.y -= self.speed
        if self.direction == 1:
            self.rect.x -= self.speed
        elif self.direction == 2:
            self.rect.x += self.speed

class Player(GameSprite):
    def __init__(self, image_name, x, y, speed, lives=3, image_live='HP.png'):
        super().__init__(image_name, x, y, speed)
        self.last_shoot_time = 0
        self.last_shoot_time_for_new_weapon = 0
        self.lives = lives
        self.image_live = transform.scale(image.load(image_live), (SPRITE_SIZE, SPRITE_SIZE))

    def draw_lives(self):
        for i in range(self.lives):
            window.blit(self.image_live, (SCREEN_SIZE[0]-i*70 - 80, 20))

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < SCREEN_SIZE[0] - SPRITE_SIZE:
            self.rect.x += self.speed
        if keys_pressed[K_q]:
            if get_time() - self.last_shoot_time_for_new_weapon > .8:
                self.new_weapon_shoot()
                self.last_shoot_time_for_new_weapon = get_time()
        if keys_pressed[K_SPACE]:
            if get_time() - self.last_shoot_time > .4:
                self.shoot()
                self.last_shoot_time = get_time()
        self.reset()
    def new_weapon_shoot(self):
        s = mixer.Sound('fire.ogg')
        s.set_volume(0.02)
        s.play()
        for i in range(3):
            new_billet = Bullet('bullet.png', self.rect.x, self.rect.y, 15, i)
            new_billet.image = transform.scale(new_billet.image, (SPRITE_SIZE // 4, SPRITE_SIZE // 4))
            new_billet.rect = new_billet.image.get_rect()
            new_billet.rect.x = self.rect.centerx - 8
            new_billet.rect.y = self.rect.y
            bullets.add(new_billet)

    def shoot(self):
        new_billet = Bullet('bullet.png', self.rect.x, self.rect.y, 15)
        new_billet.image = transform.scale(new_billet.image, (SPRITE_SIZE // 4, SPRITE_SIZE // 4))
        new_billet.rect = new_billet.image.get_rect()
        new_billet.rect.x = self.rect.centerx - 8
        new_billet.rect.y = self.rect.y
        bullets.add(new_billet)
        s = mixer.Sound('fire.ogg')
        s.set_volume(0.02)
        s.play()
        
missed_counter = Counter(10, 10, 'Количество пропущенных:')
missed_counter.render_text()

killed_counter = Counter(10, 50, 'Количество уничтоженных:')
killed_counter.render_text()

bullets = sprite.Group()

asteroid = sprite.Group()

enemies = sprite.Group()
for i in range(10):
    new_enemy = Enemy('ufo.png', randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, randint(1,3))
    enemies.add(new_enemy)

asteroid.add(Asteroid('asteroid.png', randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, 1))
asteroid.add(Asteroid('asteroid.png', randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, 1))

player = Player('rocket.png',SCREEN_SIZE[0]/2, SCREEN_SIZE[-1]- SPRITE_SIZE, 20)       

window = display.set_mode(SCREEN_SIZE)
display.set_caption('Shooter')
background = transform.scale(
        image.load('galaxy.jpg'),
        SCREEN_SIZE
)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.4)
mixer.music.play()            
game = True
clock = time.Clock()
FPS = 60
finish = False
while game:
    clock.tick(FPS)
    if finish == False:

        window.blit(background, (0,0))
        player.update()
        bullets.update()
        bullets.draw(window)
        enemies.update()
        enemies.draw(window)
        asteroid.update()
        asteroid.draw(window)
        missed_counter.reset()
        killed_counter.reset()

        # show_text(str(player.lives), SCREEN_SIZE[0]-40, 10)

        monsters_list = sprite.groupcollide(enemies, bullets, False, True)
        for m in monsters_list:
            m.hp -= 1
            if m.hp <= 0:
                m.set_hp()
                m.rect.y = 0
                m.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
                killed_counter.count += 1
                killed_counter.render_text()

        for m in sprite.spritecollide(player, enemies, False) + sprite.spritecollide(player, asteroid, False):
            m.rect.y = 0
            m.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
            player.lives -= 1
            

        if missed_counter.count >= 10:
            player.lives -= 1
            missed_counter.count = 0 
        
        if player.lives <= 0:    
            show_text('Поражение', SCREEN_SIZE[0]//2 - 50, SCREEN_SIZE[1]//2 - 50)
            mixer.music.stop()
            finish = True
            
        if killed_counter.count >= 15:
            show_text('Победа', SCREEN_SIZE[0]//2 - 50, SCREEN_SIZE[1]//2 - 50)
            mixer.music.stop()
            finish = True
        
        
        player.draw_lives()
        display.update()
    for e in event.get():
        if e.type == QUIT:
            game = False