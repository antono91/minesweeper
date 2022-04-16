import pygame

pygame.init()

WIDTH, HEIGHT = 700, 800

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Minesweeper")

FPS = 60
BG_COLOR = "white"

def draw():
    pass


def run():

    running = True
    while running:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game Logic
        win.fill(BG_COLOR)

        pygame.display.flip()       

    pygame.quit()

run()