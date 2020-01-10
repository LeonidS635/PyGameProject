import pygame
import os
import random

running = True
FPS = 50
WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
platform = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
horizontal_borders_bottom = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        # вертикальная стенка
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)

            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        # горизонтальная стенка
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

            self.add(horizontal_borders)
            self.add(horizontal_borders_bottom)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, fps):
        super().__init__(all_sprites)
        self.image = pygame.Surface((50, 10))
        self.image.fill(pygame.Color("Grey"))

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.add(platform)

        v = 50
        self.vx = v / fps

    def update(self, x):
        if x > 0:
            if self.rect.left > WIDTH:
                self.rect.right = 0
        if x < 0:
            if self.rect.right < 0:
                self.rect.left = WIDTH
        self.rect = self.rect.move(x, 0)


class Ball(pygame.sprite.Sprite):
    image = load_image("bomb3.png", -1)
    image_boom = load_image("boom.png", -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.x = 250
        self.y = 440

        f = True

        while f:
            self.rect.x = random.randrange(WIDTH)
            self.rect.y = random.randrange(HEIGHT)

            if (pygame.sprite.spritecollideany(self, bombs) is None and (
                    pygame.sprite.spritecollideany(self, horizontal_borders) is None) and (
                    pygame.sprite.spritecollideany(self, vertical_borders) is None)):
                f = False

        self.add(bombs)

    def update(self, *args):
        if len(pygame.sprite.spritecollide(self, bombs, False)) >= 2:
            self.x = -self.x
            self.y = -self.y
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.x = -self.x
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.y = -self.y

        self.rect = self.rect.move(self.x, self.y)

        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom


Border(0, 0, WIDTH, 0)
Border(-1, HEIGHT, WIDTH, HEIGHT)
Border(0, 0, 0, HEIGHT)
Border(WIDTH, 0, WIDTH, HEIGHT)

Player((230, 450), 50)

while running:
    x = 0
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x = -8
    elif keys[pygame.K_RIGHT]:
        x = 8
    platform.update(x)

    all_sprites.draw(screen)
    #all_sprites.update(event)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()