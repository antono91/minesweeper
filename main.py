import pygame
import random

from zmq import EVENT_CLOSE_FAILED

pygame.init()

WIDTH, HEIGHT = 400, 400

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Minesweeper")

FPS = 30
BG_COLOR = "white"
ROWS, COLS = 10, 10
CELLS = ROWS * COLS
CELL_SIZE = WIDTH // ROWS
MINES = 5

cell_normal = pygame.transform.scale(pygame.image.load(
    "./assets/cell_normal.gif"), (CELL_SIZE, CELL_SIZE))
cell_numbers = [pygame.transform.scale(pygame.image.load(
    f"./assets/cell_{i}.gif"), (CELL_SIZE, CELL_SIZE)) for i in range(9)]
cell_mine = pygame.transform.scale(pygame.image.load(
    "./assets/cell_mine.gif"), (CELL_SIZE, CELL_SIZE))
cell_flagged = pygame.transform.scale(pygame.image.load(
    "./assets/cell_marked.gif"), (CELL_SIZE, CELL_SIZE))
cell_mine_exploded = pygame.transform.scale(pygame.image.load(
    "./assets/cell_mine_exploded.gif"), (CELL_SIZE, CELL_SIZE))



class Cell():
    row: int
    col: int
    mine: bool = False
    exploded: bool = False
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
                if self.exploded:
                    win.blit(cell_mine_exploded, pos)
                else:
                    win.blit(cell_mine, pos)
            else:
                win.blit(cell_numbers[self.mines_around], pos)
        else:
            if self.flagged:
                win.blit(cell_flagged, pos)
            else:
                win.blit(cell_normal, pos)


def get_neighbours(i):
    neighbours = []
    DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                  (1, 0), (1, -1), (0, -1), (-1, -1)]
    row, col = i // ROWS, i % ROWS
    for DIR in DIRECTIONS:
        r_to_check = row + DIR[0]
        c_to_check = col + DIR[1]
        if 0 <= r_to_check < ROWS and 0 <= c_to_check < COLS:
            neighbours.append(r_to_check * COLS + c_to_check)
    return neighbours


def flood_fill(pos, field):
    for n in get_neighbours(pos):
        if field[n].mines_around == 0 and not field[n].selected:
            field[n].selected = True   
            flood_fill(n, field)
        field[n].selected = True


def create_field(mines, cells):
    field = []
    for n in range(CELLS):
        field.append(Cell(n // ROWS, n % ROWS))

    mine_positions = set()
    while len(mine_positions) < mines:
        pos = random.randint(0, cells-1)
        if pos in mine_positions:
            continue
        mine_positions.add(pos)
        field[pos].mine = True
        for n in get_neighbours(pos):
            field[n].mines_around += 1

    return field


def draw(field):
    for cell in field:
        cell.show()
    pygame.display.update()


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
                p = (pos[0] // CELL_SIZE) * COLS + (pos[1] // CELL_SIZE)
                cell = field[p]
                if event.button == 1:
                    cell.selected = True
                    if cell.mine:
                        # game over
                        cell.exploded = True
                        for c in field:
                            c.selected = True
                    elif cell.mines_around == 0:
                        flood_fill(p, field)


                elif event.button == 3:
                    cell.flagged = not cell.flagged

        draw(field)

    pygame.quit()


run()
