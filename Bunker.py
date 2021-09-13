import pygame
from settings import *
from Laser import Laser
green = (0, 255, 0)
# Create Bunkers

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

class Bunker():
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.bunker_img = BUNKER
        self.mask = pygame.mask.from_surface(self.bunker_img)
        self.lasers = []
        self.cool_down_counter = 0
        self.max_health = health


    def draw(self, window):
        window.blit(self.bunker_img, (self.x, self.y))

    def collision(self, obj):
        return collide(self, obj)

    def cooldown(self):
        if self.cool_down_counter >= self.reduce:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1


    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:  # if it collided remove the object
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def get_width(self):
        return self.bunker_img.get_width()

    def get_height(self):
        return self.bunker_img.get_height()



