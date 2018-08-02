import json
import pygame


class Position:
    def __init__(self, line, column):
        self.line = line
        self.column = column


class Cell:
    def __init__(self, position, value):
        self.position = position
        self.value = value


def get_maze_from_file():
    maze = []
    with open("data/maze.json") as maze_file:
        data = json.load(maze_file)
        for entry in data:
            maze.append(entry["line"])
    return maze


def show_maze(maze):
    pygame.init()
    window = pygame.display.set_mode((300, 300))
    wall = pygame.image.load("data/wall.jpg").convert()
    floor = pygame.image.load("data/floor.jpg").convert()
    mac = pygame.image.load("data/MacGyver.png").convert_alpha()
    guard = pygame.image.load("data/Gardien.png").convert_alpha()
    ether = pygame.image.load("data/ether.png").convert_alpha()
    needle = pygame.image.load("data/aiguille.png").convert_alpha()
    tube = pygame.image.load("data/tube_plastique.png").convert_alpha()

    line_index = 0
    column_index = 0
    for i in range(len(maze)):
            if maze[i].value == "f":
                window.blit(floor, (column_index * 20, line_index * 20))
            elif maze[i].value == "w":
                window.blit(wall, (column_index * 20, line_index * 20))
            elif maze[i].value == "m":
                window.blit(floor, (column_index * 20, line_index * 20))
                window.blit(mac, (column_index * 20, line_index * 20))
            elif maze[i].value == "g":
                window.blit(floor, (column_index * 20, line_index * 20))
                window.blit(guard, (column_index * 20, line_index * 20))
            elif maze[i].value == "e":
                window.blit(floor, (column_index * 20, line_index * 20))
                window.blit(ether, (column_index * 20, line_index * 20))
            elif maze[i].value == "n":
                window.blit(floor, (column_index * 20, line_index * 20))
                window.blit(needle, (column_index * 20, line_index * 20))
            elif maze[i].value == "t":
                window.blit(floor, (column_index * 20, line_index * 20))
                window.blit(tube, (column_index * 20, line_index * 20))
            if column_index < 14:
                column_index += 1
            else:
                line_index += 1
                column_index = 0
    pygame.display.flip()

    still_playing = 1
    while still_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                still_playing = 0


def main():
    maze = []
    cells = get_maze_from_file()
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            pos = Position(i, j)
            cell = Cell(pos, cells[i][j])
            maze.append(cell)
    show_maze(maze)


if __name__ == "__main__":
    main()
