import pygame
import sys
from tkinter import Canvas

#start of the game
def start_game():
    Canvas.fill(Black)
    start_image = pygame.image.load('Start.png')
    start_image_rect = start_image.get_rect()
    start_image_rect.center = (window_width/2, window_height/2)
    cancas.blit(start_image, start_image_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.quit:
                pygame.quit()
                sys.exit()
            if event.type == pygame.keydown:
                if event.key == pygame.k_escape:
                    pygame.quit()
                    sys.exit()
                game.loop()
        pygame.display.update()

#Game Levels      
def check_level(score):
    global check_level
    if score in range(0,10):
        cactus_img_rect.bottom = 50
        fire_img_rect.top = -50
        level = 1
    elif score in range(10,20):
        cactus_img_rect.bottom = 100
        fire_img_rect.top = -100
        level = 2
    elif score in range(10,20):
        cactus_img_rect.bottom = 150
        fire_img_rect.top = -150
        level = 3
    elif score in range(10,20):
        cactus_img_rect.bottom = 200
        fire_img_rect.top = -200
        level = 4

