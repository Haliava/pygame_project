import pygame
import additional_functions
import sys

FPS = 60
WIDTH = 1300
HEIGHT = 750
VOLUME = 0.01
MUSIC_VOLUME = 0.3
TILE_SIZE = 50
CURRENT_LEVEL = 'lvl2'
LEVELS = ['lvl1', 'lvl2', 'lvl3', 'lvl4', 'lvl5']

boxes_group = pygame.sprite.Group()


class InputBox(pygame.sprite.Sprite):
    """Создать поле - прямоугольник, который ожидает ввода пользователя
        w - ширина поля в px
        h - высота поля в px
        cords - координаты поля в клетках поля, размером TILE_SIZE
        text - текст, расположенный на поле

    """
    def __init__(self, w, h, coords, text, corresponding_setting):
        super().__init__(boxes_group)
        self.color_active = pygame.Color('dodgerblue2')
        self.color_inactive = pygame.Color('lightskyblue3')
        self.font = pygame.font.Font(None, 25)
        self.rect = pygame.Rect(coords[0] * TILE_SIZE, coords[1] * TILE_SIZE, w, h)
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.corresponding_setting = corresponding_setting
        self.active = False

    def handle_event(self, event):
        global TILE_SIZE, WIDTH, HEIGHT, VOLUME, MUSIC_VOLUME, FPS
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    try:
                        if self.corresponding_setting == 'VOLUME':
                            VOLUME = float(self.text)
                        elif self.corresponding_setting == 'MUSIC_VOLUME':
                            MUSIC_VOLUME = float(self.text)
                        elif self.corresponding_setting == 'FPS':
                            FPS = int(self.text)
                    except ValueError:
                        self.text = 'Ошибка'
                elif event.key == pygame.K_BACKSPACE:
                    print(123)
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 15))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def settings_screen():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    buttons = pygame.sprite.Group()
    clock = pygame.time.Clock()
    background_image = pygame.transform.scale(additional_functions.load_image('bg.png'), (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))

    back_to_menu = additional_functions.Button(200, 50, (1, 13), 'Вернуться к меню', buttons, screen)
    fps_box = InputBox(200, 50, (11, 7), 'FPS', 'VOLUME')
    music_box = InputBox(200, 50, (11, 9), 'Громкость музыки', 'MUSIC_VOLUME')
    volume_box = InputBox(200, 50, (11, 11), 'Громкость звуков', 'VOLUME')
    boxes_group.add(music_box)
    boxes_group.add(volume_box)
    boxes = [volume_box, music_box, fps_box]

    def render_info_text():
        intro_text = ['Настройки:', '',
                      'Нажмите enter для сохранения изменений поля', '',
                      'Громкость изменяется от 0.0 до 1.0', ''
                      '* Изменения вступят в силу при выходе из экрана настроек']
        font = pygame.font.Font(None, 25)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    for box in boxes:
        box.draw(screen)

    render_info_text()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_menu.rect.collidepoint(event.pos):
                    from menu import start
                    start()
            elif event.type == pygame.MOUSEMOTION:
                rel = event.rel
                screen.blit(background_image, (rel[0] * 0.2, rel[1] * 0.2))
                render_info_text()
            for box in boxes:
                box.draw(screen)
            for box in boxes:
                box.handle_event(event)
        boxes_group.update()
        buttons.update()

        clock.tick(60)
        pygame.display.flip()
