from settings import *
from Ship import Ship
from Laser import Laser
class Invaders(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        #
        self.color = color
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def action(self, vel, player):  # the move
        for bul in player.lasers:

            if bul.x in range(self.x - int(RED_LASER.get_width()),
                              self.x + size_of_enemies) and bul.y + RED_LASER.get_height() > self.y:
                # if selfen more left from laser
                if self.x + size_of_enemies / 2 - bul.x + RED_LASER.get_width() / 2 < 0:
                    # move left
                    # if no start of map
                    if self.x - 8 > 0:
                        self.x -= 8
                    # else move right
                    else:
                        self.x += 8*5
                elif self.x + size_of_enemies / 2 - bul.x + RED_LASER.get_width() / 2 > 0:
                    # move right
                    # if not end of map
                    if self.x + size_of_enemies + 8 < WIDTH:
                        self.x += 8
                    # else move left
                    else:
                        self.x -= 8*5

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + int(self.ship_img.get_width()/2), self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def copy_object(self):
        res = Invaders(self.x,self.y, self.color, self.health)
        res.ship_img, res.laser_img = res.COLOR_MAP[res.color]

        return res