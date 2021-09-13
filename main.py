import pygame
import random
from settings import *
from Ship import Ship
from Bunker import Bunker
from Player import Player
from Invaders import Invaders

pygame.font.init()

green = (0, 255, 0)
red = (255, 0, 0)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    playing = True  # running the game
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    invaders = []  # store were the enimies will be
    bunkers = []
    wave_length = 5  # every level will generate a new amount of enimies
    enemy_vel = 1  # time of movement

    player_vel = 5
    laser_vel = 5

    player = Player(330, 630)

    bunker1 = Bunker(50, 500)
    bunker2 = Bunker(350, 500)
    bunker3 = Bunker(600, 500)

    clock = pygame.time.Clock()

    cast_away = False  # lost
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        # position of the labels
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for invader in invaders:  # draw the enemies
            invader.draw(WIN)

        player.draw(WIN)
        bunker1.draw(WIN)
        bunker2.draw(WIN)
        bunker3.draw(WIN)

        pygame.display.update()  # refresh the screen

    while playing:  # running the game
        clock.tick(FPS)  # it will run with the same speed in any devices

        redraw_window()

        if lives <= 0 or player.health <= 0:
            cast_away = True
            lost_count += 1  # then starting a new game

        if cast_away:
            if lost_count > FPS * 3:
                playing = False
            else:
                continue

        # the start movement of the enemies
        if len(invaders) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                invader = Invaders(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                                   random.choice(["red", "blue", "green"]))
                invaders.append(invader)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if we press quit it will stop running
                quit()

        keys = pygame.key.get_pressed()  # returning the dictionary of all the keys and tells u whether they r pressed or not at the current time
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

            # move them down
        for bunker in bunkers[:]:
            # bunker.action(enemy_vel)
            # bunker.move_lasers(laser_vel, player)

            if collide(player, bunker):
                bunker.health -= 10
                bunkers.remove(bunker)
                print(1)
            elif bunker.y + bunker.get_height() > HEIGHT:
                lives -= 1
                bunkers.remove(bunker)

        # move them down
        for invader in invaders[:]:
            invader.action(enemy_vel)
            invader.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:  # probability of 50% of shooting
                invader.shoot()

            if collide(invader, player):
                player.health -= 10
                invaders.remove(invader)
            elif invader.y + invader.get_height() > HEIGHT:
                lives -= 1
                invaders.remove(invader)

        player.move_lasers(-laser_vel, invaders)  # to make the space cruft to do up


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    playing = True
    while playing:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
