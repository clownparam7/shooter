#Создай собственный Шутер!

from pygame import *
from random import randint
 
#фоновая музыка
mixer.init()
mixer.music.load('a4-kids.mp3')
mixer.music.play()
shot = mixer.Sound('fire.ogg')
 
#шрифты и надписи
font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
 
# нам нужны такие картинки:
img_back = "a4.png" # фон игры
img_hero = "kobyakov.jpeg" # герой
img_bullet = "h12.png" # пуля
img_enemy = "clowna42.jpg" # враг
 
score = 0 # сбито кораблей
lost = 0 # пропущено кораблей
count_bullets = 20
 
# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        shot.play()
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 40, 30, -15)
        bullets.add(bullet)
 
# класс спрайта-врага   
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        direction = randint(1,2)
        if direction == 1:
            self.rect.x += self.speed + randint(1,6)
        else:
            self.rect.x -= self.speed + randint(1,6)

        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
# класс спрайта-пули   
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
 
# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 20)
 
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
bullets = sprite.Group()
 
# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна
while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                count_bullets -= 1
                ship.fire()
 
    if not finish:
        # обновляем фон
        window.blit(background,(0,0))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 0, 255))
        window.blit(text_lose, (10, 50))
 
        text_bullets = font2.render('Пуль осталось:' + str(count_bullets),
                                    1, (255,0,255))
        window.blit(text_bullets,(10,90))
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for dead in sprite_list:
            score +=1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if count_bullets == 0:
            text_bullets_over = font2.render('ПУЛИ ЗАКОНЧИЛИСЬ',
                                            1, (255,0,0))
            text_bullets_over1 = font2.render('ТЫ ПОПУСК',
                                            1, (255,0,0))
            window.blit(text_bullets_over,(10,140))
            window.blit(text_bullets_over1,(100, 200))
            finish = True
        if score >=10:
            text_win = font1.render('ты попадаешь в видео!', True, (0,255,0))
            window.blit(text_win, (10,250))
            finish = True
        # производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
 
        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        if lost >=3:
            text_lost = font1.render('ты умер героем', True, (255,0,0))
            window.blit(text_lost, (win_height/2-100, win_width/2-50))
            finish = True
 
        display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)
