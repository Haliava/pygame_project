import math
import sys
import time

import additional_functions
import pygame
import settings

TILE_SIZE = settings.TILE_SIZE


class GameObject:
    def __init__(self):
        self.rect = pygame.Rect(TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def collide_with_sth(self, object_type=None):
        for i in all_sprites:
            if object_type is None:
                if self.rect.colliderect(i) and i is not self:
                    return True, type(i)
            else:
                if self.rect.colliderect(i) and i is not self and type(i) == object_type:
                    return True, (i.rect.x, i.rect.y)
        return False, None


class Player(pygame.sprite.Sprite, GameObject):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.ready_to_change_gravity = True
        self.g = 1.1
        self.direction = 1
        self.vy = 0
        self.rect = pygame.Rect(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE)

    def idle(self, animIdle):
        global stay, sum1
        coords = (int(self.rect.x), int(self.rect.y - 12))
        letter = 'R' if stay == 1 else 'L'
        if sum1 % 2 == 0:
            exec(f'screen.blit(additional_functions.idle{letter}[additional_functions.animIdle // 5], coords)')
        else:
            exec(f'screen.blit(additional_functions.idle{letter}rev[additional_functions.animIdle // 5], coords)')

    def run(self, animRun):
        global left, right
        coords = (int(self.rect.x), int(self.rect.y - 12))
        letter = 'L' if left else 'R'
        if sum1 % 2 == 0 and (left or right):
            exec(f'screen.blit(additional_functions.Running{letter}[{animRun} // 5], coords)')
        elif left or right:
            exec(f'screen.blit(additional_functions.Running{letter}rev[{animRun} // 5], coords)')

    def move(self, x, y):
        old_x, old_y, w, h = [int(x) for x in self.rect]
        self.rect = pygame.Rect(old_x, old_y + y, w, h)
        if self.vy == 0 and not self.collide_with_sth(Wall)[0]:
            self.vy = 5 * self.direction
        if self.collide_with_sth(Wall)[0] or self.collide_with_sth(Exit)[0]:
            collision_coords = self.collide_with_sth(Wall)[1] \
                if self.collide_with_sth(Wall)[0] else self.collide_with_sth(Exit)[1]
            self.rect.y = collision_coords[1] + -(TILE_SIZE * self.direction)
            self.ready_to_change_gravity = True
            self.vy = 0
        else:
            self.rect.x += x
        if self.collide_with_sth(Wall)[0]:
            self.rect = pygame.Rect(old_x, old_y, w, h)

    def update(self, *args):
        self.vy *= self.g
        if self.vy != 0:
            self.ready_to_change_gravity = False
            self.move(0, self.vy)
        if self.collide_with_sth(Wall)[0]:
            self.vy = 0
        # pygame.draw.rect(screen, pygame.Color('white'), self.rect)

    def change_gravity(self):
        self.direction *= -1
        self.vy = 5 * self.direction


class Spike(pygame.sprite.Sprite, GameObject):
    def __init__(self, x, y):
        super().__init__(spikes, all_sprites)
        self.rect = pygame.Rect(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE)

    def update(self, *args):
        pygame.draw.rect(screen, pygame.Color('red'), self.rect)


class Wall(pygame.sprite.Sprite, GameObject):
    def __init__(self, x, y):
        super().__init__(walls, all_sprites)
        self.initial_x = x
        self.initial_y = y
        self.rect = pygame.Rect(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE)

    def update(self, *args):
        pygame.draw.rect(screen, pygame.Color('black'), self.rect)


class Exit(pygame.sprite.Sprite, GameObject):
    def __init__(self, x, y):
        super().__init__(exits, all_sprites)
        self.rect = pygame.Rect(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE)

    def update(self, *args):
        pygame.draw.rect(screen, pygame.Color('green'), self.rect)


class Ball(pygame.sprite.Sprite, GameObject):
    def __init__(self, x, y, radius):
        super().__init__(balls, all_sprites)
        self.initial_x = x
        self.initial_y = y
        self.rect = pygame.Rect(TILE_SIZE * x, TILE_SIZE * y, radius, radius)
        self.r = radius
        self.hits = 0
        self.vx = 0
        self.vy = 5

    def update(self, *args):
        global ball_hit_sound, screen, main_mirror, level
        if self.collide_with_sth()[0]:
            ball_hit_sound.play()  # <-- звук здесь, его не терять
            is_collided_with_wall = self.collide_with_sth(Wall)
            is_collided_with_mirror = self.collide_with_sth(Mirror)
            if is_collided_with_wall[0]:
                # проверяется клетка, в которую прилетит шар на следующем кадре, на столкновение со стенами
                initial_ball_tile = (self.rect.center[0] // TILE_SIZE, self.rect.center[1] // TILE_SIZE)
                ball_tile = ((self.rect.center[0] + self.vx) // TILE_SIZE, (self.rect.center[1] + self.vy) // TILE_SIZE)
                for wall in walls:
                    c = 0
                    if (wall.initial_x, wall.initial_y) == ball_tile:
                        if abs(initial_ball_tile[1] - ball_tile[1]) == 1:
                            self.vy *= -1
                            c += 1
                        if abs(initial_ball_tile[0] - ball_tile[0]) == 1:
                            self.vx *= -1
                            c += 1
                    if c == 2:
                        i, j = initial_ball_tile[0], initial_ball_tile[1]
                        try:
                            horizontal, vertical = False, False
                            if level[j - 1][i] == '#' or level[j + 1][i] == '#':
                                vertical = True
                            if level[j][i - 1] == '#' or level[j][i + 1] == '#':
                                horizontal = True
                            if horizontal:
                                self.vy *= -1
                            elif vertical:
                                self.vx *= -1
                        except IndexError:
                            if j >= len(level) or j <= 0:
                                self.vy *= -1
                                break
                            if i >= len(level) or i <= 0:
                                self.vx *= -1
                                break
            elif is_collided_with_mirror[0]:
                self.reflect(main_mirror)
        self.rect.x += self.vx
        self.rect.y += self.vy
        pygame.draw.circle(screen, pygame.Color('yellow'), (self.rect.x, self.rect.y), self.r)

    def reflect(self, mirror):
        angle = int(mirror.angle)
        if player.direction == 1:
            num = 5
        else:
            num = -5
        if angle in range(-20, -71, -1):
            self.vx = num
        if angle in range(0, 10):
            self.vx = 0
            self.vy = -num
        elif angle in range(0, 71):
            self.vx = -num
        self.vy = -num


class Mirror(pygame.sprite.Sprite, GameObject):
    def __init__(self, m_image):
        super().__init__(all_sprites, mirror)
        self.m_image = m_image
        self.image = m_image
        self.angle = 0
        self.rect = self.image.get_rect()

    def update(self, *args):
        """Поворот зеркала.
        Управлять градусом поворота можно только при передвижении мыши на правой половине экрана
        ↑ - от 0 до 10 градусов
        → - от -20 до -50 градусов
        ← - от 0 до 50 градусов
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if not (self.angle < -50 or self.angle > 50):
            self.image = pygame.transform.rotate(self.m_image, int(self.angle))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        if player.direction == 1:
            self.rect.y = player.rect.y - 20
        else:
            self.rect.y = player.rect.y + 40


def generate_level(level):
    """Загрузить уровень из list в объекты, составляющие его
    . - пустая клетка
    # - клетка-стена
    ^ - клетка-шип
    @ - игрок
    $ - клетка-выход
    | - клетка-шар
    (размер всех клеток равен параметру TILE_SIZE из файла settings.py)
    """
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Wall(x, y)
            elif level[y][x] == '^':
                Spike(x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Exit(x, y)
            elif level[y][x] == '|':
                Ball(x, y, TILE_SIZE // 3)
    return new_player, x, y, level


def draw():
    global left, right
    if additional_functions.animIdle >= 85:
        additional_functions.animIdle = 0
    if additional_functions.animRun >= 55:
        additional_functions.animRun = 0
    if left or right:
        player.run(additional_functions.animRun)
        additional_functions.animRun += 1
    else:
        player.idle(additional_functions.animIdle)
        additional_functions.animIdle += 1


def pause(screen):
    global player, level_x, level_y
    time_0 = time.time()
    screen.fill(pygame.Color('black'))
    bg = pygame.transform.scale(additional_functions.load_image('pause.jpg', -1),
                                (settings.WIDTH, settings.HEIGHT))
    screen.blit(bg, (0, 0))
    to_menu_button = additional_functions.Button(200, 50, (11, 11), 'Меню', buttons, screen)
    buttons.update()
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if to_menu_button.rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    from menu import start
                    start()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and time.time() - time_0 > 0.25:
            break


def win(screen):
    global player, level_x, level_y
    time_0 = time.time()
    screen.fill(pygame.Color('black'))
    bg = pygame.transform.scale(additional_functions.load_image('win_menu.jpg', -1),
                                (settings.WIDTH, settings.HEIGHT))
    screen.blit(bg, (0, 0))
    levels = [additional_functions.Button(175, 50, (6 * i - 1, 3 * j), str((j - 1) * 3 + i), buttons, screen)
              for i in range(1, 4) for j in range(1, 5)]
    buttons.update()
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in levels:
                    if button.rect.collidepoint(event.pos):
                        settings.CURRENT_LEVEL = f'lvl{button.text}'
                        pygame.quit()
                        from main import game_loop
                        game_loop()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] and time.time() - time_0 > 0.25:
                break


all_sprites = pygame.sprite.Group()
spikes = pygame.sprite.Group()
walls = pygame.sprite.Group()
exits = pygame.sprite.Group()
player_group = pygame.sprite.Group()
mirror = pygame.sprite.Group()
balls = pygame.sprite.Group()
buttons = pygame.sprite.Group()


def game_loop():
    global left, right, main_mirror, stay, player, sum1, screen, ball_hit_sound, level
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()
    ball_hit_sound = pygame.mixer.Sound('data/ball_hit.wav')
    pygame.mixer.music.load('data/ambiance_loop.wav')
    pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
    ball_hit_sound.set_volume(settings.VOLUME)
    player, level_x, level_y, level = generate_level(additional_functions.load_level(f'{settings.CURRENT_LEVEL}.txt'))
    m_image = additional_functions.load_image('mim.jpg')
    main_mirror = Mirror(m_image)

    additional_functions.animation()
    time_from_last_esc = time.time() - 0.5

    left, right = False, False
    shift_pressed = False
    pygame.mixer.music.play(-1)
    sum1, stay = 0, 0

    while True:
        screen.fill(pygame.Color('aquamarine'))
        draw()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1 and player.ready_to_change_gravity:
                    sum1 += 1
                    player.change_gravity()
            elif e.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.KMOD_LSHIFT]:
                    shift_pressed = True
            elif e.type == pygame.KEYUP:
                if e.key == pygame.KMOD_LSHIFT:
                    shift_pressed = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] or \
                keys[pygame.K_d] and not keys[pygame.K_a]:
            stay = 1
            left = False
            right = True
            player.move(10, 0)
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] or \
                keys[pygame.K_a] and not keys[pygame.K_d]:
            stay = 0
            left = True
            right = False
            player.move(-10, 0)
        elif keys[pygame.K_ESCAPE] and time.time() - time_from_last_esc > 0.25:
            pause(screen)
            time_from_last_esc = time.time()
        else:
            left = False
            right = False

        all_sprites.update()
        mirror.draw(screen)
        for elem in player_group:
            res = elem.collide_with_sth()
            if res[0]:
                if res[1] in (Wall, Exit):
                    elem.rect.x += 10 if elem.rect.x <= TILE_SIZE else -10
                elif res[1] == Spike:
                    background_image = pygame.transform.scale(
                        additional_functions.load_image('death_screen.jpg'), (settings.WIDTH, settings.HEIGHT)
                    )
                    screen.fill(pygame.Color('black'))
                    screen.blit(background_image, (0, -150))
                    restart_button = additional_functions.Button(200, 50, (11, 9), 'Заново', buttons, screen)
                    exit_button = additional_functions.Button(200, 50, (11, 11), 'Выход', buttons, screen)
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if exit_button.rect.collidepoint(event.pos):
                                    from menu import start
                                    start()
                                elif restart_button.rect.collidepoint(event.pos):
                                    from main import game_loop
                                    game_loop()
                            elif event.type == pygame.MOUSEMOTION:
                                screen.fill(pygame.Color('black'))
                                rel = event.rel
                                screen.blit(background_image, (rel[0] * 0.2, rel[1] * 0.2 - 150))
                        buttons.update()
                        clock.tick(settings.FPS)
                        pygame.display.flip()
        for elem in balls:
            if elem.collide_with_sth(Exit)[0]:
                win(screen)
        if shift_pressed:
            clock.tick(30)
        else:
            clock.tick(settings.FPS)
        pygame.display.flip()


game_loop()
