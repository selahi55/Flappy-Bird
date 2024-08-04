import pygame
import time
from utils import load_image, HEIGHT, WIDTH
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self, game, color):
        super().__init__()
        self.game = game
        self.color = color

        # Idle, DownFlap, UpFlap
        if self.color == 'blue':
            self.frames = [load_image("bluebird-midflap.png"), load_image('bluebird-downflap.png'),
                           load_image('bluebird-upflap.png')]
        elif self.color == 'red':
            self.frames = [load_image("redbird-midflap.png"), load_image('redbird-downflap.png'), 
                           load_image('redbird-upflap.png')]
        else:
            self.frames = [load_image('yellowbird-midflap.png'), load_image('yellowbird-downflap.png'),
                           load_image('yellowbird-upflap.png')]
            
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(50, HEIGHT // 2))
        self.player_mask = pygame.mask.from_surface(self.image)
        self.gravity = 0 
        self.flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
        self.press = False

    def player_input(self):
        if self.press and self.rect.y > 30:
            self.gravity = -13
            self.animation_index = 1 
            self.flap_sound.play()       
            self.press = False 

    def flap_animation(self):
        if self.rect.bottom < self.game.ground_rect.top:
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
        else:
            self.image = self.frames[0]

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > self.game.ground_rect.top:
            self.rect.bottom = self.game.ground_rect.top

    def update(self):
        self.player_input()
        self.flap_animation()
        self.apply_gravity()

# Functionality for Speed of Pipe?
class Pipe(pygame.sprite.Sprite):
    def __init__(self, game, color, upside_down=False):
        super().__init__()
        self.game = game
        self.color = color

        #52 x 320
        if color == 'green':
            self.image = load_image('pipe-green.png')
        else:
            self.image = load_image('pipe-red.png')
        self.pipe_mask = pygame.mask.from_surface(self.image)

        if upside_down:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(center=(500, 512))
        else:
            self.rect = self.image.get_rect(center=(500, 512))

    def move(self):
        self.rect.centerx -= 2
        offset_x = self.game.player.rect.x-self.rect.x
        offset_y = self.game.player.rect.y - self.rect.y
        if self.pipe_mask.overlap(self.game.player.player_mask, (offset_x, offset_y)):
            self.game.game_active = False
            self.game.pipes.empty()
            self.game.dying_sound.play()
        if self.rect.centerx < -100:
            self.kill()

    def update(self):
        self.move()
