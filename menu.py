import additional_functions
import settings
import pygame
import sys
import os

pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
buttons = pygame.sprite.Group()
clock = pygame.time.Clock()


def load_image(name, trans=0):
    full_name = os.path.join('data', name)
    image = pygame.image.load(full_name).convert()
    if trans is not None:
        if trans == -1:
            trans = image.get_at((0, 0))
        image.set_colorkey(trans)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    if is_exited:
        sys.exit()
    if settings_opened:
        pygame.quit()
        settings.settings_screen()
    else:
        pygame.quit()
        import main


background_image = pygame.transform.scale(load_image('bg.png'), (settings.WIDTH, settings.HEIGHT))
screen.blit(background_image, (0, 0))
is_exited = False
settings_opened = False


def start_screen():
    global is_exited, settings_opened
    start_button = additional_functions.Button(200, 50, (11, 5), 'Начать игру', buttons, screen)
    settings_button = additional_functions.Button(200, 50, (11, 7), 'Настройки', buttons, screen)
    exit_button = additional_functions.Button(200, 50, (11, 9), 'Выход', buttons, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    terminate()
                elif settings_button.rect.collidepoint(event.pos):
                    settings_opened = True
                    terminate()
                elif exit_button.rect.collidepoint(event.pos):
                    is_exited = True
                    terminate()
            elif event.type == pygame.MOUSEMOTION:
                rel = event.rel
                screen.blit(background_image, (rel[0] * 0.2, rel[1] * 0.2))
        buttons.update()
        pygame.display.flip()
        clock.tick(60)


start_screen()
