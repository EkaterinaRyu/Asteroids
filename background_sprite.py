import pygame as pg
import random
import os


game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

stars = []
pics = ['star_tiny.png', 'star_small.png', 'star_medium.png', 'star_large.png', 'star_medium.png',
        'star_small.png', 'star_tiny.png']
for pic in pics:
    stars.append(pg.image.load(os.path.join(img_folder, pic)))


class Star(pg.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        pg.sprite.Sprite.__init__(self)
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.image = stars[0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, self.WIDTH)
        self.rect.y = random.randrange(0, HEIGHT)
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(stars):
                self.kill()
            else:
                center = self.rect.center
                self.image = stars[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
