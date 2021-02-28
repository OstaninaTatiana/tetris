import pygame
import os
import sys
import random


pygame.init()
size = width, height = 350, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
s_all_sprites = []


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Detale1(pygame.sprite.Sprite):
    size_name_of_file = {'1.png': (100, 25),
                         '2.png': (50, 50),
                         '3.png': (50, 75),
                         '4.png': (75, 50),
                         '5.png': (50, 75),
                         '6.png': (75, 50),
                         '7.png': (25, 100),
                         '8.png': (50, 75),
                         '9.png': (50, 75),
                         '10.png': (75, 50),
                         '11.png': (50, 75),
                         '12.png': (75, 50),
                         '13.png': (75, 50)}

    def __init__(self, pos=(150, 0), name_of_file=random.choice(('1.png', '2.png', '3.png', '4.png',
                                                                 '5.png', '6.png', '7.png', '8.png',
                                                                 '9.png', '10.png', '11.png', '12.png', '13.png'))):
        print(name_of_file)
        self.image = pygame.transform.scale(load_image(name_of_file), self.size_name_of_file[name_of_file])
        super().__init__(all_sprites)
        self.image = self.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.v = 1

    def update(self, g_v=0):
        if self.rect.left == 0 and g_v < 0:
            g_v = 0
        if self.rect.right == 350 and g_v > 0:
            g_v = 0
        self.rect.top += self.v
        self.rect.left += g_v
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.v = 0
        for i in s_all_sprites:
            if pygame.sprite.collide_mask(self, i):
                self.v = 0
                s_all_sprites.append(self)
                break


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


fps = 60
running = True
v = 10  # пикселей в секунду
clock = pygame.time.Clock()
detale = None

while running:
    new_game = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == 32:
            new_game = True
            del all_sprites
            all_sprites = pygame.sprite.Group()
            s_all_sprites.clear()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if detale:
                detale.update(g_v=25)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if detale:
                detale.update(g_v=-25)

    if new_game:
        detale = Detale1(name_of_file=random.choice(('1.png', '2.png', '3.png', '4.png',
                                                     '5.png', '6.png', '7.png', '8.png',
                                                     '9.png', '10.png', '11.png', '12.png', '13.png')))

    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    text = font.render('''Для начала игры нажмите пробел''', True, (100, 255, 100))
    text_x = 7
    text_y = 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    for i in range(14):
        pygame.draw.line(screen, pygame.Color('white'), (25 + 25 * i, 25), (25 + 25 * i, 500), 1)
    for i in range(25):
        pygame.draw.line(screen, pygame.Color('white'), (0, 25 + 25 * i), (350, 25 + 25 * i), 1)
    s_all_sprites.append(Border(0, height, width, height))

    all_sprites.draw(screen)
    all_sprites.update()
    if detale:
        if detale in s_all_sprites:
            detale = Detale1(name_of_file=random.choice(('1.png', '2.png', '3.png', '4.png',
                                                         '5.png', '6.png', '7.png', '8.png',
                                                         '9.png', '10.png', '11.png', '12.png', '13.png')))
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
