import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TOTAL_TIME, MAX_SPEED_POINTS, MAX_DEFAULT_POINTS
from player import Player
from points import Speed_Point, Default_Point, spawn_point, pilka
from menu import main_menu, loading
from enemy import Husky
from bush import Bush
import random

pygame.init()

#parametry startowe (menu, loading, tła)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bobiś - The amazing cat")
clock = pygame.time.Clock()

tlo = pygame.image.load('assets/tlo.jpg')
tlo = pygame.transform.scale(tlo, (SCREEN_WIDTH, SCREEN_HEIGHT))
main_menu(screen)
loading(screen)


#generowanie sprite'ów
player = Player((100, 100))
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

bushes = pygame.sprite.Group()
bushes.add(
    Bush((300, 400)),
    Bush((SCREEN_WIDTH-300, 400))
)

speed_points = pygame.sprite.Group()
default_points = pygame.sprite.Group()

pilka_bool = False
ball = pygame.sprite.Group()

husky = Husky((random.randint(400,SCREEN_WIDTH), random.randint(400,SCREEN_HEIGHT))) 
enemies = pygame.sprite.Group()
enemies.add(husky) 


def przegrana():
    font = pygame.font.Font("assets/pixel.ttf", 100)
    lose_text = font.render("Przegrałeś :(", True, (255, 0, 0))
    screen.fill((50, 50, 50))
    screen.blit(lose_text, (SCREEN_WIDTH//2 - lose_text.get_width()//2, SCREEN_HEIGHT//2 - lose_text.get_height()//2))
    pygame.display.flip()
    waiting = True
    #pętla po to aby po wyświetleniu komunikatu fragment kodu cały czas się wywoływałał a nie tylko raz
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    

#spawn punktów
for _ in range(MAX_SPEED_POINTS):
    spawn_point(speed_points, all_sprites, Speed_Point)

for _ in range(MAX_DEFAULT_POINTS):
    spawn_point(default_points, all_sprites, Default_Point)

start_ticks = pygame.time.get_ticks()
extra_time_given = False
total_time = TOTAL_TIME

#główna pętla gry

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            if not extra_time_given:
                total_time += 1
                extra_time_given = True

    keys = pygame.key.get_pressed()
    all_sprites.update(keys)
    enemies.update(player, bushes)
    speed_points.update()
    
    #screen.fill((50, 100, 50))
    
    screen.blit(tlo,(0,0))
    all_sprites.draw(screen)
    enemies.draw(screen)

    second_passed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = total_time - second_passed

    font = pygame.font.Font("assets/pixel.ttf", 50)
    timer_text = font.render(f'Time: {time_left} s', True, (255, 255, 255))
    points_text = font.render(f'Points: {player.points}', True, (255, 255, 255))

    screen.blit(timer_text, (20, 20))
    screen.blit(points_text, (20, 70))

    for bush in bushes:
        screen.blit(bush.image, bush.rect)

    boost_hit = pygame.sprite.spritecollide(player, speed_points, True)
    if boost_hit:
        player.active_boost()
        for _ in range(len(boost_hit)):
            spawn_point(speed_points, all_sprites, Speed_Point)

    default_hit = pygame.sprite.spritecollide(player, default_points, True)
    if default_hit:
        player.add_point()
        if not extra_time_given:
            total_time += 1
            extra_time_given = True
        for _ in range(len(default_hit)):
            spawn_point(default_points, all_sprites, Default_Point)

    #rysowanie hitboxa
    #player.draw_hitbox(screen)
    #bush.draw_hitbox(screen)

    if player.points >= 20 and not pilka_bool:
        pilka = pilka((random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)))
        ball.add(pilka)
        all_sprites.add(pilka)
        pilka_bool = True 

    #font ekran koncowy
    font_1 = pygame.font.Font("assets/pixel.ttf", 100)

    husky_collision1 = any(
        husky.collision_rect.colliderect(player.collision_rect) and not player.is_hidden(bushes)
        for husky in enemies
    )
    if husky_collision1:
        przegrana()
    
    
    ball_hit = pygame.sprite.spritecollide(player, ball, True)
    if player.points >= 20 and ball_hit:
        win_text = font_1.render("Wygrałeś!", True, (0, 255, 0))
        screen.fill((50, 50, 50))
        screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, SCREEN_HEIGHT//2 - win_text.get_height()//2))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    elif player.points < 20 and time_left <= 0 or player.points >= 20 and time_left <=0:
        przegrana()

    extra_time_given = False
    #print("Ukryty:", player.is_hidden(bushes))
    pygame.display.flip()
    clock.tick(FPS)
