import pygame
from settings import SPRITE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, distance
from random import random, choice
import bush

SPRITE_SIZE = 64

def load_husky_animation(row, num_frames, scale=(128,128)):
    sheet = pygame.image.load('assets/husky.png').convert_alpha()
    frames = []
    for i in range(num_frames):
        frame_rect = pygame.Rect(i*SPRITE_SIZE, row*SPRITE_SIZE, SPRITE_SIZE,SPRITE_SIZE)
        frame = sheet.subsurface(frame_rect)
        frame = pygame.transform.scale(frame,scale)
        frames.append(frame)
    return frames

class Husky(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()

        self.animations = {
            'up': load_husky_animation(0,8),
            'down': load_husky_animation(0,8),
            'right': load_husky_animation(0,8),
            "left": [pygame.transform.flip(frame, True, False) for frame in load_husky_animation(0, 8)],
        }

        self.direction = 'down'
        self.image = self.animations[self.direction][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = self.rect.inflate(-64, -64)

        self.speed = 4  
        self.frame_index = 0

        self.change_direction_time = pygame.time.get_ticks()
        self.direction_change_interval = 2000  # Co 2 sekundy zmiana kierunku

    def change_direction(self):
        """Losowo zmienia kierunek poruszania się"""
        directions = ["down", "left", "up", "right"]
        self.direction = choice(directions)

    def find_player(self, player_pos,player, bushes):
        if player.is_hidden(bushes) == False:
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery

            if abs(dx) <= distance and abs(dy) <= distance:
                if abs(dx) > abs(dy):
                    self.direction = 'right' if dx > 0 else 'left'
                else:
                    self.direction = 'down' if dy > 0 else 'up'



    def update(self, player, bushes):
        current_time = pygame.time.get_ticks()

        # Spróbuj znaleźć gracza, ale tylko jeśli NIE jest ukryty
        self.find_player(player.rect.center, player, bushes)

        # Losowa zmiana kierunku, jeśli nie śledzi gracza
        if current_time - self.change_direction_time > self.direction_change_interval:
            self.change_direction_time = current_time
            self.change_direction()

        # Poruszanie się
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        """
        # Przeskocz na drugą str
        if self.rect.right < -15:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH+15:
            self.rect.right = 0
        if self.rect.bottom < -15:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT+15:
            self.rect.bottom = 0
        """
         # Blokowanie ruchu poza ekran
        if self.rect.left < -SPRITE_SIZE:
            self.rect.left = -SPRITE_SIZE
        elif self.rect.right > SCREEN_WIDTH + SPRITE_SIZE:
            self.rect.right = SCREEN_WIDTH + SPRITE_SIZE

        if self.rect.top < -SPRITE_SIZE:
            self.rect.top = -SPRITE_SIZE
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.collision_rect.center = self.rect.center

        # Animacja
        self.frame_index += 0.3
        if self.frame_index >= len(self.animations[self.direction]):
            self.frame_index = 0
        self.image = self.animations[self.direction][int(self.frame_index)]