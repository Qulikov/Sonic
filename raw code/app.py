from objects import player, rings_list, particles, spikes_list, emeralds, Button, gif1, gif2
from constants import *
import os
import sounds

os.environ['SDL_VIDEO_CENTERED'] = '1'

mixer_working = False


def play():
    pygame.mixer_music.load('Sounds/Music/Bg_music.mp3')
    pygame.mixer_music.play(10)

    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    scene = pygame.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    bg = pygame.image.load('Sprites/background.png').convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    paused = False

    is_running = True
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.constants.K_a:
                player.left = True
            if event.type == pygame.KEYUP and event.key == pygame.constants.K_a:
                player.left = False

            if event.type == pygame.KEYDOWN and event.key == pygame.constants.K_d:
                player.right = True
            if event.type == pygame.KEYUP and event.key == pygame.constants.K_d:
                player.right = False

            if event.type == pygame.KEYDOWN and event.key == pygame.constants.K_SPACE:
                player.up = True
                pygame.mixer.Sound(sounds.jump_sound).play()
            if event.type == pygame.KEYUP and event.key == pygame.constants.K_SPACE:
                player.up = False

            if event.type == pygame.KEYDOWN and event.key == pygame.constants.K_ESCAPE:
                pygame.mixer_music.stop()
                is_running = False
                menu()

            if event.type == pygame.KEYDOWN and event.key == pygame.constants.K_p:
                if paused:
                    pygame.mixer_music.unpause()
                    paused = False
                else:
                    pygame.mixer_music.pause()
                    paused = True

        if player.rect.top > HEIGHT * 1.3 or player.rect.right > WIDTH * 1.1:
            is_running = False

        score = score_font.render(f'SCORE: {player.score}', False, (250, 200, 0))

        scene.blit(bg, (0, 0))
        scene.blit(score, (10, 10))

        scene.blit(player.image, player.rect)
        player.update()
        if not player.win:
            scene.blit(emeralds.image, emeralds.rect)
            if player.score == 20:
                for s in spikes_list:
                    s.kill()
                emeralds.update()

        particles.emit(scene)

        rings_list.draw(scene)
        rings_list.update()

        if player.score < 20:
            spikes_list.draw(scene)
            spikes_list.update()

        display.blit(scene, (0, 0))
        pygame.display.update()

    pygame.quit()


def menu():
    global mixer_working
    if not mixer_working:
        pygame.mixer_music.load('Sounds/Music/Menu_Theme.mp3')
        pygame.mixer_music.play()

    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Menu')
    scene = pygame.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    bg = pygame.image.load('Sprites/menu_bg.png').convert()

    start = Button((640, 300), (585, 100), 'START', menu_font, (255, 255, 255), (100, 150, 250))
    settings = Button((640, 450), (585, 100), 'Settings', menu_font, (255, 255, 255), (100, 150, 250))
    exit_button = Button((640, 600), (585, 100), 'QUIT', menu_font, (255, 255, 255), (100, 150, 250))

    is_running = True
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.checkForInput(pygame.mouse.get_pos()):
                    pygame.mixer.Sound(sounds.button_sound).play()
                    pygame.time.delay(500)
                    pygame.mixer_music.stop()
                    is_running = False
                    play()

                if settings.checkForInput(pygame.mouse.get_pos()):
                    mixer_working = True
                    pygame.mixer.Sound(sounds.button_sound).play()
                    pygame.time.delay(500)
                    set_screen()

                if exit_button.checkForInput(pygame.mouse.get_pos()):
                    pygame.mixer.Sound(sounds.button_sound).play()
                    pygame.time.delay(500)
                    is_running = False

        scene.blit(bg, (0, 0))

        start.changeColor(pygame.mouse.get_pos())
        start.update(scene)

        settings.changeColor(pygame.mouse.get_pos())
        settings.update(scene)

        exit_button.changeColor(pygame.mouse.get_pos())
        exit_button.update(scene)

        display.blit(scene, (0, 0))
        pygame.display.update()

    pygame.quit()


def set_screen():
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Settings')
    scene = pygame.Surface((WIDTH, HEIGHT))

    bg = pygame.image.load('Sprites/set_bg.png'). convert()

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 16 <= pygame.mouse.get_pos()[0] <= 167 and 25 <= pygame.mouse.get_pos()[1] <= 101:
                    pygame.mixer.Sound(sounds.button_sound).play()
                    pygame.time.delay(500)
                    is_running = False
                    menu()

        scene.blit(bg, (0, 0))
        scene.blit(gif1.image, gif1.rect)
        scene.blit(gif2.image, gif2.rect)

        gif1.update()
        gif2.update()

        display.blit(scene, (0, 0))
        pygame.display.update()

    pygame.quit()


menu()
