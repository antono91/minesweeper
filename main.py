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
MINES = 5


def create_field(mines, cells): 
    field = [-1]*cells
    while field.count(9) < mines:
        field[random.randint(0, cells-1)] = 9
    return field

field = create_field(MINES, CELLS)

face_down = pygame.transform.scale(pygame.image.load("./assets/facingDown.png"), (CELL_SIZE, CELL_SIZE))
numbers = [pygame.transform.scale(pygame.image.load(f"./assets/{i}.png"), (CELL_SIZE, CELL_SIZE)) for i in range(9)]
bomb = pygame.transform.scale(pygame.image.load("./assets/bomb.png"), (CELL_SIZE, CELL_SIZE))


def count_bombs(row, col):
    DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    count = 0
    for DIR in DIRECTIONS:
        r_to_check = row + DIR[0]
        c_to_check = col + DIR[1]
        if 0 <= r_to_check < ROWS and 0 <= c_to_check < COLS:
            i = r_to_check * COLS + c_to_check
            if field[i] == 9:
                count +=1
    return count


def draw(win):
    for i, c in enumerate(field):
        x = i % ROWS * CELL_SIZE
        y = i // ROWS * CELL_SIZE
        if c == -1:
            win.blit(face_down, (x, y))
        elif c in range(9):
            win.blit(numbers[c], (x, y))
        else:
            win.blit(bomb, (x, y))
            

def reveal_cell(pos):
    col = pos[0] // CELL_SIZE
    row = pos[1] // CELL_SIZE
    field[row * COLS + col] = count_bombs(row, col)
    

    


def run():
    running = True
    while running:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                reveal_cell(pos)
                print(field)

        # Game Logic
        draw(win)
        pygame.display.flip()       

    pygame.quit()

run()