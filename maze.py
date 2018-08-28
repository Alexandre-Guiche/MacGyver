import json
import pygame
import time
from position import *
from cell import *


class Maze:

    ITEMS = set()

    def __init__(self):
        self.cells = self.generate_maze_from_file()

    def get_cells(self):
        return self.cells

    @staticmethod
    def generate_maze_from_file():
        # reads Json file, creates a list of lines then returns a list of Cell objects from all the lines
        maze_lines = []
        maze_cells = []
        with open("data/maze.json") as maze_file:
            data = json.load(maze_file)
            for entry in data:
                maze_lines.append(entry["line"])
        for i in range(len(maze_lines)):
            for j in range(len(maze_lines[i])):
                pos = Position(i, j)
                cell = Cell(pos, maze_lines[i][j])
                maze_cells.append(cell)
        return maze_cells

    def get_mac_cell(self):
        # returns MacGyver position in the maze
        for i in range(len(self.cells)):
            if self.cells[i].value == "m":
                return self.cells[i]

    def get_neighbor_list(self, cell):
        # checks every nearby free cell then returns them in a list
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
        # catches user keyboard events to know where to move Mac
        cell = self.get_mac_cell()
        neighbors = self.get_neighbor_list(cell)
        if event.key == pygame.K_DOWN and cell.position.convert_units() + 15 in neighbors:
            if self.cells[cell.position.convert_units() + 15].value in ["n", "e", "t"]:
                self.get_item(cell, self.cells[cell.position.convert_units()+15])
            elif self.cells[cell.position.convert_units() + 15].value == "g":
                self.fight_guard(cell, self.cells[cell.position.convert_units() + 15])
            else:
                self.swap_cells(cell, self.cells[cell.position.convert_units()+15])
        elif event.key == pygame.K_UP and cell.position.convert_units() - 15 in neighbors:
            if self.cells[cell.position.convert_units() - 15].value in ["n", "e", "t"]:
                self.get_item(cell, self.cells[cell.position.convert_units()-15])
            elif self.cells[cell.position.convert_units() - 15].value == "g":
                self.fight_guard(cell, self.cells[cell.position.convert_units() - 15])
            else:
                self.swap_cells(cell, self.cells[cell.position.convert_units() - 15])
        elif event.key == pygame.K_LEFT and cell.position.convert_units() - 1 in neighbors:
            if self.cells[cell.position.convert_units() - 1].value in ["n", "e", "t"]:
                self.get_item(cell, self.cells[cell.position.convert_units()-1])
            elif self.cells[cell.position.convert_units() - 1].value == "g":
                self.fight_guard(cell, self.cells[cell.position.convert_units() - 1])
            else:
                self.swap_cells(cell, self.cells[cell.position.convert_units() - 1])
        elif event.key == pygame.K_RIGHT and cell.position.convert_units() + 1 in neighbors:
            if self.cells[cell.position.convert_units() + 1].value in ["n", "e", "t"]:
                self.get_item(cell, self.cells[cell.position.convert_units()+1])
            elif self.cells[cell.position.convert_units() + 1].value == "g":
                self.fight_guard(cell, self.cells[cell.position.convert_units() + 1])
            else:
                self.swap_cells(cell, self.cells[cell.position.convert_units() + 1])
        self.show_maze(self)

    def swap_cells(self, cell_1, cell_2):
        # Swaps two neighbors cells together
        self.cells[cell_1.position.convert_units()].value, self.cells[cell_2.position.convert_units()].value = \
            self.cells[cell_2.position.convert_units()].value, self.cells[cell_1.position.convert_units()].value

    def get_item(self, cell_mac, cell_item):
        # Collects item in a list then swaps Mac and the now empty cell
        self.ITEMS.add(self.cells[cell_item.position.convert_units()].value)
        self.cells[cell_item.position.convert_units()].value = "f"
        self.swap_cells(cell_mac, cell_item)

    def fight_guard(self, cell_mac, cell_guard):
        # Checks if every item is in the list when approaching the guard, then calls a function
        # to print if the player won or lost
        if self.ITEMS == {"e", "n", "t"}:
            self.cells[cell_guard.position.convert_units()].value = "f"
            self.swap_cells(cell_mac, cell_guard)
            self.game_won()
        else:
            self.game_lost()

    def game_won(self):
        # prints 'you won' on the board then closes the game
        game_quit = pygame.event.Event(12, {})
        self.show_maze(self, "win")
        time.sleep(3)
        pygame.event.post(game_quit)

    def game_lost(self):
        # prints 'you lost' on the board then closes the game
        game_quit = pygame.event.Event(12, {})
        self.show_maze(self, "lost")
        time.sleep(3)
        pygame.event.post(game_quit)

    @staticmethod
    def show_maze(maze, text=""):
        # Functions that initialises the game board, using a list of cells.
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
        if text == "win":
            myfont = pygame.font.SysFont("monospace", 15)
            label = myfont.render("YOU WON!", 1, (255, 255, 255))
            window.blit(label, (100, 100))
        elif text == "lost":
            myfont = pygame.font.SysFont("monospace", 15)
            label = myfont.render("GAME OVER", 1, (255, 255, 255))
            window.blit(label, (100, 100))
        pygame.display.flip()
