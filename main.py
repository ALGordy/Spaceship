import pygame
import random
import sys
import os

width, height = 800, 800
FPS = 35
size = width, height
running = True
screen = pygame.display.set_mode(size)
moving = True
shield = None
delta_x = 0
delta_y = 0
shield_count = 0
asteroids_count = 0
bonuses_count = 0
asteroids = 0
difficulty_game = 1
flag = 0
t = 0
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
bullets_sprite = pygame.sprite.Group()
asteroid_sprite = pygame.sprite.Group()
bonuses_sprite = pygame.sprite.Group()
buttons_sprite_menu = pygame.sprite.Group()
buttons_sprite_difficulty = pygame.sprite.Group()
buttons_sprite_pause = pygame.sprite.Group()
buttons_sprite_mode = pygame.sprite.Group()
game_over_sprite = pygame.sprite.Group()
bomb_sprite = pygame.sprite.Group()
shield_sprite = pygame.sprite.Group()
shield_image_sprite = pygame.sprite.Group()
spaceship_sprite = pygame.sprite.Group()
pygame.display.set_caption('Spaceship')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


soplo_image = load_image("soplo.png")
spaceship_image = load_image("spaceship.png")
destroy_image = load_image("destroy.png")
left1_image = load_image("left1.png")
left2_image = load_image("left2.png")
right1_image = load_image("right1.png")
right2_image = load_image("right2.png")
bullet_image = load_image("bullet.png")
collapse_sm_image = load_image("collapse_sm.png")
collapse_md_image = load_image("collapse_md.png")
collapse_image = load_image("collapse.png")
bul_left_image = load_image("bul_left.png")


class Soplo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(all_sprites)
        self.image = soplo_image
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
        self.add(spaceship_sprite)
        self.image = spaceship_image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def moving(self, spaceship_delta_x, spaceship_delta_y):
        if moving and height >= self.rect.x + spaceship_delta_x + self.rect.w and \
                self.rect.x + spaceship_delta_x >= 0 and \
                height - 30 >= self.rect.y + spaceship_delta_y + self.rect.w and self.rect.y + spaceship_delta_y >= height // 2 and \
                spaceship_delta_y == 0 and spaceship_delta_x != 0:
            self.rect.x = self.rect.x + spaceship_delta_x
        elif moving and height >= self.rect.x + spaceship_delta_x + self.rect.w \
                and self.rect.x + spaceship_delta_x >= 0 and \
                height - 30 >= self.rect.y + spaceship_delta_y + self.rect.w and self.rect.y + spaceship_delta_y >= height // 2 and \
                spaceship_delta_x == 0 and spaceship_delta_y != 0:
            self.rect.y = self.rect.y + spaceship_delta_y

    def update(self):
        global flag
        global playing
        global dying
        global asteroids
        global asteroid_sprite
        global shield_bool
        global shield
        global shield_count
        for i in asteroid_sprite:
            if pygame.sprite.collide_mask(self, i) and i.alive:
                self.image = destroy_image
                playing = False
                dying = True
                if soplo_fl:
                    soplo.kill()
        for i in bonuses_sprite:
            if pygame.sprite.collide_mask(self, i) and self.bonusrect:
                self.bonuses += 1
                i.kill()
                flag = 0
        for i in bomb_sprite:
            if pygame.sprite.collide_mask(self, i) and self.bonusrect:
                for asteroid in asteroid_sprite:
                    if height > self.rect.y > -50:
                        asteroid.alive = 0
                        asteroid.time = 1
                        asteroids += 1
                i.kill()
                flag = 0
        for i in shield_sprite:
            if pygame.sprite.collide_mask(self, i) and self.bonusrect:
                i.kill()
                if shield_count == 0:
                    shield = Shield(spaceship.rect.x, spaceship.rect.y - 15)
                    shield_count = 1
                shield_bool = True
                flag = 0

    def upd_img(self, fl):
        x = self.rect.x
        y = self.rect.y
        if fl == 0:
            self.image = spaceship_image
        if fl == 1:
            self.image = left1_image
        if fl == 2:
            self.image = left2_image
        if fl == 3:
            self.image = right1_image
        if fl == 4:
            self.image = right2_image
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
        self.image = bullet_image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global asteroids
        self.rect.y -= 10
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 10, 10)
        for i in asteroid_sprite:
            if self.rect.y < -50 or self.rect.y > height or (pygame.sprite.collide_mask(self, i) and i.alive == 1):
                if pygame.sprite.collide_mask(self, i) and i.alive == 1:
                    i.alive = 0
                    i.time = 1
                    asteroids += 1
                    if i.typ == 1:
                        i.image = collapse_sm_image
                    elif i.typ == 2:
                        i.image = collapse_md_image
                    else:
                        i.image = collapse_image
                self.kill()


class Bullet_diagonal_left(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(all_sprites)
        self.add(bullets_sprite)
        self.image = bul_left_image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global asteroids
        self.rect.y -= 10
        self.rect.x -= 3
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 10, 10)
        for i in asteroid_sprite:
            if self.rect.y < -50 or self.rect.y > height or (pygame.sprite.collide_mask(self, i) and i.alive == 1):
                if pygame.sprite.collide_mask(self, i) and i.alive == 1:
                    i.alive = 0
                    i.time = 1
                    asteroids += 1
                    if i.typ == 1:
                        i.image = collapse_sm_image
                    elif i.typ == 2:
                        i.image = collapse_md_image
                    else:
                        i.image = collapse_image
                self.kill()


class Bullet_diagonal_right(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(all_sprites)
        self.add(bullets_sprite)
        self.image = load_image("bul_right.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global asteroids
        self.rect.y -= 10
        self.rect.x += 3
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 10, 10)
        for i in asteroid_sprite:
            if self.rect.y < -50 or self.rect.y > height or (pygame.sprite.collide_mask(self, i) and i.alive == 1):
                if pygame.sprite.collide_mask(self, i) and i.alive == 1:
                    i.alive = 0
                    i.time = 1
                    asteroids += 1
                    if i.typ == 1:
                        i.image = collapse_sm_image
                    elif i.typ == 2:
                        i.image = collapse_md_image
                    else:
                        i.image = collapse_image
                self.kill()


class Buttons_pause(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(buttons_sprite_pause)
        self.image = load_image(image)
        self.add(buttons_sprite_pause)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
        self.alive = 1
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(10, 15)

    def update(self):
        global asteroids
        if self.alive:
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
            if pygame.sprite.spritecollideany(self, shield_image_sprite):
                self.alive = 0
                self.time = 1
            for i in bullets_sprite:
                if self.rect.y < -50 or self.rect.y > 1050 or pygame.sprite.collide_mask(self, i):
                    if pygame.sprite.collide_mask(self, i):
                        i.kill()
                        asteroids += 1
                    self.alive = 0
                    self.time = 1
                    if self.typ == 1:
                        self.image = collapse_sm_image
                    elif self.typ == 2:
                        self.image = collapse_md_image
                    else:
                        self.image = collapse_image
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


class Bonus_bomb(pygame.sprite.Sprite):
    def __init__(self, radius, y):
        super().__init__(all_sprites)
        self.add(bomb_sprite)
        self.image = load_image("bomb.png")
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


class Bonus_shield(pygame.sprite.Sprite):
    def __init__(self, radius, y):
        super().__init__(all_sprites)
        self.add(shield_sprite)
        self.image = load_image("shield_image.png")
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


class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(shield_image_sprite)
        self.image = load_image('shield.png')
        self.add(shield_image_sprite)
        self.add(all_sprites)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global shield_count
        if pygame.sprite.spritecollideany(self, asteroid_sprite):
            self.kill()
            shield_count = 0


class Buttons_menu(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(buttons_sprite_menu)
        self.image = load_image(image)
        self.add(buttons_sprite_menu)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Buttons_difficulty(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(buttons_sprite_difficulty)
        self.image = load_image(image)
        self.add(buttons_sprite_difficulty)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Buttons_mode(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(buttons_sprite_mode)
        self.image = load_image(image)
        self.add(buttons_sprite_mode)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Image(pygame.sprite.Sprite):
    def __init__(self, group, fl):
        super().__init__(group)
        if fl == 0:
            self.image = load_image("gameover.png")
        else:
            self.image = load_image("win.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


Border(width + 1, 0, width + 1, height + 1)
Border(-1, -1, -1, height + 1)
soplo_fl = 0
spaceship = Spaceship(395, 600)
povorot = 0
if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.flip()
    shield_bool = False
    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    count_mov = 0
    time = 0
    menu = True
    playing = False
    mode = False
    difficulty = False
    dying = False
    pause = False
    f1 = pygame.font.Font(None, 36)
    f2 = pygame.font.Font(None, 42)
    endless_survival = False
    while running:
        play = Buttons_menu('play.png', 425 * 0.8, 400 * 0.8)
        quit = Buttons_menu('quit.png', 425 * 0.8, 475 * 0.8)
        text2 = f2.render(f'Select difficulty:', True,
                          (255, 255, 255))
        text3 = f2.render(f'Select mode:', True,
                          (255, 255, 255))
        survival = Buttons_mode('survival.png', 425 * 0.8, 400 * 0.8)
        endless_survival_image = Buttons_mode('endless.png', 425 * 0.8, 475 * 0.8)
        easy = Buttons_difficulty('easy.png', 425 * 0.8, 350 * 0.8)
        medium = Buttons_difficulty('medium.png', 425 * 0.8, 425 * 0.8)
        hard = Buttons_difficulty('hard.png', 425 * 0.8, 500 * 0.8)
        cont = Buttons_pause('continue.png', 425 * 0.8, 300 * 0.8)
        retry = Buttons_pause('retry.png', 425 * 0.8, 375 * 0.8)
        menu_2 = Buttons_pause('menu.png', 425 * 0.8, 450 * 0.8)
        quit_2 = Buttons_pause('quit.png', 425 * 0.8, 525 * 0.8)
        fon = pygame.transform.scale(load_image('fon.png'), (width, height))
        fon_menu = pygame.transform.scale(load_image('fon_menu.png'), (width, height))
        bonuses = random.randrange(100, 300)
        bombs = random.randrange(100, 300)
        shields = random.randrange(100, 300)

        while menu:
            screen.blit(fon_menu, (0, 0))
            buttons_sprite_menu.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    menu = False
                    playing = False
                    difficulty = False
                    pause = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play.rect.collidepoint(event.pos):
                        mode = True
                        menu = False
                    if quit.rect.collidepoint(event.pos):
                        running = False
                        menu = False
                        playing = False
                        difficulty = False
                        pause = False
        while mode:
            screen.blit(fon_menu, (0, 0))
            screen.blit(text3, (400 * 0.8, 330 * 0.8))
            buttons_sprite_mode.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    menu = False
                    difficulty = False
                    mode = False
                    playing = False
                    pause = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if survival.rect.collidepoint(event.pos):
                        difficulty = True
                        mode = False
                        endless_survival = False
                    if endless_survival_image.rect.collidepoint(event.pos):
                        playing = True
                        endless_survival = True
                        mode = False
                        difficulty_game = 15
        while difficulty:
            screen.blit(fon_menu, (0, 0))
            buttons_sprite_difficulty.draw(screen)
            screen.blit(text2, (385 * 0.8, 300 * 0.8))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    menu = False
                    difficulty = False
                    playing = False
                    pause = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy.rect.collidepoint(event.pos):
                        playing = True
                        difficulty = False
                        difficulty_game = 9
                    if medium.rect.collidepoint(event.pos):
                        playing = True
                        difficulty = False
                        difficulty_game = 6
                    if hard.rect.collidepoint(event.pos):
                        playing = True
                        difficulty = False
                        difficulty_game = 3
        while pause:
            screen.blit(fon_menu, (0, 0))
            buttons_sprite_pause.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    menu = False
                    difficulty = False
                    playing = False
                    pause = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if cont.rect.collidepoint(event.pos):
                        pause = False
                        dying = False
                        playing = True
                        img = None
                    if retry.rect.collidepoint(event.pos):
                        pause = False
                        playing = True
                        if endless_survival:
                            difficulty_game = 15
                        screen.fill((0, 0, 0))
                        pygame.display.flip()
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
                        buttons_sprite_menu = pygame.sprite.Group()
                        buttons_sprite_difficulty = pygame.sprite.Group()
                        game_over_sprite = pygame.sprite.Group()
                        Border(width + 1, 0, width + 1, height + 1)
                        Border(-1, -1, -1, height + 1)
                        soplo_fl = 0
                        spaceship = Spaceship(395, 600)
                        povorot = 0
                        count_mov = 0
                        time = 0
                        t = 0
                        asteroids = 0
                    if menu_2.rect.collidepoint(event.pos):
                        pause = False
                        menu = True
                        screen.fill((0, 0, 0))
                        pygame.display.flip()
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
                        buttons_sprite_menu = pygame.sprite.Group()
                        buttons_sprite_difficulty = pygame.sprite.Group()
                        game_over_sprite = pygame.sprite.Group()
                        Border(width + 1, 0, width + 1, height + 1)
                        Border(-1, -1, -1, height + 1)
                        soplo_fl = 0
                        spaceship = Spaceship(395, 600)
                        povorot = 0
                        count_mov = 0
                        time = 0
                        t = 0
                        asteroids = 0
                    if quit_2.rect.collidepoint(event.pos):
                        running = False
                        menu = False
                        playing = False
                        difficulty = False
                        pause = False
        while playing:
            time += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if spaceship.bonuses == 1:
                        bullet = Bullet(spaceship.rect.x + 35, spaceship.rect.y)
                    elif 3 > spaceship.bonuses > 1:
                        bullet = Bullet(spaceship.rect.x + 15, spaceship.rect.y)
                        bullet1 = Bullet(spaceship.rect.x + 55, spaceship.rect.y)
                    elif 3 <= spaceship.bonuses:
                        bullet = Bullet_diagonal_left(spaceship.rect.x + 15, spaceship.rect.y)
                        bullet1 = Bullet(spaceship.rect.x + 35, spaceship.rect.y)
                        bullet2 = Bullet_diagonal_right(spaceship.rect.x + 55, spaceship.rect.y)
                if event.type == pygame.KEYDOWN:
                    moving = True
                    if event.key == pygame.K_ESCAPE:
                        pause = True
                        menu = False
                        mode = False
                        difficulty = False
                        playing = False
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
                            soplo = Soplo(spaceship.rect.x + (spaceship.rect.w // 2),
                                          spaceship.rect.y + spaceship.rect.h)
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
            if shield_bool:
                shield.rect.x = spaceship.rect.x
                shield.rect.y = spaceship.rect.y - 25
            screen.blit(fon, (0, 0))
            spaceship.moving(delta_x, 0)
            spaceship.moving(0, delta_y)
            if soplo_fl:
                soplo.moving(spaceship.rect.x + (spaceship.rect.w // 2), spaceship.rect.y + spaceship.rect.h)
            asteroids_count += 1
            bonuses_count += 1
            if asteroids_count % (1 * difficulty_game) == 0 and asteroids_count % (
                   2 * difficulty_game) != 0 and asteroids_count % (3 * difficulty_game) != 0:
                Asteroid(random.randint(0, width - 50), -30, 0)
            if asteroids_count % (2 * difficulty_game) == 0 and asteroids_count % (3 * difficulty_game) != 0:
                Asteroid(random.randint(0, width - 50), -30, 1)
            if asteroids_count % (3 * difficulty_game) == 0:
                Asteroid(random.randint(0, width - 50), -30, 2)
            if bonuses_count % bonuses == 0 and spaceship.bonuses != 3:
                Bonus(random.randint(0, width - 50), -30)
            if bonuses_count % bombs == 0:
                Bonus_bomb(random.randint(0, width - 50), -30)
            if bonuses_count % shields == 0:
                Bonus_shield(random.randint(0, width - 50), -30)
            if endless_survival and bonuses_count % 100 == 0 and difficulty_game != 2:
                difficulty_game -= 1
            text1 = f1.render(f'number of asteroids destroyed:{asteroids}', True,
                              (180, 0, 0))
            all_sprites.update()
            all_sprites.draw(screen)
            screen.blit(text1, (10, 25))
            pygame.display.flip()
            clock.tick(FPS)
            if not endless_survival:
                if time == 18000 or asteroids > 100:
                    t = 0
                    flag = 1
                    dying = True
                    playing = False
        while dying:
            img = Image(game_over_sprite, flag)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            game_over_sprite.update()
            game_over_sprite.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
            t += 1
            if t >= 20:
                screen.fill((0, 0, 0))
                pygame.display.flip()
                menu = True
                dying = False
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
                buttons_sprite_menu = pygame.sprite.Group()
                buttons_sprite_difficulty = pygame.sprite.Group()
                game_over_sprite = pygame.sprite.Group()
                Border(width + 1, 0, width + 1, height + 1)
                Border(-1, -1, -1, height + 1)
                soplo_fl = 0
                spaceship = Spaceship(395, 600)
                povorot = 0
                count_mov = 0
                time = 0
                t = 0
                asteroids = 0
                flag = 0
    pygame.quit()
