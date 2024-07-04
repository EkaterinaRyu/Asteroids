import random
import pygame as pg
from player_sprite import Player
from asteroid_sprite import Asteroid
from explosion_animation import Explosion
from background_sprite import Star

WIDTH = 480
HEIGHT = 600
FPS = 60
BACK = (24, 24, 32)
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("asteroids")
clock = pg.time.Clock()

# группа для всех спрайтов
all_sprites = pg.sprite.Group()

# группа для звездочек на фоне
stars = pg.sprite.Group()


# условно рандомная генерация звездочек
def new_star():
    for i in range(random.randint(0, 7)):
        if random.randrange(0, 100) < 1:
            s = Star(WIDTH, HEIGHT)
            all_sprites.add(s)
            stars.add(s)


player = Player(WIDTH, HEIGHT)
all_sprites.add(player)


# генерация новый астероидов
def new_asteroid(n):
    for i in range(n):
        a = Asteroid(WIDTH, HEIGHT)
        all_sprites.add(a)
        asteroids.add(a)


asteroids = pg.sprite.Group()
new_asteroid(10)

bullets = pg.sprite.Group()
score = 0


# вывод текста
def print_text(surf, text, x, y):
    font = pg.font.Font("Montserrat-VariableFont_wght.ttf", 30)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# вывод полоски здоровья
def health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    length = 100
    height = 10
    fill = (pct / 100) * length
    outline_rect = pg.Rect(x, y, length, height)
    fill_rect = pg.Rect(x, y, fill, height)
    pg.draw.rect(surf, (15, 255, 80), fill_rect)
    pg.draw.rect(surf, (255, 255, 255), outline_rect, 2)


# кнопка запуска игры
def button(scrn, text):
    scrn.fill(BACK)
    font = pg.font.Font("Montserrat-VariableFont_wght.ttf", 50)
    text_render = font.render(text, True, BACK)
    x, y, w, h = text_render.get_rect()
    x_center, y_center = WIDTH / 2, HEIGHT - 100
    x, y = x_center - w / 2, y_center - h / 2
    pg.draw.line(scrn, (150, 150, 150), (x, y), (x + w, y), 5)
    pg.draw.line(scrn, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pg.draw.line(scrn, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pg.draw.line(scrn, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pg.draw.rect(scrn, (255, 255, 255), (x, y, w, h))
    return scrn.blit(text_render, (x, y))


# начальный экран
def start_screen(text):
    new_surf = pg.Surface((WIDTH, HEIGHT))
    butt = button(new_surf, text)  # создаем кнопку на новой плоскости
    screen.blit(new_surf, (0, 0))
    print_text(screen, "asteroids", WIDTH / 2, HEIGHT / 4)
    print_text(screen, "WSAD move, QE rotate", WIDTH / 2, HEIGHT / 2)
    print_text(screen, "Space fire", WIDTH / 2, HEIGHT / 2 + 50)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for klic in pg.event.get():
            if klic.type == pg.QUIT:
                pg.quit()
            if klic.type == pg.MOUSEBUTTONDOWN:  # отслеживаем нажание на кнопку
                if butt.collidepoint(pg.mouse.get_pos()):
                    waiting = False


# перезапуск
def restart():
    global all_sprites, asteroids, bullets, player, score # сбрасываем спрайты
    start_screen('Restart?')  # вывод экрана перезапуска
    all_sprites = pg.sprite.Group()
    asteroids = pg.sprite.Group()
    bullets = pg.sprite.Group()
    player = Player(WIDTH, HEIGHT)
    all_sprites.add(player)
    new_asteroid(10)
    score = 0


start_screen('Play!')

game_over = False
running = True
while running:
    clock.tick(FPS)
    if game_over:
        game_over = False
        restart()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:  # отслеживаем стрельбу
                all_sprites.add(player.shoot())
                bullets.add(player.shoot())

    # обновление спрайтов
    all_sprites.update()

    hits = pg.sprite.groupcollide(asteroids, bullets, True, True)  # обработка попаданий лазера
    for hit in hits:
        score += 1
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        new_asteroid(1)

    collisions = pg.sprite.spritecollide(player, asteroids, True, pg.sprite.collide_circle)  # обработка столкновения
    for collision in collisions:
        player.health -= 10
        expl = Explosion(collision.rect.center, 'sm')  # вызов анимации взрыва
        all_sprites.add(expl)
        new_asteroid(1)
        if player.health <= 0:
            game_over = True

    screen.fill(BACK)
    new_star()
    all_sprites.draw(screen)
    print_text(screen, str(score), WIDTH / 2, 10)
    health(screen, 5, 5, player.health)
    pg.display.flip()

pg.quit()
