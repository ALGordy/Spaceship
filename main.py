import pygame
import random
import sys
import os

width, height = 1000, 1000
FPS = 60
size = width, height
running = True
menu = True
playing = True
moving = True
difficulty = True
screen = pygame.display.set_mode(size)
delta_x = 0
delta_y = 0
asteroids_count = 0
bonuses_count = 0
difficulty_game = 1
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
bullets_sprite = pygame.sprite.Group()
asteroid_sprite = pygame.sprite.Group()
bonuses_sprite = pygame.sprite.Group()
buttons_sprite_menu = pygame.sprite.Group()
buttons_sprite_difficulty = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
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
        if moving and 950 >= self.x + spaceship_delta_x >= 0 and 950 >= self.y + spaceship_delta_y >= 500:
            self.x += spaceship_delta_x
            self.y += spaceship_delta_y
            self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def update(self):
        for i in asteroid_sprite:
            if pygame.sprite.collide_mask(self, i):
                self.kill()
                pygame.quit()
        for i in bonuses_sprite:
            if pygame.sprite.collide_mask(self, i) and self.bonusrect:
                self.bonuses += 1
                i.kill()

    def upd_img(self, fl):
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
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.add(all_sprites)
        self.add(bullets_sprite)
        self.image = load_image("bullet.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.y -= 10
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        for i in asteroid_sprite:
            if self.y < -50 or self.y > 1050 or pygame.sprite.collide_mask(self, i):
                self.kill()
                if pygame.sprite.collide_mask(self, i):
                    i.kill()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        self.add(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.image.fill((49, 194, 119))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.image.fill((49, 194, 119))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


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


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, flag):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.add(asteroid_sprite)
        if flag == 1:
            self.image = load_image("asteroid.png")
        elif flag == 2:
            self.image = load_image("big_asteroid.png")
        else:
            self.image = load_image("mid_asteroid.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.vx = random.randint(0, 5)
        self.vy = random.randrange(10, 15)

    # движение с проверкой столкновение шара со стенками
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        for i in vertical_borders:
            if pygame.sprite.collide_mask(self, i):
                self.vx = -self.vx
        for i in bullets_sprite:
            if self.y < -50 or self.y > 1050 or pygame.sprite.collide_mask(self, i):
                self.kill()
                if pygame.sprite.collide_mask(self, i):
                    i.kill()


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
        for i in vertical_borders:
            if pygame.sprite.collide_mask(self, i):
                self.vx = -self.vx


Border(width - 0, 0, width - 0, height - 0)
Border(-1, -1, -1, height + 1)

spaceship = Spaceship(500, 900)
povorot = 0
if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.flip()
    count_mov = 0
    while running:
        while menu:
            play = Buttons_menu('play.jpg', 450, 450)
            quit = Buttons_menu('quit.jpg', 450, 550)
            fon_menu = pygame.transform.scale(load_image('fon_menu.png'), (width, height))
            screen.blit(fon_menu, (0, 0))
            buttons_sprite_menu.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    menu = False
                    playing = False
                    difficulty = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play.rect.collidepoint(event.pos):
                        difficulty = True
                        menu = False
                    if quit.rect.collidepoint(event.pos):
                        running = False
                        menu = False
                        playing = False
                        difficulty = False
        while difficulty:
            easy = Buttons_difficulty('easy.jpg', 450, 400)
            medium = Buttons_difficulty('medium.jpg', 450, 450)
            hard = Buttons_difficulty('hard.jpg', 450, 500)
            fon_menu = pygame.transform.scale(load_image('fon_menu.png'), (width, height))
            screen.blit(fon_menu, (0, 0))
            buttons_sprite_difficulty.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    menu = False
                    difficulty = False
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy.rect.collidepoint(event.pos):
                        playing = True
                        difficulty = False
                        difficulty_game = 3
                    if medium.rect.collidepoint(event.pos):
                        playing = True
                        difficulty = False
                        difficulty_game = 2
                    if hard.rect.collidepoint(event.pos):
                        playing = True
                        difficulty = False
                        difficulty_game = 1
        while playing:
            fon_game = pygame.transform.scale(load_image('fon.png'), (width, height))
            screen.blit(fon_game, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    playing = False
                    menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if spaceship.bonuses == 1:
                        bullet = Bullet(spaceship.x + 35, spaceship.y)
                    elif 3 > spaceship.bonuses > 1:
                        bullet = Bullet(spaceship.x + 15, spaceship.y)
                        bullet1 = Bullet(spaceship.x + 55, spaceship.y)
                    elif 3 <= spaceship.bonuses:
                        bullet = Bullet(spaceship.x + 15, spaceship.y)
                        bullet1 = Bullet(spaceship.x + 35, spaceship.y)
                        bullet2 = Bullet(spaceship.x + 55, spaceship.y)
                if event.type == pygame.KEYDOWN:
                    moving = True
                    if pygame.key.get_pressed()[pygame.K_d]:
                        delta_x = 8
                        spaceship.upd_img(3)
                        count_mov = 1
                        povorot = 2
                    if pygame.key.get_pressed()[pygame.K_a]:
                        delta_x = -8
                        spaceship.upd_img(1)
                        count_mov = 1
                        povorot = 1
                    if pygame.key.get_pressed()[pygame.K_s]:
                        delta_y = 8
                    if pygame.key.get_pressed()[pygame.K_w]:
                        delta_y = -8
                    if pygame.key.get_pressed()[pygame.K_d] and pygame.key.get_pressed()[pygame.K_a]:
                        delta_x = 0
                        spaceship.upd_img(0)
                        count_mov = 0
                        povorot = 0

                if count_mov != 0:
                    count_mov += 1
                if povorot == 1 and count_mov == 10:
                    spaceship.upd_img(2)
                    count_mov = 0
                    povorot = 0
                if povorot == 2 and count_mov == 10:
                    spaceship.upd_img(4)
                    count_mov = 0
                    povorot = 0
                if event.type == pygame.KEYUP and (event.key == pygame.K_a or event.key == pygame.K_d):
                    delta_x = 0
                    spaceship.upd_img(0)
                    count_mov = 0
                    povorot = 0
                if event.type == pygame.KEYUP and (event.key == pygame.K_w or event.key == pygame.K_s):
                    delta_y = 0
                    spaceship.upd_img(0)
                    count_mov = 0
                    povorot = 0
            clock = pygame.time.Clock()
            fon = pygame.transform.scale(load_image('fon.png'), (width, height))
            screen.blit(fon, (0, 0))
            spaceship.moving(delta_x, 0)
            spaceship.moving(0, delta_y)
            asteroids_count += 1
            bonuses_count += 1
            if asteroids_count % (3 * difficulty_game) == 0 and asteroids_count % (6 * difficulty_game) != 0 and asteroids_count % (9 * difficulty_game) != 0:
                Asteroid(random.randint(0, width), -30, 0)
            if asteroids_count % (6 * difficulty_game) == 0 and asteroids_count % (9 * difficulty_game) != 0:
                Asteroid(random.randint(0, width), -30, 1)
            if asteroids_count % (9 * difficulty_game) == 0:
                Asteroid(random.randint(0, width), -30, 2)
            if bonuses_count % (500 * difficulty_game) == 0:
                Bonus(random.randint(0, width), -30)
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
    pygame.quit()
