import pygame

pygame.init()
display = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

green = (0, 240, 0)
blue = (38, 123, 218)


def get_image(sheet, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image


stay_sprites = pygame.image.load('Sprites/player/sonic_stay.png').convert_alpha()
walk_sprites = pygame.image.load('Sprites/player/sonic_walk.png').convert_alpha()
jump_sprites = pygame.image.load('Sprites/player/sonic_jump.png').convert_alpha()
slow_sprites = pygame.image.load('Sprites/player/sonic_slow_run.png').convert_alpha()
fast_sprites = pygame.image.load('Sprites/player/sonic_fast_run.png').convert_alpha()
ring_sprites = pygame.image.load('Sprites/objects/ring.png').convert_alpha()
win_sprites = pygame.image.load('Sprites/player/winner_transform.png').convert_alpha()
flew_away_sprites = pygame.image.load('Sprites/player/winner_flew_away.png').convert_alpha()

stay_animation_steps = []
for x in range(20):
    stay_animation_steps.append(get_image(stay_sprites, x, 39, 39, 1.5, green))

walk_animation_steps = []
for x in range(10):
    walk_animation_steps.append(get_image(walk_sprites, x, 39, 39, 1.5, green))

jump_animation_steps = []
for x in range(8):
    jump_animation_steps.append(get_image(jump_sprites, x, 39, 39, 1.5, green))

slow_animation_steps = []
for x in range(8):
    slow_animation_steps.append(get_image(slow_sprites, x, 39, 39, 1.5, green))

fast_animation_steps = []
for x in range(4):
    fast_animation_steps.append(get_image(fast_sprites, x, 39, 39, 1.5, green))

ring_animation_steps = []
for x in range(16):
    ring_animation_steps.append(get_image(ring_sprites, x, 16, 16, 2, blue))

gif1_animation_steps = []
for x in range(14):
    gif1_animation_steps.append(pygame.image.load(f'Sprites/out_of_work1/{x}.gif'))

gif2_animation_steps = []
for x in range(16):
    gif2_animation_steps.append(pygame.image.load(f'Sprites/out_of_work2/{x}.gif'))

win_animation_steps = []
for x in range(19):
    win_animation_steps.append(get_image(win_sprites, x, 48, 53, 1.5, green))

flew_away_animation_steps = []
for x in range(6):
    flew_away_animation_steps.append(get_image(flew_away_sprites, x, 48, 48, 1.5, green))