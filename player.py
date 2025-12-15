import pygame
from settings import SPRITE_SIZE, SCREEN_WIDTH,SCREEN_HEIGHT

def load_animation(row, num_frames, scale=(90, 90)):
    sheet = pygame.image.load("assets/Cat Sprite Sheet.png").convert_alpha() 
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * SPRITE_SIZE, row * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
        frame = pygame.transform.scale(frame, scale)
        frames.append(frame)
    return frames

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.animations = {
            "down": load_animation(4, 6),
            "down_rotate": [pygame.transform.flip(frame, True, False) for frame in load_animation(4, 6)],
            "right": load_animation(5, 6),
            "left": [pygame.transform.flip(frame, True, False) for frame in load_animation(5, 6)],
            "take": load_animation(7, 6),
        }

        self.direction = 'down'
        self.image = self.animations[self.direction][0]
        self.rect = self.image.get_rect(topleft=pos)
        
        self.collision_rect = self.rect.inflate(-20, -30)
        self.collision_rect.x += 15

        self.normal_speed = 5
        self.speed = self.normal_speed
        self.left_click = False

        self.boost_speed = 9
        self.boost_active = False
        self.boost_time = 0

        self.points = 0
        self.frame_index = 0

    def active_boost(self):
        self.boost_active = True
        self.boost_start_time = pygame.time.get_ticks()
        self.speed = self.boost_speed

    def add_point(self):
        self.points += 1

    def is_hidden(self, bushes):
        return any(bush.hide_zone.colliderect(self.collision_rect) for bush in bushes)

    def draw_hitbox(self, surface):
        #sprawdzanie hitboxów postaci
        pygame.draw.rect(surface, (255, 0, 0), self.collision_rect, 2)
    def update(self, keys):
        move = False

        if self.boost_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.boost_start_time >= 1000:
                self.boost_active = False
                self.speed = self.normal_speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = 'left'
            self.left_click = True
            move = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = 'right'
            self.left_click = False
            move = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = 'down_rotate' if self.left_click else 'down'
            move = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = 'down_rotate' if self.left_click else 'down'
            move = True

        if move:
            self.frame_index += 0.4
            if self.frame_index >= len(self.animations[self.direction]):
                self.frame_index = 0
        else:
            self.frame_index = 0

        #self.collision_rect = self.rect.inflate(-16, -16)
        # zmniejszenie hitboxa
        self.collision_rect = self.rect.inflate(-40, -40)  
        self.collision_rect.center = self.rect.center

        #przesuniecie względem osi Y
        self.collision_rect.y += 30

        
        # Blokowanie ruchu poza ekran
        if self.rect.left < -SPRITE_SIZE:
            self.rect.left = -SPRITE_SIZE
        elif self.rect.right > SCREEN_WIDTH+SPRITE_SIZE:
            self.rect.right = SCREEN_WIDTH+SPRITE_SIZE

        if self.rect.top < -SPRITE_SIZE:
            self.rect.top = -SPRITE_SIZE
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.image = self.animations[self.direction][int(self.frame_index)]
