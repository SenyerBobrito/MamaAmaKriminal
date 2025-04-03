from pygame import *
from random import randint
from time import time as tm

window = display.set_mode((700,500))
display.set_caption("Шутер")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()


        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    
    
    def fire (self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.centery, 5)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        if self.rect.y < 0:
            self.kill()
        else:
            self.rect.y -= self.speed


class Enemy(GameSprite):
    def update(self):
        if self.rect.y + self.speed > 500:
            self.rect.y = 10
            self.rect.x = randint(10, 600)
            self.speed = randint(2, 5)
        else:
            self.rect.y += self.speed
        

font.init()
font_reload = font.Font(None, 25)
font1 = font.Font(None, 33)
reload_text = font_reload.render("ПЕРЕЗАРЯДКА", True, (255, 0, 0))



list_enemy_sprite = ["ufo.png"]
counter = 0


background = transform.scale(image.load("galaxy.jpg"), (700,500))
window.blit(background, (0,0))
player = Player("rocket.png", 300, 400, 15)
mixer.init()

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", randint(10, 600), 300, 10)
    enemies.add(enemy)

bullets = sprite.Group()

mixer.music.load("space.ogg")
mixer.music.play(-1)


clock = time.Clock()
FPS = 60 

round_end = False
game_is_run = True
isReload = False
fire_num = 0
reload_start_time = None
while game_is_run:
    text_counter = font1.render("Килы:"+str(counter), True, (10, 10, 123))
    
    clock.tick(FPS)
    if round_end == False:
        window.blit(background, (0,0))
        window.blit(text_counter, (10,10))                      
        player.update()
        player.reset()                                          
        enemies.update()                                        
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)
        for e in event.get():
            if e.type == QUIT:
                game_is_run = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if fire_num == 5:    
                        time_now = tm()
                        if time_now - reload_start_time > 2:
                            fire_num = 0
                        else:
                            window.blit(reload_text, (player.rect.centerx, player.rect.centery))
                    else:
                        fire_num += 1
                        if fire_num == 5:
                            reload_start_time = tm()
                        player.fire()
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for i in range(len(collides)):
            enemy = Enemy("ufo.png", randint(10, 600), 10, randint(1, 5))
            enemies.add(enemy)
            counter += 1
            if (counter > 10):
                round_end = True

    else:
        for e in event.get():
            if e.type == QUIT:
                game_is_run = False
        if counter > 10:
           text_win = font1.render("Вы победили!", True, (0, 255, 0))
           window.blit(text_win, (250, 200))
    

    display.update()

