import pygame
import random
import sys
import os

width, height = 1000, 1000
FPS = 60
size = width, height
running = True
screen = pygame.display.set_mode(size)
moving = True
delta_x = 0
delta_y = 0
asteroids_count = 0
bonuses_count = 0
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
bullets_sprite = pygame.sprite.Group()
asteroid_sprite = pygame.sprite.Group()
bonuses_sprite = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Soplo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(all_sprites)
        self.image = load_image("soplo.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x - self.rect.w // 2
        self.rect.y = y

    def moving(self, x, y):
        self.rect.x = x - self.rect.w // 2
        self.rect.y = y


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.bonuses = 1
        self.bonusrect = True
        self.add(all_sprites)
        self.image = load_image("spaceship.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def moving(self, spaceship_delta_x, spaceship_delta_y):
        if moving and 1000 >= self.rect.x + spaceship_delta_x + self.rect.w and \
                self.rect.x + spaceship_delta_x >= 0 and \
                970 >= self.rect.y + spaceship_delta_y + self.rect.w and self.rect.y + spaceship_delta_y >= 500 and \
                spaceship_delta_y == 0 and spaceship_delta_x != 0:
            self.rect.x = self.rect.x + spaceship_delta_x
        elif moving and 1000 >= self.rect.x + spaceship_delta_x + self.rect.w \
                and self.rect.x + spaceship_delta_x >= 0 and \
                970 >= self.rect.y + spaceship_delta_y + self.rect.w and self.rect.y + spaceship_delta_y >= 500 and \
                spaceship_delta_x == 0 and spaceship_delta_y != 0:
            self.rect.y = self.rect.y + spaceship_delta_y

    def update(self):
        for i in asteroid_sprite:
            if pygame.sprite.collide_mask(self, i) and i.alive:
                self.kill()
                pygame.quit()
        for i in bonuses_sprite:
            if pygame.sprite.collide_mask(self, i) and self.bonusrect:
                self.bonuses += 1
                i.kill()

    def upd_img(self, fl):
        x = self.rect.x
        y = self.rect.y
        if fl == 0:
            self.image = load_image("spaceship.png")
        if fl == 1:
            self.image = load_image("left1.png")
        if fl == 2:
            self.image = load_image("left2.png")
        if fl == 3:
            self.image = load_image("right1.png")
        if fl == 4:
            self.image = load_image("right2.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(all_sprites)
        self.add(bullets_sprite)
        self.image = load_image("bullet.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 10
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 10, 10)
        for i in asteroid_sprite:
            if self.rect.y < -50 or self.rect.y > 1000 or (pygame.sprite.collide_mask(self, i) and i.alive == 1):
                if pygame.sprite.collide_mask(self, i) and i.alive == 1:
                    i.alive = 0
                    i.time = 1
                    if i.typ == 1:
                        i.image = load_image("collapse_sm.png")
                    elif i.typ == 2:
                        i.image = load_image("collapse_md.png")
                    else:
                        i.image = load_image("collapse.png")
                self.kill()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        self.add(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.image.fill((49, 194, 119))
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.image.fill((49, 194, 119))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, flag):
        super().__init__(all_sprites)
        self.add(asteroid_sprite)
        if flag == 1:
            self.typ = 1
            self.image = load_image("asteroid.png")
        elif flag == 2:
            self.typ = 2
            self.image = load_image("mid_asteroid.png")
        else:
            self.typ = 3
            self.image = load_image("big_asteroid.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.time = None
        alive = 1
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(10, 15)

    # движение с проверкой столкновение шара со стенками
    def update(self):
        if self.alive:
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, vertical_borders):
                    self.vx = -self.vx
            for i in bullets_sprite:
                if self.rect.y < -50 or self.rect.y > 1050 or pygame.sprite.collide_mask(self, i):
                    if pygame.sprite.collide_mask(self, i):
                        i.kill()
                    self.alive = 0
                    self.time = 1
                    if self.typ == 1:
                        self.image = load_image("collapse_sm.png")
                    elif self.typ == 2:
                        self.image = load_image("collapse_md.png")
                    else:
                        self.image = load_image("collapse.png")
                    self.mask = pygame.mask.from_surface(self.image)
        else:
            self.rect = self.rect.move(self.vx // 3, self.vy // 3)
            self.time += 1
            if self.time == 5:
                if self.typ == 1:
                    self.image = load_image("collapse_sm1.png")
                elif self.typ == 2:
                    self.image = load_image("collapse_md1.png")
                else:
                    self.image = load_image("collapse1.png")

            if self.time == 10:
                if self.typ == 1:
                    self.image = load_image("collapse_sm2.png")
                elif self.typ == 2:
                    self.image = load_image("collapse_md2.png")
                else:
                    self.image = load_image("collapse2.png")
            if self.time == 15:
                self.kill()


class Bonus(pygame.sprite.Sprite):
    def __init__(self, radius, y):
        super().__init__(all_sprites)
        self.add(bonuses_sprite)
        self.image = load_image("bonus.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = radius
        self.rect.y = y
        self.vx = random.randint(0, 5)
        self.vy = random.randrange(10, 15)

    # движение с проверкой столкновение шара со стенками
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx


Border(width - 0, 0, width - 0, height - 0)
Border(-1, -1, -1, height + 1)
soplo_fl = 0
spaceship = Spaceship(500, 800)
povorot = 0
if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    count_mov = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(spaceship.bonuses)
                if spaceship.bonuses == 1:
                    bullet = Bullet(spaceship.rect.x + 35, spaceship.rect.y)
                elif 3 > spaceship.bonuses > 1:
                    bullet = Bullet(spaceship.rect.x + 15, spaceship.rect.y)
                    bullet1 = Bullet(spaceship.rect.x + 55, spaceship.rect.y)
                elif 3 <= spaceship.bonuses:
                    bullet = Bullet(spaceship.rect.x + 15, spaceship.rect.y)
                    bullet1 = Bullet(spaceship.rect.x + 35, spaceship.rect.y)
                    bullet2 = Bullet(spaceship.rect.x + 55, spaceship.rect.y)
            if event.type == pygame.KEYDOWN:
                moving = True
                if event.key == pygame.K_d:
                    delta_x = 8
                    spaceship.upd_img(3)
                    count_mov = 1
                    povorot = 2
                if event.key == pygame.K_a:
                    delta_x = -8
                    spaceship.upd_img(1)
                    count_mov = 1
                    povorot = 1
                if event.key == pygame.K_s:
                    delta_y = 8
                if event.key == pygame.K_w:
                    delta_y = -8
                    if not soplo_fl:
                        soplo = Soplo(spaceship.rect.x + (spaceship.rect.w // 2), spaceship.rect.y + spaceship.rect.h)
                        soplo_fl = 1
                if event.key == pygame.K_a and event.key == pygame.K_d:
                    delta_x = 0
                    spaceship.upd_img(0)
                    count_mov = 0
                    povorot = 0

            if count_mov != 0:
                count_mov += 1
            if povorot == 1 and count_mov == 10:
                spaceship.upd_img(2)
            if povorot == 2 and count_mov == 10:
                spaceship.upd_img(4)
            if event.type == pygame.KEYUP and (event.key == pygame.K_a or event.key == pygame.K_d):
                delta_x = 0
                spaceship.upd_img(0)
                count_mov = 0
                povorot = 0
            if event.type == pygame.KEYUP and (event.key == pygame.K_w or event.key == pygame.K_s):
                delta_y = 0
                if povorot == 0:
                    spaceship.upd_img(0)
                if soplo_fl:
                    soplo.kill()
                    soplo_fl = 0

        fon = pygame.transform.scale(load_image('fon.png'), (width, height))
        screen.blit(fon, (0, 0))
        spaceship.moving(delta_x, 0)
        spaceship.moving(0, delta_y)
        if soplo_fl:
            soplo.moving(spaceship.rect.x + (spaceship.rect.w // 2), spaceship.rect.y + spaceship.rect.h)
        asteroids_count += 1
        bonuses_count += 1
        if asteroids_count % 2 == 0 and asteroids_count % 4 != 0 and asteroids_count % 6 != 0:
            Asteroid(random.randint(0, width), -30, 0)
        if asteroids_count % 4 == 0 and asteroids_count % 6 != 0:
            Asteroid(random.randint(0, width), -30, 1)
        if asteroids_count % 6 == 0:
            Asteroid(random.randint(0, width), -30, 2)
        if bonuses_count % 100 == 0:
            Bonus(random.randint(0, width), -30)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
