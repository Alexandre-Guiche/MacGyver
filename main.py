from maze import *


def main():
    maze = Maze()
    maze.cells = maze.generate_maze_from_file()
    still_playing = 1
    while still_playing:
        maze.show_maze(maze)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                maze.get_direction(event)
            if event.type == pygame.QUIT:
                still_playing = 0