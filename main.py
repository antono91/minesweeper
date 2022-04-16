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
    field = [0]*cells
    while field.count(1) < mines:
        field[random.randint(0, cells-1)] = 1
    return field

field = create_field(MINES, CELLS)
print(sum(field), field)

face_down = pygame.transform.scale(pygame.image.load("./assets/facingDown.png"), (CELL_SIZE, CELL_SIZE))

def draw(win):
    for i in range(CELLS):
        x = i % ROWS * CELL_SIZE
        y = i // ROWS * CELL_SIZE
        win.blit(face_down, (x, y))
    


def run():

    running = True
    while running:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game Logic
        draw(win)
        pygame.display.flip()       

    pygame.quit()

run()