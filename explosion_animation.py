import pygame as pg
from os import path


game_folder = path.dirname(__file__)
img_dir = path.join(game_folder, 'exp_anim')
explosion_anim = {'lg': [], 'sm': []}
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename))
    img_lg = pg.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
