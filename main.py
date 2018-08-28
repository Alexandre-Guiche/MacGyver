from maze import *


def main():
    # main loop that stops when the player reaches the guard, either it won or lost (or quits manually)
    maze = Maze()
    still_playing = 1
    while still_playing:
        maze.show_maze(maze)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                maze.get_direction(event)
            if event.type == pygame.QUIT:
                still_playing = 0
