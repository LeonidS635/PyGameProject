import pygame
import os
import random

running = True
FPS = 50
WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
colors = ["Red", "Green", "Blue", "Pink", "Purple", "Yellow", "Brown", "Grey", "Black", "White"]

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
platform = pygame.sprite.Group()
bricks = pygame.sprite.Group()
ball = pygame.sprite.Group()
gameover = pygame.sprite.Group()
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


class GameOver(pygame.sprite.Sprite):
    image1 = load_image("game_over.png")
    image = pygame.transform.scale(image1, (WIDTH + 10, HEIGHT))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = GameOver.image
        self.rect = self.image.get_rect()
        self.rect.x = -WIDTH
        self.rect.y = 0

        self.add(gameover)

    def update(self):
        v = 300
        x = v / FPS
        self.rect.x += x
        if self.rect.x >= -5:
            x = -x
        self.rect = self.rect.move(x, 0)


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


class Bricks(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(all_sprites)
        self.image = pygame.Surface((65, 15))
        self.image.fill(pygame.Color(color))

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.add(bricks)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((50, 10))
        self.image.fill(pygame.Color("Grey"))

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.add(platform)

    def update(self, x):
        if x > 0:
            if self.rect.left > WIDTH:
                self.rect.right = 0
        if x < 0:
            if self.rect.right < 0:
                self.rect.left = WIDTH
        self.rect = self.rect.move(x, 0)


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius):
        super().__init__(all_sprites)
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (radius, radius), radius)
        self.rect = pygame.Rect(250, 420, 2 * radius, 2 * radius)

        self.v = 100
        self.vy = self.v / FPS
        self.vx = self.v / FPS

        self.add(ball)

    def update(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = 0
                self.vx = 0
                self.rect.x = 250
                self.rect.y = 420
                GameOver()
            else:
                self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx

        if pygame.sprite.spritecollideany(self, platform):
            platform_list = pygame.sprite.spritecollide(self, platform, False)
            for pl in platform_list:
                if abs(self.rect.y - pl.rect.y) < 8 and 0 < pl.rect.center[0] - self.rect.center[0] < 30:
                    self.rect.x = pl.rect.x - 11
                    self.vy = -self.v / FPS
                    self.vx = -self.v / FPS
                    pl.vx = 0
                elif abs(self.rect.y - pl.rect.y) < 8 and 0 < self.rect.center[0] - pl.rect.center[0] < 30:
                    self.rect.x = pl.rect.x + 50
                    self.vy = -self.v / FPS
                    self.vx = self.v / FPS
                    pl.vx = 0
                else:
                    self.vy = -self.vy

        if pygame.sprite.spritecollideany(self, bricks):
            brick_list = pygame.sprite.spritecollide(self, bricks, True)
            for brick in brick_list:
                if abs(self.rect.y - brick.rect.y) < 8 and 0 < brick.rect.center[0] - self.rect.center[0] < 38:
                    self.vx = -self.vx
                elif abs(self.rect.y - brick.rect.y) < 8 and 0 < self.rect.center[0] - brick.rect.center[0] < 38:
                    self.vx = -self.vx
                else:
                    self.vy = -self.vy

        if self.rect.left < -1 or self.rect.right > WIDTH + 1:
            self.rect.x = 250
            self.rect.y = 350
            self.vy = self.v / FPS

        self.rect = self.rect.move(self.vx, self.vy)


Border(0, -1, WIDTH, 0)
Border(0, HEIGHT, WIDTH, HEIGHT)
Border(0, 0, 0, HEIGHT)
Border(WIDTH - 1, 0, WIDTH - 1, HEIGHT)

Player((230, 450))
Ball(5)

for j in range(15):
    for i in range(7):
        Bricks((8 + 70 * i, 8 + 20 * j), random.choice(colors))

while running:
    x = 0
    screen.fill((30, 170, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x = -8
    elif keys[pygame.K_RIGHT]:
        x = 8
    platform.update(x)
    ball.update()
    gameover.update()

    all_sprites.draw(screen)
    #all_sprites.update()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
