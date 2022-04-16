from operator import ne
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 200, 200

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Minesweeper")

FPS = 30
BG_COLOR = "white"
ROWS, COLS = 10, 10
CELLS = ROWS * COLS
CELL_SIZE = 20
MINES = 10

face_down = pygame.transform.scale(pygame.image.load("./assets/facingDown.png"), (CELL_SIZE, CELL_SIZE))
numbers = [pygame.transform.scale(pygame.image.load(f"./assets/{i}.png"), (CELL_SIZE, CELL_SIZE)) for i in range(9)]
bomb = pygame.transform.scale(pygame.image.load("./assets/bomb.png"), (CELL_SIZE, CELL_SIZE))

def get_neighbours(i):
    neighbours = []
    DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    row, col = i // ROWS, i % ROWS
    for DIR in DIRECTIONS:
        r_to_check = row + DIR[0]
        c_to_check = col + DIR[1]
        if 0 <= r_to_check < ROWS and 0 <= c_to_check < COLS:
            neighbours.append(r_to_check * COLS + c_to_check)
    return neighbours


def create_field(mines, cells):
    field = [0]*cells
    mine_positions = set()
    while len(mine_positions) < mines:
        pos = random.randint(0, cells-1)
        if pos in mine_positions: continue
        mine_positions.add(pos)
        for neighbour in get_neighbours(pos):
            field[neighbour] += 1
    
    for i in mine_positions:
        field[i] = 9 
    return field


def draw(win, field):
    for i, c in enumerate(field):
        x, y = i % ROWS * CELL_SIZE, i // ROWS * CELL_SIZE
        if c == 0:
            win.blit(face_down, (x, y))
        elif c in range(8):
            win.blit(numbers[c], (x, y))
        else:
            win.blit(bomb, (x, y))
            
    pygame.display.flip()           


def reveal_cell(pos):
    pass


def run():
    field = create_field(MINES, CELLS)
    running = True
    while running:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Game Logic

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                reveal_cell(pos)

        draw(win, field)

    pygame.quit()

run()