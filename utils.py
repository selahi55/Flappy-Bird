import pygame, os

BASE_DIR = 'assets/sprites/'
WIDTH = 336
HEIGHT = 624

def load_image(path):
    image = pygame.image.load(BASE_DIR + path).convert_alpha()
    return image