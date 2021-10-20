from settings import *

def check_collision(obj1_mask, obj1_pos, obj2_mask, obj2_pos):
    pos1 = [(point[0] + obj1_pos[0], point[1] + obj1_pos[1]) for point in obj1_mask]
    pos2 = [(point[0] + obj2_pos[0], point[1] + obj2_pos[1]) for point in obj2_mask]
    for point1 in pos1:
        for point2 in pos2:
            if point2 == point1:
                return True
    return False


def dist(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 1 / 2


class Node:
    def __init__(self, player, invaders, bulls, move, bunkers):
        self.player = player.copy_object()
        self.invaders = [invader.copy_object() for invader in invaders]
        self.bulls = [bull.copy_object() for bull in bulls]
        self.bunkers = [bunker.copy_object() for bunker in bunkers]
        self.move = move
        self.is_terminal = False


    def check_collision_laser_n_player(self) -> bool:
        for egg in self.bulls:
            if check_collision(self.player.mask.outline(), (self.player.x, self.player.y), egg.mask.outline(),
                               (egg.x, egg.y)):
                return True
        return False

    def check_collision_ship_n_laser(self) -> bool:
        for laser in self.player.lasers:
            for ship in self.invaders:
                if check_collision(laser.mask.outline(), (laser.x, laser.y), ship.mask.outline(), (ship.x, ship.y)):
                    return True
        return False

    def generate_children(self):
        children = []
        for new_position, direction in [((-8, 0), '<'),
                                        ((8, 0), '>')]:  # ,((0, -12),'↑'), ((0, 12),'↓')]:  # Adjacent squares ,
            # Get node position
            node_position = (self.player.x + new_position[0], self.player.y + new_position[1])
            # Make sure within range
            if node_position[0] > WIDTH - 1 or node_position[0] < 1 or node_position[1] > HEIGHT - 1 or node_position[
                1] < 1:
                continue

            # move elements
            for invader in self.invaders[:]:
                invader.action(enemy_vel,self.player)
                invader.move_lasers(laser_vel, self.player, self.bunkers)

            # check player collisions
            if self.check_collision_laser_n_player():
                self.is_terminal = True

            self.player.x += new_position[0]

            # Create new node
            new_node = Node(self.player, self.invaders, self.bulls, direction, self.bunkers)
            # Append
            children.append(new_node)
        return children

    def evaluation_function(self):
        if self.check_collision_laser_n_player():
            return float('-inf')
        elif self.check_collision_ship_n_laser():
            return float('inf')
        else:
            centre_player = (
            self.player.x + self.player.ship_img.get_width() / 2, self.player.y + self.player.ship_img.get_height() / 2)
            distances = []
            for enemy in self.invaders:
                distances.append(dist(centre_player,
                                      (enemy.x + enemy.ship_img.get_width() / 2, enemy.y + enemy.ship_img.get_height() / 2)))
            try:
                minvalue = min(distances)
            except ValueError:
                minvalue = 0
        return minvalue


def alphabeta(node: Node, depth, a, b, maximizingPlayer):
    if depth == 0 or node.is_terminal:  # or node is terminal_node:
        return (node.evaluation_function(), node)
    if maximizingPlayer:
        value = -float('inf')
        best_node = node
        # if collide with egg then return value -inf, node
        for child in node.generate_children():
            alphares, alphanode = alphabeta(child, depth - 1, a, b, True)
            if alphares > value:
                value = alphares
                best_node = child
            if value >= b:
                break  # (* b cutoff *)
            if value > a:
                a = value
        return (value, best_node)
    else:
        worst_node = node
        value = float('inf')
        # if collide with laser then return value +inf, node
        for child in node.generate_children():
            alphares, alphanode = alphabeta(child, depth - 1, a, b, False)
            if alphares < value:
                value = alphares
                worst_node = child
            if value <= a:
                break  # (* a cutoff *)
            if value < b:
                b = value
        return (value, worst_node)


def expectiminimax(node: Node, depth, maximizingPlayer):
    if depth == 0 or node.is_terminal:  # or node is terminal_node:
        return (node.evaluation_function(), node)
    if maximizingPlayer:

        res_arr_of_nodes = [expectiminimax(child, depth - 1, False) for child in node.generate_children()]
        alphares, alphanode = max(res_arr_of_nodes, key=lambda x: x[0], default=node)
        return (alphares / len(res_arr_of_nodes), alphanode)
    else:
        res_arr_of_nodes = [expectiminimax(child, depth - 1, True) for child in node.generate_children()]
        alphares, alphanode = min(res_arr_of_nodes, key=lambda x: x[0], default=node)
        return (alphares / len(res_arr_of_nodes), alphanode)

