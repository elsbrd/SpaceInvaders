import pygame
import os

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
accur = 50
size_of_enemies = 70
# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png")),(size_of_enemies, 50))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png")),(50 ,40))
# Bunkers
BUNKER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_bunker.png")),(30 ,15))
# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))




def snext(method):
    if method == 'star':
        return 'dfs'
    elif method == 'dfs':
        return 'bfs'
    elif method == 'bfs':
        return 'ucs'
    elif method == 'ucs':
        return 'star'


method = 'star'
