from Invaders import Invaders
class Dummy(Invaders):
    def action(self, vel,player):  # the move
        self.y += vel
