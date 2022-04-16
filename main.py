from asyncio import FastChildWatcher
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

cell_normal = pygame.transform.scale(pygame.image.load("./assets/cell_normal.gif"), (CELL_SIZE, CELL_SIZE))
cell_numbers = [pygame.transform.scale(pygame.image.load(f"./assets/cell_{i}.gif"), (CELL_SIZE, CELL_SIZE)) for i in range(9)]
cell_mine = pygame.transform.scale(pygame.image.load("./assets/cell_mine.gif"), (CELL_SIZE, CELL_SIZE))
cell_flagged = pygame.transform.scale(pygame.image.load("./assets/cell_marked.gif"), (CELL_SIZE, CELL_SIZE))

class Cell():
    row: int
    col: int
    mine: bool = False
    selected: bool = False
    flagged: bool = False
    mines_around: int = 0

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def show(self):
        pos = self.row * CELL_SIZE, self.col * CELL_SIZE
        if self.selected:
            if self.mine:
                win.blit(cell_mine, pos)
            else:
                win.blit(cell_numbers[self.mines_around], pos)
        else:
            win.blit(cell_normal, pos)


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
    field = []
    for row in range(ROWS):
        for col in range(COLS):
            field.append(Cell(row, col))
    
    mine_positions = set()
    while len(mine_positions) < mines:
        pos = random.randint(0, cells-1)
        if pos in mine_positions: continue
        mine_positions.add(pos)
        field[pos].mine = True
        for n in get_neighbours(pos):
            field[n].mines_around += 1

    return field


def draw(field):
    for cell in field:
        cell.show()
    pygame.display.update()


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
                i = pos[0] // CELL_SIZE * COLS + (pos[1] // CELL_SIZE)
                field[i].selected = True

        draw(field)

    pygame.quit()

run()