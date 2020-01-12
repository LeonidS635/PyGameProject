import pygame
import os
import random

running = True
flag = True
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


def start_screen():
    intro_text = ["АРКАНОИД", "", "",
                  "Правила игры: управляйте платформой",
                  "с помощью стрелок на клавиатуре", "",
                  "Цель - убрать все блоки", "",
                  "Не допускайте падения шарика",
                  "(касания нижней границы экрана)",
                  "Приятной игры!"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 40)
    text_coord = 50

    string_rendered = font.render(intro_text[0], 1, (23, 70, 200))
    intro_rect = string_rendered.get_rect()
    text_coord += 10
    intro_rect.top = text_coord
    intro_rect.x = WIDTH /2 - 86
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(None, 30)
    text_coord = 50

    for line in intro_text[1:-1]:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(None, 40)
    text_coord = HEIGHT * 0.9
    string_rendered = font.render(intro_text[-1], 1, (23, 70, 200))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = WIDTH / 2 - 110
    screen.blit(string_rendered, intro_rect)


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
    def __init__(self, radius, fps):
        super().__init__(all_sprites)
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (radius, radius), radius)
        self.rect = pygame.Rect(250, 420, 2 * radius, 2 * radius)

        v = 50
        self.vy = v / fps
        self.vx = v / fps

        self.add(ball)


    def update(self, *args):
        #if len(pygame.sprite.spritecollide(self, bombs, False)) >= 2:
         #   self.x = -self.x
          #  self.y = -self.y
        if pygame.sprite.spritecollideany(self, platform):
            brick_list = pygame.sprite.spritecollide(self, platform, False)
            for brick in brick_list:
                if abs(self.rect.y - brick.rect.y) <= 10 and self.rect.x < brick.rect.x:
                    print(1)
                    if self.vx < 0:
                        self.vy = -self.vy
                        self.rect.x = brick.rect.x - 11
                    else:
                        self.vx = -self.vx
                        self.vy = -self.vy
                elif abs(self.rect.y - brick.rect.y) <= 10 and self.rect.x >= brick.rect.x + 50:
                    print(2)
                    if self.vx < 0:
                        self.vx = -self.vx
                    else:
                        self.vy = -self.vy
                else:
                    self.vy = -self.vy
        if pygame.sprite.spritecollide(self, bricks, True):
            brick_list = pygame.sprite.spritecollide(self, bricks, True)
            for brick in brick_list:
                if self.rect.right == brick.rect.left or self.rect.left == brick.rect.right:
                    self.vx = -self.vx
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        #self.rect = self.rect.move(self.x, self.y)

        #if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
         #   self.image = self.image_boom
        self.rect = self.rect.move(self.vx, self.vy)


def start():
    Border(0, -1, WIDTH, 0)
    Border(0, HEIGHT, WIDTH, HEIGHT)
    Border(0, 0, 0, HEIGHT)
    Border(WIDTH, 0, WIDTH, HEIGHT)

    Player((230, 450))
    Ball(5, 50)

    for j in range(15):
        for i in range(7):
            Bricks((8 + 70 * i, 8 + 20 * j), random.choice(colors))

start_screen()

while running:
    x = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if flag:
                start()
            flag = False

    if not flag:
        screen.fill((30, 170, 40))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            for sprite in all_sprites:
                sprite.kill()
            start_screen()
            flag = True
        if keys[pygame.K_LEFT]:
            x = -8
        elif keys[pygame.K_RIGHT]:
            x = 8
        platform.update(x)
        ball.update()

        all_sprites.draw(screen)
    #all_sprites.update()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
