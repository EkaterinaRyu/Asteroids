import pygame as pg
import random
import os

# загружаем картиншки в список

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

asteroids = []
pics = ['meteor_detailedLarge.png', 'meteor_detailedSmall.png', 'meteor_large.png', 'meteor_small.png',
        'meteor_squareDetailedLarge.png', 'meteor_squareDetailedSmall.png',
        'meteor_squareLarge.png', 'meteor_squareSmall.png']
for pic in pics:
    asteroids.append(pg.image.load(os.path.join(img_folder, pic)))


class Asteroid(pg.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        pg.sprite.Sprite.__init__(self)
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.image_old = random.choice(asteroids)  # рандомный выбор картинки из списка
        self.image = self.image_old.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(self.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_old, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > self.HEIGHT + 10 or self.rect.left < -25 or self.rect.right > self.WIDTH + 20:
            self.rect.x = random.randrange(self.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
