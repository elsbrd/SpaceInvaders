import pygame
import random
from algorithm import *
from Search import search
from csv_write import csv_write
from settings import *
from Ship import Ship
from Bunker import Bunker
from Dumm import *
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
    global method
    playing = True  # running the game
    FPS = 30
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    invaders = []  # store were the enimies will be
    bunkers = []
    wave_length = 1  # every level will generate a new amount of enimies
    enemy_vel = 1  # time of movement

    player_vel = 20
    laser_vel = 30



    player = Player(330, 630)
    for i in range (4):
        bunkers.extend([Bunker(random.randrange(0, 750),random.randrange(0, 750-YELLOW_SPACE_SHIP.get_height()-50))])

    clock = pygame.time.Clock()

    cast_away = False  # lost
    lost_count = 0
    def invadersHold():
        lasers = []
        for i in invaders:
            for laser in i.lasers:
                lasers.append(laser)
        return lasers

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        # position of the labels
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        player.shoot()
        for invader in invaders:  # draw the enemies
            invader.draw(WIN)

        player.draw(WIN)

        if cast_away:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            WIN.blit(lost_label,(WIDTH/2-lost_label.get_width()/22, 350))

    while playing:  # running the game
        clock.tick(FPS)  # it will run with the same speed in any devices


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
            wave_length += 2
            for i in range(wave_length):

                invaders.append(Dummy(random.randrange(50, WIDTH - 100), random.randrange(10, 200),
                              random.choice(["red", "blue", "green"])))
                invaders.append(Invaders(random.randrange(50, WIDTH - 100), random.randrange(10, 200),
                                         random.choice(["red", "blue", "green"])))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if we press quit it will stop running
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    method = snext(method)
                    print(method)

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
        for bunker in bunkers:
            # bunker.action(enemy_vel)
            # bunker.move_lasers(laser_vel, player)

            if collide(player, bunker):
                # bunker.health -= 10
                bunkers.remove(bunker)
                print(1)
            elif bunker.y + bunker.get_height() > HEIGHT:
                lives -= 1
                bunkers.remove(bunker)
        #result_of_search = search(player, invaders, bunkers, method)

        import time
        start_time = time.time()
        (alpha_beta_result, direction) = alphabeta(Node(player, invaders, invadersHold(), '', bunkers), depth_recurtion, -float('inf'),float('inf'),False)
        #(alpha_beta_result, direction) = expectiminimax(Node(player,  invaders, invadersHold(), '', bunkers), depth_recurtion, True)
        print((alpha_beta_result, direction.move) )

        # useless
        # move to target

        dirs = {"<": (-8, 0), ">": (8, 0), '': (0, 0)}

        # move to target

        player.x += dirs[direction.move][0]
        lasers = []
        for i in invaders:
            for laser in i.lasers:
                lasers.append(laser)
        for bul in lasers:
            if bul.x in range(int(player.x) - int(RED_LASER.get_width()), int(player.x) + int(
                    YELLOW_SPACE_SHIP.get_width())) and bul.y < player.y + YELLOW_SPACE_SHIP.get_height() and player.y - (
                    bul.y + RED_LASER.get_height()) < 100:
                # if bul.x in range(0 if ship.x-LASER_IMG.get_width()-1<0 else ship.x-LASER_IMG.get_width()-1,(WIDTH-size_of_enemies) if ship.x+size_of_enemies+1>WIDTH else WIDTH-size_of_enemies):
                # if shipen more left from laser
                if player.x + YELLOW_SPACE_SHIP.get_width() / 2 - bul.x + RED_LASER.get_width() / 2 < 0:
                    # move left
                    # if no start of map
                    if player.x - abs(player_vel) > 0:
                        player.x -= abs(player_vel + 10)
                    # else move right
                    else:
                        player.x += abs(player_vel + 10)
                elif player.x + YELLOW_SPACE_SHIP.get_width() / 2 - bul.x + RED_LASER.get_width() / 2 > 0:
                    # move right
                    # if not end of map
                    if player.x + YELLOW_SPACE_SHIP.get_width() + abs(player_vel) < WIDTH:
                        player.x += abs(player_vel + 10)
                    # else move left
                    else:
                        player.x -= abs(player_vel + 10)


        for bunker in bunkers:
            bunker.draw(WIN)

        # move them down
        for invader in invaders[:]:
            invader.action(enemy_vel,player)
            invader.move_lasers(laser_vel, player, bunkers)

            if random.randrange(0, 2 * 60) == 1:  # probability of 50% of shooting
                invader.shoot()

            if collide(invader, player):
                player.health -= 10
                invaders.remove(invader)
            elif invader.y + invader.get_height() > HEIGHT:
                lives -= 1
                invaders.remove(invader)


        # Функцие мув лазерс я просто тупо добавил неограниченное количество остаточных параметров,
        # чтобы можно было передавать несколько массивов врагов (у тебя их два - враги-корабли и астероиды)
        player.move_lasers(-laser_vel, invaders, bunkers)  # to make the space cruft to do up
        # Тут была главная проблема, потому что ты не проверяла на сталкивания с астероидами вообще

        csv_write('output.csv', [str(cast_away), str(time.time() - start_time), str(level), 'alpha-beta', 'expetr minimax'])

        pygame.display.update()  # refresh the screen
        redraw_window()



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