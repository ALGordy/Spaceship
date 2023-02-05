import pygame
import random

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


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.bonuses = 1
        self.bonusrect = True
        self.add(all_sprites)
        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 0, 255))
        self.rect = pygame.Rect(x, y, 50, 50)

    def moving(self, spaceship_delta_x, spaceship_delta_y):
        if moving and 950 >= self.x + spaceship_delta_x >= 0 and 950 >= self.y + spaceship_delta_y >= 500:
            self.x += spaceship_delta_x
            self.y += spaceship_delta_y
            self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def update(self):
        if pygame.sprite.spritecollideany(self, asteroid_sprite):
            self.kill()
            pygame.quit()
        if pygame.sprite.spritecollideany(self, bonuses_sprite) and self.bonusrect:
            self.bonuses += 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.add(all_sprites)
        self.add(bullets_sprite)
        self.image = pygame.Surface([10, 10])
        self.image.fill((255, 255, 0))
        self.rect = pygame.Rect(x, y, 10, 10)

    def update(self):
        self.y -= 10
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        if self.y < -50 or self.y > 1050 or pygame.sprite.spritecollideany(self, asteroid_sprite):
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
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.add(asteroid_sprite)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("grey"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(0, 5)
        self.vy = random.randrange(10, 15)

    # движение с проверкой столкновение шара со стенками
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if self.y < -50 or self.y > 1050 or pygame.sprite.spritecollideany(self, bullets_sprite):
            self.kill()


class Bonus(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.add(bonuses_sprite)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("yellow"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(0, 5)
        self.vy = random.randrange(10, 15)

    # движение с проверкой столкновение шара со стенками
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


Border(width - 0, 0, width - 0, height - 0)
Border(-1, -1, -1, height + 1)

spaceship = Spaceship(500, 900)

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(spaceship.bonuses)
                if spaceship.bonuses == 1:
                    bullet = Bullet(spaceship.x + 20, spaceship.y)
                elif 10 >= spaceship.bonuses > 1:
                    bullet = Bullet(spaceship.x, spaceship.y)
                    bullet1 = Bullet(spaceship.x + 40, spaceship.y)
                elif 20 <= spaceship.bonuses:
                    bullet = Bullet(spaceship.x + 20, spaceship.y)
                    bullet1 = Bullet(spaceship.x, spaceship.y)
                    bullet2 = Bullet(spaceship.x + 40, spaceship.y)
            if event.type == pygame.KEYDOWN:
                moving = True
                if pygame.key.get_pressed()[pygame.K_d]:
                    delta_x = 8
                if pygame.key.get_pressed()[pygame.K_a]:
                    delta_x = -8
                if pygame.key.get_pressed()[pygame.K_s]:
                    delta_y = 8
                if pygame.key.get_pressed()[pygame.K_w]:
                    delta_y = -8
            if event.type == pygame.KEYUP and (event.key == pygame.K_a or event.key == pygame.K_d):
                    delta_x = 0
            if event.type == pygame.KEYUP and (event.key == pygame.K_w or event.key == pygame.K_s):
                    delta_y = 0

        spaceship.moving(delta_x, 0)
        spaceship.moving(0, delta_y)
        asteroids_count += 1
        bonuses_count += 1
        if asteroids_count % 10 == 0:
            Asteroid(30, random.randint(0, width), -30)
        if bonuses_count % 100 == 0:
            Bonus(30, random.randint(0, width), -30)
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
