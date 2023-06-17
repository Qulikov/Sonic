import os
import random, sprites

import pygame.sprite

import sounds
from constants import *

lefts = []
rights = []
tops = []
bottoms = []


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.images = []
        for image in sprites.walk_animation_steps:
            self.images.append(image)
        for image in sprites.slow_animation_steps:
            self.images.append(image)
        for image in sprites.fast_animation_steps:
            self.images.append(image)
        for image in sprites.jump_animation_steps:
            self.images.append(image)

        self.image_index = 0
        self.image = self.images[self.image_index]
        self.stay_images = []

        self.default_image = pygame.image.load('Sprites/player/sonic_default.png')
        self.default_image.set_colorkey(sprites.green)
        self.default_image = pygame.transform.scale(self.default_image, (self.default_image.get_size()[0] * 1.5, self.default_image.get_size()[1] * 1.5))

        self.stay_images.append(self.default_image)
        for image in sprites.stay_animation_steps:
            self.stay_images.append(image)

        self.fall_image = pygame.image.load('Sprites/player/sonic_fall.png')
        self.fall_image.set_colorkey(sprites.green)
        self.fall_image = pygame.transform.scale(self.fall_image, (self.fall_image.get_size()[0] * 1.5, self.fall_image.get_size()[1] * 1.5))

        self.death_image = pygame.image.load('Sprites/player/sonic_death.png')
        self.death_image.set_colorkey(sprites.green)
        self.death_image = pygame.transform.scale(self.death_image, (self.death_image.get_size()[0] * 1.5, self.death_image.get_size()[1] * 1.5))

        self.winner_tr = []
        for image in sprites.win_animation_steps:
            self.winner_tr.append(image)

        self.winner_fa = []
        for image in sprites.flew_away_animation_steps:
            self.winner_fa.append(image)

        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2 + 150, 39, 39)

        self.xvel = 0
        self.yvel = 0

        self.player_speed = 7
        self.boost = 0
        self.player_jump_strength = 10
        self.score = 0
        self.pr_s = 0

        self.left = self.right = False
        self.up = False
        self.is_walk = False
        self.stay_indexation = True
        self.staying = 0
        self.on_ground = False

        self.s_cd = -1000
        self.is_hit = False
        self.left_hit = False
        self.right_hit = False

        self.death = False
        self.d_cd = 0

        self.win = False

    def update(self):
        if not self.win:
            if not self.death:
                if self.is_hit:
                    self.staying = 0
                    if not self.on_ground:
                        if self.left_hit:
                            self.left = True
                        if self.right_hit:
                            self.right = True
                        self.image = self.fall_image
                        if self.pr_s > 0:
                            self.pr_s -= 1
                            r = Ring(self.rect.x, self.rect.y)
                            rings_list.add(r)
                            r.on_ground = False
                        for i in range(7):
                            if (rights[i] > self.rect.right >= lefts[i] or rights[i] >= self.rect.left > lefts[
                                i]) and self.rect.top > tops[i]:
                                self.left = False
                                self.right = False
                                self.left_hit = False
                                self.right_hit = False
                    else:
                        self.is_hit = False
                        self.left = False
                        self.right = False
                        self.left_hit = False
                        self.right_hit = False

                else:
                    if not self.is_walk and not self.on_ground:
                        self.staying = 0
                        if self.image_index < 22:
                            self.image_index = 22

                        self.image_index += 0.6
                        if self.image_index >= 30:
                            self.image_index = 22

                        self.image = self.images[int(self.image_index)]

                    elif self.is_walk and not self.on_ground:
                        self.staying = 0
                        if self.image_index < 22:
                            self.image_index = 22

                        self.image_index += 0.4
                        if self.image_index >= 30:
                            self.image_index = 22

                        self.image = self.images[int(self.image_index)]

                    elif self.is_walk and self.on_ground:
                        self.staying = 0

                        if self.boost <= 15:
                            self.boost += 0.05

                        if self.boost <= 5:
                            self.image_index += 0.2
                            if self.image_index >= 10:
                                self.image_index = 0

                        if 5 < self.boost <= 10:
                            self.image_index += 0.3
                            if 18 <= self.image_index or self.image_index < 10:
                                self.image_index = 10

                        if 10 < self.boost:
                            self.image_index += 0.4
                            if 22 <= self.image_index or self.image_index < 18:
                                self.image_index = 18

                        self.image = self.images[int(self.image_index)]
                    elif self.on_ground and not self.is_walk:
                        self.staying += 1

                        if self.staying >= 300 and self.image in self.stay_images:
                            if self.stay_indexation:
                                self.image_index += 0.2

                            elif not self.stay_indexation:
                                self.image_index -= 0.2

                            if self.image_index >= len(self.stay_images) - 1.1:
                                self.stay_indexation = False

                            if self.image_index <= 1 and not self.stay_indexation:
                                self.stay_indexation = True
                                self.staying = 0
                                self.image_index = 0

                            self.image = self.stay_images[int(self.image_index)]

                        else:
                            self.image_index = 0
                            self.image = self.stay_images[self.image_index]

                        self.boost = 0

                if self.left:
                    self.xvel = -self.player_speed - self.boost
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.image.set_colorkey(sprites.green)
                    self.is_walk = True

                elif self.right:
                    self.xvel = self.player_speed + self.boost
                    self.is_walk = True

                elif not self.left and not self.right:
                    self.xvel = 0
                    self.is_walk = False

                if self.on_ground:
                    if self.up:
                        self.yvel = -self.player_jump_strength
                        self.on_ground = False
                    else:
                        self.yvel = 0
                else:
                    self.yvel += GRAVITY

                if self.rect.right > WIDTH:
                    self.rect.right = WIDTH
                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.top >= HEIGHT:
                    self.rect.bottom = 0

                self.rect.y += self.yvel
                self.collide(0, self.yvel, platforms_list)

                self.rect.x += self.xvel
                self.collide(self.xvel, 0, platforms_list)

            else:
                self.image = self.death_image
                if pygame.time.get_ticks() - self.d_cd < 1000:
                    self.rect.y -= 0
                else:
                    pygame.mixer.Sound(sounds.death_sound).play()
                    self.rect.y += 10

        else:
            self.image_index += 0.3
            if self.image_index >= len(self.winner_tr):
                pygame.mixer.Sound(sounds.flew_away_sound).play()
                if self.image_index >= len(self.winner_tr) + len(self.winner_fa):
                    self.image_index = len(self.winner_tr)
                self.image = self.winner_fa[int(self.image_index - len(self.winner_tr))]
                self.rect.x += 15
            else:
                self.image = self.winner_tr[int(self.image_index)]

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.yvel = 0

        for r in rings_list:
            if pygame.sprite.collide_rect(self, r) and pygame.time.get_ticks() - self.s_cd >= 1000:
                particles.add_particles(r.rect.x, r.rect.y)
                pygame.mixer.Sound(sounds.ring_sound).play()
                r.kill()
                rings_list.remove(r)
                self.score += 1

        for s in spikes_list:
            if pygame.sprite.collide_rect(self, s) and pygame.time.get_ticks() - self.s_cd >= 1000:
                if self.score > 0:
                    self.pr_s = self.score
                    if self.score > 5:
                        self.score -= 5
                    else:
                        self.score = 0
                    pygame.mixer.Sound(sounds.ring_lose_sound).play()
                    self.pr_s -= self.score
                    self.rect.y -= 1
                    self.yvel = -10
                    self.s_cd = pygame.time.get_ticks()
                    self.is_hit = True
                    if s.rect.right >= self.rect.right >= s.rect.left:
                        self.left_hit = True
                        self.right_hit = False
                    if s.rect.left <= self.rect.left <= s.rect.right:
                        self.right_hit = True
                        self.left_hit = False
                else:
                    self.death = True
                    self.d_cd = pygame.time.get_ticks()

        if pygame.sprite.collide_rect(self, emeralds):
            emeralds.kill()
            self.win = True
            self.image_index = 0

        k = 0
        for i in range(7):
            if lefts[i] <= self.rect.right and self.rect.left < rights[i] and tops[i] == self.rect.bottom:
                k += 1
        if k:
            self.on_ground = True
        else:
            self.on_ground = False


player = Player()


class Platform(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(Platform, self).__init__()
        self.rect = pygame.Rect(rect)


platforms_list = [Platform((0, 610, WIDTH, 10)),
                  Platform((551, 493, 175, 40)),
                  Platform((226, 403, 163, 40)), Platform((880, 403, 163, 40)),
                  Platform((487, 298, 311, 40)),
                  Platform((116, 172, 163, 40)), Platform((1000, 172, 163, 40))]

for i in platforms_list:
    lefts.append(i.rect.left)
    rights.append(i.rect.right)
    tops.append(i.rect.top)
    bottoms.append(i.rect.bottom)


class Ring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Ring, self).__init__()
        self.images = []
        for image in sprites.ring_animation_steps:
            self.images.append(image)
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = pygame.Rect(x - 16, y - 16, 32, 32)

        self.on_ground = True

    def update(self):
        self.image_index += 0.6
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[int(self.image_index)]

        if not self.on_ground:
            self.rect.y += 3

            k = 0
            for i in range(7):
                if lefts[i] <= self.rect.right and self.rect.left < rights[i] and tops[i] <= self.rect.bottom < bottoms[i]:
                    k += 1
            if k:
                self.on_ground = True
            else:
                self.on_ground = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)


rings = [Ring(640, 230), Ring(605, 230), Ring(570, 230), Ring(675, 230), Ring(710, 230),
         Ring(640, 425), Ring(605, 425), Ring(675, 425),
         Ring(1080, 105), Ring(1045, 105), Ring(1115, 105),
         Ring(200, 105), Ring(165, 105), Ring(235, 105),
         Ring(312, 340), Ring(277, 340), Ring(347, 340),
         Ring(956, 340), Ring(921, 340), Ring(991, 340)]

rings_list = pygame.sprite.Group()
for r in rings:
    rings_list.add(r)


class ParticlePrinciple:
    def __init__(self):
        self.particles = []
        self.size = 5

    def emit(self, screen):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                if pygame.time.get_ticks() - particle[3] < 100:
                    particle[0][0] += particle[2][0]
                    particle[0][1] += particle[2][1]
                    c = particle[0].center
                    pygame.draw.rect(screen, particle[1], particle[0])
                    pygame.draw.polygon(screen, particle[1], (
                    (c[0], c[1] + self.size // 2 ** (1 / 2)), (c[0] - self.size // 2 ** (1 / 2), c[1]),
                    (c[0], c[1] - self.size // 2 ** (1 / 2)), (c[0] + self.size // 2 ** (1 / 2), c[1])))

    def add_particles(self, x, y):
        pos_x = x
        pos_y = y
        direction_x = random.randint(-5, 5)
        direction_y = random.randint(-5, 5)
        particle_rect = pygame.Rect(pos_x - self.size / 2, pos_y - self.size / 2, self.size, self.size)

        self.particles.append((particle_rect, (240, 240, 0), (direction_x, direction_y), pygame.time.get_ticks()))

    def delete_particles(self):
        particles_copy = [particle for particle in self.particles if particle[0].x > 0]
        self.particles = particles_copy


particles = ParticlePrinciple()


class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super(Spikes, self).__init__()
        self.angle = angle
        self.xvel = 0
        self.image = pygame.image.load('Sprites/objects/spikes.png')
        self.image.set_colorkey((38, 123, 218))
        self.image = pygame.transform.rotozoom(self.image, self.angle, 1.5)
        self.rect = pygame.Rect(x, y, 48, 48)

    def update(self):
        if self.angle == 90:
            self.xvel -= 0.15
            if self.rect.right <= 0:
                self.xvel = 0
                self.rect.right = -48
                self.image = pygame.transform.rotate(self.image, 180)
                self.angle = 270
        if self.angle == 270:
            self.xvel += 0.15
            if self.rect.left >= WIDTH:
                self.xvel = 0
                self.rect.right = 1328
                self.image = pygame.transform.rotate(self.image, 180)
                self.angle = 90
        self.rect.x += self.xvel


spikes = [Spikes(-48, 100, 270), Spikes(-48, 250, 270), Spikes(-48, 400, 270), Spikes(-48, 550, 270),
          Spikes(1328, 100, 90), Spikes(1328, 250, 90), Spikes(1328, 400, 90), Spikes(1328, 550, 90)]

spikes_list = pygame.sprite.Group()
for s in spikes:
    spikes_list.add(s)


class Emeralds(pygame.sprite.Sprite):
    def __init__(self):
        super(Emeralds, self).__init__()
        self.image = pygame.image.load('Sprites/objects/emeralds.png')
        self.image.set_colorkey(sprites.blue)
        self.image = pygame.transform.scale(self.image, (140, 105))
        self.rect = self.image.get_rect(center=(640, -105))

    def update(self):
        if self.rect.y < 50:
            self.rect.y += 2


emeralds = Emeralds()


class Button:
    def __init__(self, pos, size, text_input, font, base_color, hovering_color):
        self.image = pygame.image.load('Sprites/objects/button_bg.png')
        self.image = pygame.transform.scale(self.image, size)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos + 10, self.y_pos - 30))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Gif:
    def __init__(self, path, x, y, size, colour):
        self.images = []
        self.image_index = 0
        for image in path:
            image.set_colorkey(colour)
            image = pygame.transform.scale(image, size)
            self.images.append(image)
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.image_index += 0.1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[int(self.image_index)]


gif1 = Gif(sprites.gif1_animation_steps, 1000, 200, (256, 320), (254, 254, 254))
gif2 = Gif(sprites.gif2_animation_steps, 400, 200, (200, 200), (255, 255, 255))
