import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from player import load_animation


def load_animation(start_frame, end_frame, sprite_path, frame_size,scale_to = None):
    sheet = pygame.image.load(sprite_path).convert_alpha()
    frames = []
    for i in range(start_frame, end_frame + 1):
        rect = pygame.Rect(i * frame_size[0], 0, *frame_size)
        frame = sheet.subsurface(rect)
        if scale_to:
            frame = pygame.transform.scale(frame, scale_to)
        frames.append(frame)
        
    return frames



class AnimatedPoint(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_path, frame_size, frame_count, anim_speed,scale_to):
        super().__init__()
        self.animation = load_animation(0, frame_count - 1, sprite_path, frame_size,scale_to)
        self.frame_index = 0
        self.anim_speed = anim_speed
        self.image = self.animation[0]
        self.rect = self.image.get_rect(center=pos)
        self.collision_rect = self.rect.inflate(-16, -16)
        self.collision_rect.center = self.rect.center

    def update(self, *args):
        self.frame_index += self.anim_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]


class Speed_Point(AnimatedPoint):
    def __init__(self, pos):
        super().__init__(pos, "assets/mleko1.png", (64, 64), 5, 0.08,scale_to=(64, 64))

class Default_Point(AnimatedPoint):
    def __init__(self, pos):
        super().__init__(pos, "assets/ryba.png", (64, 64), 5, 0.15,scale_to=(64, 64))


class pilka(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        sprite = "assets/pilka1.png"
        self.animation = {
            'ball': load_animation(0, 4, sprite, (32, 32),(40,50)) 
        }
        self.frame_index = 0  # Inicjalizacja frame_index
        self.image = self.animation['ball'][self.frame_index]  # Ustawienie początkowej klatki
        self.rect = self.image.get_rect(center=pos)
        self.collision_rect = self.rect.inflate(-16, -16)
        self.collision_rect.center = self.rect.center

    def update(self, *args):
        self.frame_index += 0.15  # Zwiększanie indexu dla animacji
        if self.frame_index >= len(self.animation['ball']):
            self.frame_index = 0  # Reset indexu animacji po ostatniej klatce
        self.image = self.animation['ball'][int(self.frame_index)]  # Aktualizacja obrazu

            
def spawn_point(group, all_sprites, cls):
    x = random.randint(100, SCREEN_WIDTH - 100)
    y = random.randint(100, SCREEN_HEIGHT - 100)
    point = cls((x, y))
    group.add(point)
    all_sprites.add(point)



#stara wersja - osobne klasy

'''
def load_animation(row, num_frames,sprite, scale):
    sheet = pygame.image.load(sprite).convert_alpha() 
    frames = []
    SPRITE_SIZE = 64
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * SPRITE_SIZE, row * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
        frame = pygame.transform.scale(frame, scale)
        frames.append(frame)
    return frames
'''

'''
class Speed_Point(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        sprite = "assets/mleko1.png"
        self.animation = {
            'milk' : load_animation(0,5,sprite,(65, 65))
        }
        #self.image = pygame.Surface((32, 32))
        #self.image.fill((255, 200, 0))
        self.frame_index = 0 
        self.image = self.animation['milk'][0]
        self.rect = self.image.get_rect(center=pos)
        self.collision_rect = self.rect.inflate(-16, -16)  
        self.collision_rect.center = self.rect.center

    def update(self, *args):
        self.frame_index += 0.08
        if self.frame_index >= len(self.animation['milk']):
            self.frame_index = 0
        self.image = self.animation['milk'][int(self.frame_index)]


class Default_Point(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        sprite = "assets/ryba.png"
        self.animation = {
            'fish' : load_animation(0,5,sprite,(55,55))
        }
        #self.image = pygame.Surface((32, 32))
        #self.image.fill((255, 200, 0))
        self.frame_index = 0 
        self.image = self.animation['fish'][int(random.random() * 5)]
        self.rect = self.image.get_rect(center=pos)
        self.collision_rect = self.rect.inflate(-16, -16)  
        self.collision_rect.center = self.rect.center

    def update(self, *args):
        self.frame_index += 0.15
        if self.frame_index >= len(self.animation['fish']):
            self.frame_index = 0
        self.image = self.animation['fish'][int(self.frame_index)]

'''