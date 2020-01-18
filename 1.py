import pygame
import os
import random

running = True
flag = True
FLAG_LEVEL_1 = True
FLAG_LEVEL_2 = False
FLAG_LEVEL_3 = False
LEVEL_3_BALL = 0
FLAG_LEVEL_4 = False
FLAG_WIN = False
MYEVENTTYPE = 30
TIME = 20
GRAVITY = 0.5
FPS = 50
WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
colors = ["Red", "Green", "Blue", "Pink", "Purple", "Yellow", "Brown", "Grey", "Black", "White"]
screen_rect = (0, 0, WIDTH, HEIGHT)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
platform = pygame.sprite.Group()
bricks = pygame.sprite.Group()
ball = pygame.sprite.Group()
stars = pygame.sprite.Group()
gameover = pygame.sprite.Group()
youwin = pygame.sprite.Group()
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
    intro_rect.x = WIDTH / 2 - 86
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


def draw(number_of_level):
        font = pygame.font.Font(None, 25)
        text = font.render("LEVEL" + ' ' + str(number_of_level), 1, (0, 0, 0))
        text_x = 8
        text_y = 480
        screen.blit(text, (text_x, text_y))


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png", -1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

        self.add(stars)

    def update(self):
        self.velocity[1] += self.gravity
        self.velocity[0] += random.choice([-1, 0, 1])

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)

    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


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


class YouWin(pygame.sprite.Sprite):
    image1 = load_image("you_win.jpg")
    image = pygame.transform.scale(image1, (WIDTH + 10, HEIGHT))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = YouWin.image
        self.rect = self.image.get_rect()
        self.rect.x = -WIDTH
        self.rect.y = 0

        self.add(youwin)

    def update(self):
        v = 300
        x = v / FPS
        self.rect.x += x
        if self.rect.x >= -5:
            x = -x
        self.rect = self.rect.move(x, 0)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, flag_bottom):
        super().__init__(all_sprites)
        self.flag_bottom = flag_bottom
        # вертикальная стенка
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        # горизонтальная стенка
        else:
            self.add(horizontal_borders)
            if self.flag_bottom:
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
    def __init__(self, radius, v_ball):
        super().__init__(all_sprites)
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (radius, radius), radius)
        self.rect = pygame.Rect(250, 420, 2 * radius, 2 * radius)

        self.v = v_ball
        self.vy = self.v / FPS
        self.vx = self.v / FPS

        self.add(ball)

    def update(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if pygame.sprite.spritecollideany(self, horizontal_borders_bottom):
                for sprite in ball:
                    sprite.kill()
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

        if self.rect.left < -5 or self.rect.right > WIDTH + 5:
            self.rect.x = 250
            self.rect.y = 350
            self.vy = self.v / FPS

        self.rect = self.rect.move(self.vx, self.vy)


def level_1():
    v_platform = 8
    v_ball = 100
    return v_platform, v_ball


def level_2():
    v_platform = 3
    v_ball = 150
    return v_platform, v_ball


def level_3():
    v_platform = 9
    v_ball = 100
    return v_platform, v_ball


def level_4():
    v_platform = 50
    v_ball = 100
    return v_platform, v_ball


def start():
    Border(0, 0, WIDTH, 0, False)
    Border(0, HEIGHT, WIDTH, HEIGHT, True)
    Border(0, 0, 0, HEIGHT, False)
    Border(WIDTH - 1, 0, WIDTH - 1, HEIGHT, False)

    Player((230, 450))

    if FLAG_LEVEL_1:
        Ball(5, level_1()[1])
    if FLAG_LEVEL_2:
        Ball(5, level_2()[1])
    if FLAG_LEVEL_3:
        pygame.time.set_timer(MYEVENTTYPE, 100)
    if FLAG_LEVEL_4:
        Ball(5, level_4()[1])

    for j in range(15):
        for i in range(7):
            Bricks((8 + 70 * i, 8 + 20 * j), random.choice(colors))


start_screen()

while running:
    x = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and flag:
            if not FLAG_LEVEL_2 and not FLAG_LEVEL_3 and not FLAG_LEVEL_4:
                FLAG_LEVEL_1 = True
            start()

            flag = False
            LEVEL_3_BALL = 0
        if event.type == MYEVENTTYPE and LEVEL_3_BALL < 2 and FLAG_LEVEL_3:
            Ball(5, level_3()[1])
            LEVEL_3_BALL += 1
        if event.type == TIME and FLAG_WIN:
            create_particles((150, 34))
            create_particles((390, 340))
            create_particles((420, 10))
            create_particles((150, 150))
            create_particles((60, 400))

    if not flag:
        screen.fill((30, 170, 40))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            if FLAG_WIN:
                flag = False
            else:
                for sprite in all_sprites:
                    sprite.kill()
                start_screen()
                flag = True

        elif keys[pygame.K_ESCAPE]:
            for sprite in all_sprites:
                sprite.kill()
            start_screen()
            flag = True
            FLAG_LEVEL_1 = False
            FLAG_LEVEL_2 = False
            FLAG_LEVEL_3 = False
            FLAG_LEVEL_4 = False
            FLAG_WIN = False

        elif keys[pygame.K_LEFT]:
            if FLAG_LEVEL_1:
                x = -level_1()[0]
            if FLAG_LEVEL_2:
                x = -level_2()[0]
            if FLAG_LEVEL_3:
                x = -level_3()[0]
            if FLAG_LEVEL_4:
                x = -level_4()[0]

        elif keys[pygame.K_RIGHT]:
            if FLAG_LEVEL_1:
                x = level_1()[0]
            if FLAG_LEVEL_2:
                x = level_2()[0]
            if FLAG_LEVEL_3:
                x = level_3()[0]
            if FLAG_LEVEL_4:
                x = level_4()[0]

        platform.update(x)
        ball.update()
        gameover.update()
        youwin.update()
        stars.update()

    if not flag:
        if len(bricks) <= 103 and FLAG_LEVEL_1:
            FLAG_LEVEL_1 = False
            FLAG_LEVEL_2 = True
            for sprite in all_sprites:
                sprite.kill()
            start()

        if len(bricks) <= 103 and FLAG_LEVEL_2:
            FLAG_LEVEL_2 = False
            FLAG_LEVEL_3 = True
            LEVEL_3_BALL = 0
            for sprite in all_sprites:
                sprite.kill()
            start()

        if len(bricks) <= 100 and FLAG_LEVEL_3:
            FLAG_LEVEL_3 = False
            FLAG_LEVEL_4 = True
            for sprite in all_sprites:
                sprite.kill()
            start()

        if len(bricks) <= 104 and FLAG_LEVEL_4:
            FLAG_LEVEL_4 = False
            FLAG_WIN = True
            pygame.time.set_timer(TIME, 900)
            for sprite in all_sprites:
                sprite.kill()
            YouWin()

        if FLAG_LEVEL_1:
            draw(1)
        if FLAG_LEVEL_2:
            draw(2)
        if FLAG_LEVEL_3:
            draw(3)
        if FLAG_LEVEL_4:
            draw(4)

    all_sprites.draw(screen)
    #all_sprites.update()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
