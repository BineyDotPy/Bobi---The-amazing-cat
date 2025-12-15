import pygame
from settings import SPRITE_SIZE,SCREEN_HEIGHT,SCREEN_WIDTH


class Bush(pygame.sprite.Sprite):
    def __init__(self,pos,size = (100,100)):
        super().__init__()
        self.image = pygame.image.load("assets/bush.png").convert_alpha()
        self.rect = self. image.get_rect(center=pos)
        self.hide_zone = self.rect.inflate(20,20)
        self.hide_zone.x += 40
        self.hide_zone.y += 40
        self.image = pygame.transform.scale(self.image, size)
    def is_hidden(self, bushes):
        return any(bush.hide_zone.colliderect(self.collision_rect) for bush in bushes)
    def draw_hitbox(self, surface):
        #sprawdzanie hitboxów krzaka
        pygame.draw.rect(surface, (255, 0, 0), self.hide_zone, 2)
    
