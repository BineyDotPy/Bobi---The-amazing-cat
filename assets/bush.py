import pygame
from settings import SPRITE_SIZE,SCREEN_HEIGHT,SCREEN_WIDTH


class Bush(pygame.sprite.Sprite):
    def __init__(self,pos,size = (100,100)):
        super().__init__()
        self.image = pygame.image.load("assets/bush.png").convert_alpha()
        self.rect = self. image.get_rect(center=pos)
        self.hide_zone = self.rect.inflate(-5,-5)
        self.hide_zone.x += 30
        self.hide_zone.y += 10
        self.image = pygame.transform.scale(self.image, size)
    def is_hidden(self, bushes):
        return any(bush.hide_zone.colliderect(self.collision_rect) for bush in bushes)
    
