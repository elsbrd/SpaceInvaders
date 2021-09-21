import sys
from matplotlib import pyplot as plt

from settings import *

matrix = [[0 for i in range(HEIGHT)] for j in range(WIDTH)]
sys.setrecursionlimit(99999999)


def check(matrix, ship_mask_with_pos):
    for point in ship_mask_with_pos:
        try:
            if matrix[point[1]][point[0]] == 2:
                return 'found'
            elif matrix[point[1]][point[0]] == 3:
                return "back"
        except IndexError:
            return 'out'
    return False

visited = []
found = False

def bfs(matrix, current, player):
    '''прохід бфс'''
    print("seaching for bfs")
    global found, path, visited, queue
    queue.append(current)
    curr = current
    while len(queue) != 0 and not found:
        curr = queue[0]
        visited.append(curr)
        if found:
            queue.append(curr)
            return poped_queue
        visited.append(curr)
        WIN.set_at(curr, (0, 255, 255))
        pygame.display.update()
        for i in [(0, -accur), (-accur, 0), (accur, 0),
                  (0, accur)]:
            new_curr = (curr[0] + i[0], curr[1] + i[1])
            new_ship_mask_with_pos = [(int(h[0] + i[0] + new_curr[0] - YELLOW_SPACE_SHIP.get_width() / 2),
                                       int(h[1] + i[1] + new_curr[1] - YELLOW_SPACE_SHIP.get_height() / 2)) for h in
                                      player.mask.outline()]

            check_res = check(matrix, new_ship_mask_with_pos)
            if check_res == 'back':
                visited.append(new_curr)
            elif check(matrix, new_ship_mask_with_pos) == 'found':
                poped_queue.append(curr)
                poped_queue.append(new_curr)
                found = True
                return poped_queue
            elif new_curr not in visited:
                queue.append(new_curr)

        poped_queue.append(queue.pop(0))

    return []




def dfs(WIN, matrix, ship_mask_with_pos, path, curr):
    global found
    global visited
    if found:
        return path
    path = path
    curr = curr
    visited.append(curr)
    check_res = check(matrix, ship_mask_with_pos)
    if check_res == 'found':
        found = True
        return path
    elif not check_res:

        path.append(curr)
        for i in [(0, -accur), (-accur, 0), (accur, 0),
                  (0, accur), ]:
            new_curr = (curr[0] + i[0], curr[1] + i[1])
            new_ship_mask_with_pos = [(h[0] + i[0], h[1] + i[1]) for h in ship_mask_with_pos]
            if min(new_ship_mask_with_pos, key=lambda x: x[0])[0] < 0 or \
                    min(new_ship_mask_with_pos, key=lambda x: x[1])[1] < 0:
                continue
            elif found:
                break
            elif check(matrix, new_ship_mask_with_pos) == 'out':
                continue
            elif new_curr not in visited:
                path = dfs(WIN, matrix, new_ship_mask_with_pos, path, new_curr)
            else:
                continue
    return path


queue = []
poped_queue = []

path = []



matrix_uni = [[[] for i in range(WIDTH)] for j in range(HEIGHT)]


def uniform(matrix, current, player):
    print("searching ucs")
    global found, path, visited, queue
    queue.append(current)
    curr = current
    while len(queue) != 0 and not found:
        curr = queue[0]
        visited.append(curr)

        visited.append(curr)
        for i in [(0, -accur), (-accur, 0), (accur, 0),
                  (0, accur)]:
            new_curr = (curr[0] + i[0], curr[1] + i[1])
            new_ship_mask_with_pos = [(int(h[0] + i[0] + new_curr[0] - YELLOW_SPACE_SHIP.get_width() / 2),
                                       int(h[1] + i[1] + new_curr[1] - YELLOW_SPACE_SHIP.get_height() / 2)) for h in
                                      player.mask.outline()]

            check_res = check(matrix, new_ship_mask_with_pos)
            if check_res == 'back':
                visited.append(new_curr)
            elif check(matrix, new_ship_mask_with_pos) == 'found':
                poped_queue.append(curr)
                poped_queue.append(new_curr)
                found = True
                try:
                    matrix_uni[new_curr[1]][new_curr[0]] = curr
                except IndexError:
                    pass
                return find_way(matrix_uni, new_curr)
            elif new_curr not in visited:
                queue.append(new_curr)  # y down x side
                try:
                    matrix_uni[new_curr[1]][new_curr[0]] = curr
                except IndexError:
                    pass
        poped_queue.append(queue.pop(0))

    return []


def find_way(uni_matrix, point):
    way = [point]
    while point:
        print('way',way)
        point = uni_matrix[point[1]][point[0]]
        if point:
            print('point not empty')
            way.append(point)
        elif point == []:
            print('returning way')
            return way


def search(player, invaders, bunkers, method):
    global matrix
    global visited, queue, path, found, line, poped_queue,matrix_uni
    lines = []

    try:
        for GOAL in invaders:
            matrix = [[0 for i in range(HEIGHT)] for j in range(WIDTH)]
            for inv in invaders:
                for invpoint in inv.mask.outline():
                    matrix[invpoint[1] + inv.y][invpoint[0] + inv.x] = 3
                for laser in inv.lasers:
                    for point in laser.mask.outline():
                        matrix[point[1] + laser.y][point[0] + laser.x] = 3
            for i in GOAL.mask.outline():
                matrix[i[1] + GOAL.y][i[0] + GOAL.x] = 2
    except IndexError:
        pass
    pos = []
    for i in player.mask.outline():
        if method == 'dfs':
            pos.append((int(i[0]) + int(player.x), int(i[1]) + int(player.y)))
        elif method == 'bfs' or method == 'ucs':
            pos.append((int(i[0]), int(i[1])))

    for bunker in bunkers:
        for point in bunker.mask.outline():
            matrix[point[1] + bunker.y][point[0] + bunker.x] = 3
    if method == 'dfs':
        line = dfs(WIN, matrix, pos, [], ((max(player.mask.outline(), key=lambda coords: coords[0])[0] +
                                           min(player.mask.outline(), key=lambda coords: coords[0])[0]) // 2 +
                                          int(player.x),
                                          (max(player.mask.outline(), key=lambda coords: coords[1])[1] +
                                           min(player.mask.outline(), key=lambda coords: coords[1])[1]) // 2 + int(
                                              player.y)))
    elif method == 'bfs':
        line = bfs(matrix, ((max(player.mask.outline(), key=lambda coords: coords[0])[0] +
                             min(player.mask.outline(), key=lambda coords: coords[0])[0]) // 2 +
                            int(player.x),
                            (max(player.mask.outline(), key=lambda coords: coords[1])[1] +
                             min(player.mask.outline(), key=lambda coords: coords[1])[1]) // 2 + int(
                                player.y)), player)
    elif method == 'ucs':
        line = uniform(matrix, ((max(player.mask.outline(), key=lambda coords: coords[0])[0] +
                                 min(player.mask.outline(), key=lambda coords: coords[0])[0]) // 2 +
                                int(player.x),
                                (max(player.mask.outline(), key=lambda coords: coords[1])[1] +
                                 min(player.mask.outline(), key=lambda coords: coords[1])[1]) // 2 + int(
                                    player.y)), player)

    poped_queue = []
    matrix_uni=[[[] for i in range(WIDTH)] for j in range(HEIGHT)]
    if line:
        lines.append(line)
    found = False
    visited = []
    queue = []
    path = []
    found = False
    print(lines)
    return lines


def draw_matrix(field):
    x = [0, WIDTH]
    y = [0, HEIGHT]
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] > 0:
                x.append(int(j))
                y.append(int(HEIGHT - i))
    plt.scatter(x, y)
    plt.show()
