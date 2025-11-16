import pygame
from modules.utils import cfg

class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = 0
        self.imagpaths = cfg.SKIER_IMAGE_PATH[:-1]
        self.image = pygame.image.load(self.imagpaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.speed = [self.direction, 6 - abs(self.direction) * 2]
        self.lives = 3

    def turn(self, num):
        self.direction += num
        self.direction = max(-2, self.direction)
        self.direction = min(2, self.direction)
        center = self.rect.center
        self.image = pygame.image.load(self.imagpaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = [self.direction, 6 - abs(self.direction) * 2]
        return self.speed

    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centerx = max(20, self.rect.centerx)
        self.rect.centerx = min(620, self.rect.centerx)

    def setFall(self):
        self.image = pygame.image.load(cfg.SKIER_IMAGE_PATH[-1])

    def setForward(self):
        self.direction = 0
        self.image = pygame.image.load(self.imagpaths[self.direction])
        self.speed = [self.direction, 6 - abs(self.direction) * 2]
