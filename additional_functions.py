import itertools
import pygame
import settings
import os


class Button(pygame.sprite.Sprite):
    """Создать кнопку - прямоугольник с текстом
    w - ширина кнопки в px
    h - высота кнопки в px
    cords - координаты кнопки в клетках поля, размером settings.TILE_SIZE
    text - текст, расположенный на кнопке
    group - группа спрайтов, в которую входит объект Button
    screen - pygame.Surface(), где будет рисоваться сама кнопка

    """
    def __init__(self, w, h, coords, text, group, screen):
        super().__init__(group)
        self.screen = screen
        self.w = w
        self.h = h
        self.coords = (coords[0] * settings.TILE_SIZE, coords[1] * settings.TILE_SIZE)
        self.rect = pygame.Rect(self.coords[0], self.coords[1], self.w, self.h)
        self.text = text

    def update(self, *args):
        pygame.draw.rect(self.screen, pygame.Color('grey'), self.rect)
        font = pygame.font.Font(None, 25)
        text_coord = self.coords[1]
        string_rendered = font.render(self.text, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = self.coords[0] + 30
        text_coord += intro_rect.height
        self.screen.blit(string_rendered, intro_rect)


class Fader:
    """Затемнение экрана при переходе к и от экрана смерти
    (пока не реализовано)
    """
    def __init__(self, scenes):
        self.scenes = itertools.cycle(scenes)
        self.scene = next(self.scenes)
        self.fading = None
        self.alpha = 0
        sr = pygame.display.get_surface().get_rect()
        self.veil = pygame.Surface(sr.size)
        self.veil.fill((0, 0, 0))

    def next(self):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0

    def draw(self, screen):
        self.scene.draw(screen)
        if self.fading:
            self.veil.set_alpha(self.alpha)
            screen.blit(self.veil, (0, 0))

    def update(self, dt, events):
        self.scene.update(dt, events)
        if self.fading == 'OUT':
            self.alpha += 8
            if self.alpha >= 255:
                self.fading = 'IN'
                self.scene = next(self.scenes)
        else:
            self.alpha -= 8
            if self.alpha <= 0:
                self.fading = None


def load_level(filename):
    """Загрузить уровень из файла в папке data в list

    filename - путь к файлу

    """
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, trans=0):
    """Загрузить картинку из папки data/

    name -- путь к картинке
    trans -- 0 - фон картинки прозрачен
          -- -1 - сделать прозрачным цвет в верхнем левом углу картинки

    """
    full_name = os.path.join('data', name)
    image = pygame.image.load(full_name).convert()
    if trans is not None:
        if trans == -1:
            trans = image.get_at((0, 0))
        image.set_colorkey(trans)
    else:
        image = image.convert_alpha()
    return image


idleL, idleR, RunningL, RunningR = [list() for _ in range(4)]
idleLrev, idleRrev, RunningLrev, RunningRrev = [list() for _ in range(4)]

animIdle, animRun = 0, 0


def animation():
    global idleL, idleR, RunningL, RunningR
    global idleLrev, idleRrev, RunningLrev, RunningRrev

    # Бездействие
    for i in range(18):
        idleR.append(pygame.image.load(f'data/idleR/0_Reaper_Man_Idle_{str(i).rjust(3, "0")}.png'))
    for i in range(18):
        idleL.append(pygame.image.load(f'data/idleL/0_Reaper_Man_Idle_{str(i).rjust(3, "0")}.png'))

    # Бег
    for i in range(12):
        RunningR.append(pygame.image.load(f'data/RunningR/0_Reaper_Man_Running_{str(i).rjust(3, "0")}.png'))
    for i in range(12):
        RunningL.append(pygame.image.load(f'data/RunningL/0_Reaper_Man_Running_{str(i).rjust(3, "0")}.png'))

    # Бездействие ревёрс
    for i in range(18):
        idleRrev.append(pygame.image.load(f'data/idleRrev/0_Reaper_Man_Idle_{str(i).rjust(3, "0")}.png'))
    for i in range(18):
        idleLrev.append(pygame.image.load(f'data/idleLrev/0_Reaper_Man_Idle_{str(i).rjust(3, "0")}.png'))

    # Бег ревёрс
    for i in range(12):
        RunningRrev.append(pygame.image.load(f'data/RunningRrev/0_Reaper_Man_Running_{str(i).rjust(3, "0")}.png'))
    for i in range(12):
        RunningLrev.append(pygame.image.load(f'data/RunningLrev/0_Reaper_Man_Running_{str(i).rjust(3, "0")}.png'))

    for elem in [idleR, idleL, RunningL, RunningR, idleRrev, idleLrev, RunningLrev, RunningRrev]:
        for i in range(len(elem)):
            elem[i] = elem[i].convert()
            elem[i].set_colorkey((255, 255, 255))
