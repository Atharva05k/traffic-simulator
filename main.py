import pygame

from traffic_simulator.config import (
    WIDTH,
    HEIGHT,
    FPS,
    TITLE,
    BACKGROUND_COLOR,
)

def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(BACKGROUND_COLOR)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()