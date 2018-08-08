import json
import pygame


class Position:
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def convert_units(self):
        return self.line * 15 + self.column


class Cell:
    def __init__(self, position, value):
        self.position = position
        self.value = value


class Maze:
    def __init__(self, cells=[]):
        self.cells = cells

    def get_maze_from_file(self):
        maze = []
        with open("data/maze.json") as maze_file:
            data = json.load(maze_file)
            for entry in data:
                maze.append(entry["line"])
        self.cells = maze
        maze = []
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                pos = Position(i, j)
                cell = Cell(pos, self.cells[i][j])
                maze.append(cell)
        return maze

    def get_mac_cell(self):
        for i in range(len(self.cells)):
            if self.cells[i].value == "m":
                return self.cells[i]

    def get_neighbor_list(self, cell):
        pos = cell.position.line * 15 + cell.position.column
        n_list = [pos - 1, pos + 1, pos - 15, pos + 15]
        rm_list = []
        for VALUE in n_list:
            if VALUE < 0 or VALUE >= 225 or (VALUE // 15 != pos // 15 and VALUE not in {pos - 15, pos + 15}):
                rm_list.append(VALUE)
            elif self.cells[VALUE].value == "w":
                rm_list.append(VALUE)
        for VALUE in rm_list:
            n_list.remove(VALUE)
        return n_list

    def get_direction(self, event):
        cell = self.get_mac_cell()
        neighbors = self.get_neighbor_list(cell)
        if event.key == pygame.K_DOWN and cell.position.convert_units() + 15 in neighbors:
            self.swap_cells(cell, self.cells[cell.position.convert_units()+15])
        elif event.key == pygame.K_UP and cell.position.convert_units() - 15 in neighbors:
            self.swap_cells(cell, self.cells[cell.position.convert_units() - 15])
        elif event.key == pygame.K_LEFT and cell.position.convert_units() - 1 in neighbors:
            self.swap_cells(cell, self.cells[cell.position.convert_units() - 1])
        elif event.key == pygame.K_RIGHT and cell.position.convert_units() + 1 in neighbors:
            self.swap_cells(cell, self.cells[cell.position.convert_units() + 1])
        self.show_maze(self)

    def swap_cells(self, cell_1, cell_2):
        self.cells[cell_1.position.convert_units()].value, self.cells[cell_2.position.convert_units()].value = \
            self.cells[cell_2.position.convert_units()].value, self.cells[cell_1.position.convert_units()].value

    @staticmethod
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
        for i in range(len(maze.cells)):
            if maze.cells[i].value == "f":
                window.blit(floor, (column_index * 20, line_index * 20))
            elif maze.cells[i].value == "w":
                window.blit(wall, (column_index * 20, line_index * 20))
            elif maze.cells[i].value == "m":
                window.blit(floor, (column_index * 20, line_index * 20))
                window.blit(mac, (column_index * 20, line_index * 20))
            elif maze.cells[i].value == "g":
                window.blit(floor, (column_index * 20, line_index * 20))
                window.blit(guard, (column_index * 20, line_index * 20))
            elif maze.cells[i].value == "e":
                window.blit(floor, (column_index * 20, line_index * 20))
                window.blit(ether, (column_index * 20, line_index * 20))
            elif maze.cells[i].value == "n":
                window.blit(floor, (column_index * 20, line_index * 20))
                window.blit(needle, (column_index * 20, line_index * 20))
            elif maze.cells[i].value == "t":
                window.blit(floor, (column_index * 20, line_index * 20))
                window.blit(tube, (column_index * 20, line_index * 20))
            if column_index < 14:
                column_index += 1
            else:
                line_index += 1
                column_index = 0
        pygame.display.flip()


def main():
    maze = Maze()
    maze.cells = maze.get_maze_from_file()
    still_playing = 1
    while still_playing:
        maze.show_maze(maze)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                maze.get_direction(event)
            """for cell in maze.cells:
                print(cell.position.line, cell.position.column, cell.value)"""
            if event.type == pygame.QUIT:
                still_playing = 0


if __name__ == "__main__":
    main()
