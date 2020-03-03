import additional_functions
import settings
import pygame
import sys


def start_menu(screen):
    pygame.init()
    buttons = pygame.sprite.Group()
    clock = pygame.time.Clock()

    background_image = pygame.transform.scale(additional_functions.load_image('bg.png'),
                                              (settings.WIDTH, settings.HEIGHT))
    screen.blit(background_image, (0, 0))
    is_exited = False
    settings_opened = False

    def terminate(set, exited):
        if set and exited:
            lvl_buttons = pygame.sprite.Group()
            screen.fill(pygame.Color('black'))
            bg = pygame.transform.scale(additional_functions.load_image('win_menu.jpg', -1),
                                        (settings.WIDTH, settings.HEIGHT))
            screen.blit(bg, (0, 0))
            levels = [additional_functions.Button(175, 50, (6 * i - 1, 3 * j), str((j - 1) * 3 + i), lvl_buttons, screen)
                      for i in range(1, 4) for j in range(1, 5)]
            lvl_buttons.update()
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for button in levels:
                            if button.rect.collidepoint(event.pos):
                                settings.CURRENT_LEVEL = f'lvl{button.text}'
                                return
        if exited:
            sys.exit()
        if set:
            return settings.settings_screen(screen)
        else:
            return

    def start_screen():
        global is_exited, settings_opened
        start_button = additional_functions.Button(200, 50, (11, 5), 'Продолжить игру', buttons, screen)
        settings_button = additional_functions.Button(200, 50, (11, 7), 'Настройки', buttons, screen)
        exit_button = additional_functions.Button(200, 50, (11, 9), 'Выход', buttons, screen)
        levels_button = additional_functions.Button(200, 50, (11, 3), 'Выбрать уровень', buttons, screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate(False, True)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.rect.collidepoint(event.pos):
                        return terminate(False, False)
                    elif settings_button.rect.collidepoint(event.pos):
                        settings_opened = True
                        return terminate(True, False)
                    elif exit_button.rect.collidepoint(event.pos):
                        is_exited = True
                        return terminate(False, True)
                    elif levels_button.rect.collidepoint(event.pos):
                        return terminate(True, True)
                elif event.type == pygame.MOUSEMOTION:
                    rel = event.rel
                    screen.blit(background_image, (rel[0] * 0.2, rel[1] * 0.2))
            buttons.update()
            pygame.display.flip()
            clock.tick(60)

    return start_screen()
