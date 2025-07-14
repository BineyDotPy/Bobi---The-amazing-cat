import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT



def loading(screen):
    pixel_font = pygame.font.Font("assets/pixel.ttf", 35)
    background = pygame.image.load("assets/background_menu.png").convert()
    blur = pygame.transform.smoothscale(background,(SCREEN_WIDTH//10, SCREEN_HEIGHT//10))
    blur = pygame.transform.smoothscale(blur,(SCREEN_WIDTH,SCREEN_HEIGHT))
    background = blur

    loading_text = pixel_font.render("Ładowanie...", True, (255, 255, 255))

    bar_width = 600
    bar_height = 40
    bar_x = (SCREEN_WIDTH - bar_width) // 2
    bar_y = (SCREEN_HEIGHT - bar_height) // 2 + 60

    for progress in range(0, 100, 10):
        screen.blit(background, (0, 0))
        screen.blit(loading_text, (SCREEN_WIDTH//2 - loading_text.get_width()//2, SCREEN_HEIGHT//2 - 50))

        # obramowanie paska
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # wypełnienie paska
        fill_width = (progress / 100) * bar_width
        pygame.draw.rect(screen, (0, 255, 0), (bar_x + 2, bar_y + 2, fill_width - 4, bar_height - 4))

        pygame.display.flip()
        pygame.time.delay(50)  # symulacja ładowania

def main_menu(screen):
    menu = True

    pixel_font = pygame.font.Font("assets/pixel.ttf", 35)
    text_bg = pygame.image.load("assets/tabelka.png").convert_alpha()
    text_bg = pygame.transform.scale(text_bg,(SCREEN_WIDTH//2, 150))
    text_bg_rect = text_bg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT -80))

    background = pygame.image.load("assets/background_menu.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    

    while menu:
        screen.blit(background, (0, 0))
        screen.blit(text_bg, text_bg_rect)
        
        author = pixel_font.render("@BK EiT 2025", True, (255,255,255))
        start_text = pixel_font.render("Naciśnij SPACJĘ, aby rozpocząć", True, (255, 255, 255))
        quit_text = pixel_font.render("ESC - wyjście", True, (255, 255, 255))
        
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 780))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 820))
        screen.blit(author, (5,5))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
