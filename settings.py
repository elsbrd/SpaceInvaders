import pygame
import os

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
accur = 50
# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Bunkers
BUNKER = pygame.image.load(os.path.join("assets", "pixel_bunker.png"))
# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

methods = ['dfs', 'bfs', 'ucs']


def snext(method):
    if method == 'dfs':
        return 'bfs'
    elif method == 'bfs':
        return 'ucs'
    elif method == 'ucs':
        return 'dfs'


method = 'dfs'
