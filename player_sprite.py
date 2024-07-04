import pygame as pg
import os
from bullet_sprite import Bullet

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
ship = pg.image.load(os.path.join(img_folder, 'ship_J.png'))
flying_ship = pg.image.load(os.path.join(img_folder, 'ship_J_fly.png'))


class Player(pg.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        pg.sprite.Sprite.__init__(self)
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.image_old = ship
        self.image = self.image_old.copy()
        self.rect = self.image_old.get_rect()
        self.radius = int(self.rect.width / 4)
        self.rect.center = (self.WIDTH / 2, self.HEIGHT / 3 * 2)
        self.speed = 0
        self.health = 100
        self.rot = 0  # angle 360
        self.rot_speed = 0
        self.angle = 90  # angle +- 0.5

    def update(self):
        self.speed = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_w]:
            self.image_old = flying_ship
            self.speed = -2
            self.rect.y += self.speed
        elif keystate[pg.K_s]:
            self.image_old = flying_ship
            self.speed = 2
            self.rect.y += self.speed
        elif keystate[pg.K_a]:
            self.image_old = flying_ship
            self.speed = -2
            self.rect.x += self.speed
        elif keystate[pg.K_d]:
            self.image_old = flying_ship
            self.speed = 2
            self.rect.x += self.speed
        elif keystate[pg.K_q]:
            self.image_old = flying_ship
            self.rot_speed = 2
            self.angle += 2
            self.rotate()
        elif keystate[pg.K_e]:
            self.image_old = flying_ship
            self.rot_speed = -2
            self.angle -= 2
            self.rotate()
        else:
            self.image_old = ship
        if self.rect.right > self.WIDTH:
            self.rect.right = self.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def forward(self):
        # self.rect.x = math.cos(self.rot) * self.speed + WIDTH / 2
        # self.rect.y = math.sin(self.rot) * self.speed + HEIGHT / 2
        pass

    def rotate(self):
        self.rot = (self.rot + self.rot_speed) % 360
        new_image = pg.transform.rotate(self.image_old, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.angle)
        return bullet
