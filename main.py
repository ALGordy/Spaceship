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
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
bullets_sprite = pygame.sprite.Group()


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.add(all_sprites)
        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 0, 255))
        self.rect = pygame.Rect(x, y, 50, 50)

    def moving(self, spaceship_delta_x, spaceship_delta_y):
        if moving and 950 >= self.x + spaceship_delta_x >= 0 and 950 >= self.y + spaceship_delta_y >= 500:
            self.x += spaceship_delta_x
            self.y += spaceship_delta_y
            self.rect = pygame.Rect(self.x, self.y, 50, 50)


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


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        self.add(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


# Border(0, 0, width, 0)
# Border(0, height, width, height)
# Border(0, 0, 0, height)
# Border(width, 0, width, height)

spaceship = Spaceship(500, 900)

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(spaceship.x + 20, spaceship.y)
            if event.type == pygame.KEYDOWN:
                moving = True
                if pygame.key.get_pressed()[pygame.K_d]:
                    delta_x = 5
                if pygame.key.get_pressed()[pygame.K_a]:
                    delta_x = -5
                if pygame.key.get_pressed()[pygame.K_s]:
                    delta_y = 5
                if pygame.key.get_pressed()[pygame.K_w]:
                    delta_y = -5
            if event.type == pygame.KEYUP:
                moving = False
                delta_x = 0
                delta_y = 0
        spaceship.moving(delta_x, delta_y)
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
