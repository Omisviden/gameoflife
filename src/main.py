# Conway's Game of Life rules
# 
# For a space that is 'populated':
#     Each cell with one or no neighbors dies, as if by solitude. 
#     Each cell with four or more neighbors dies, as if by overpopulation. 
#     Each cell with two or three neighbors survives. 
# For a space that is 'empty' or 'unpopulated'
#     Each cell with three neighbors becomes populated.

from copy import deepcopy
import pygame, os

W, H = 20, 20

CELL = pygame.image.load(os.path.join("assets/cell.png"))
BG = pygame.image.load("assets/grid.png")
CHECK = pygame.image.load("assets/check.png")
UNCHECK = pygame.image.load("assets/uncheck.png")

ADJACENCY = [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)]
grid = [[0 for x in range(W)] for y in range(H)]

autorun = False
speed = 10

def get_adjacent_cells( x_coord, y_coord ):
    for dx, dy in ADJACENCY:
        if 0 <= (x_coord + dx) < W and 0 <= y_coord + dy < H: # Boundaries check
            yield grid[x_coord + dx][y_coord + dy]

def update():
    global grid
    new_grid = deepcopy(grid)
    


    for i in range(W):
        for j in range(H):
            neighbors = sum(get_adjacent_cells(i, j))

            if new_grid[i][j] == 0 and neighbors == 3:
                new_grid[i][j] = 1
            elif neighbors > 3 or neighbors < 2:
                new_grid[i][j] = 0
    grid = new_grid

def render(screen):
    screen.blit(BG, (0, 0))
    for i in range(W):
        for j in range(H):
            if grid[i][j] == 1:
                screen.blit(CELL, (2 + 22*i, 2 + 22*j))
    if autorun:
        screen.blit(CHECK, (0, 442))
    else:
        screen.blit(UNCHECK, (0, 442))


def main():

    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption("Conway's Game of Life")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((442, 482))
    # define a variable to control the main loop
    global speed, autorun
    running = True
    countdown = speed
    # main loop
    while running:

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    update()
                if event.key == pygame.K_a:
                    autorun = not(autorun)
                if event.key == pygame.K_p:
                    speed += 1
                if event.key == pygame.K_m:
                    speed -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                if 0 < pos[0] < 442 and 0 < pos[1] < 442:
                    if grid[pos[0]//22][pos[1]//22] == 1:
                        grid[pos[0]//22][pos[1]//22] = 0
                    else:
                        grid[pos[0]//22][pos[1]//22] = 1
                elif 0 < pos[0] < 66 and 442 < pos[1] < 482:
                    autorun = not(autorun)
        if autorun:
            countdown -= 1
            if countdown == 0:
                countdown = speed
                update()
        clock.tick(30)
        render(screen)
        pygame.display.flip()

if __name__=="__main__":
    main()