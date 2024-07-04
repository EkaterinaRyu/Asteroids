import math

import pygame as pg
import os


# импортируем картинку лазера
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
bullet = pg.image.load(os.path.join(img_folder, 'laserBlue07.png'))


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, angle):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x  # привязываем лазер к центру корабля
        self.time = 0
        self.angle = angle
        self.direction = math.radians(self.angle)

    def update(self):
        self.rect.x += math.cos(self.direction) * self.time
        self.rect.y -= math.sin(self.direction) * self.time
        self.time += 0.5
        if self.rect.bottom < 0:
            self.kill()
