import pygame

from traffic_simulator.config import (
    WIDTH,
    HEIGHT,
    FPS,
    TITLE,
    BACKGROUND_COLOR,
)

from traffic_simulator.renderer import (
    draw_intersection,
    draw_vehicles,
)

from traffic_simulator.simulation import TrafficSimulation

def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT),
    )

    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    simulation = TrafficSimulation(
        seed=7
    )

    running = True

    while running:

        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

        simulation.update(dt)

        draw_intersection(screen)

        draw_vehicles(
            screen,
            simulation.lanes
        )

        pygame.display.flip()
      
    pygame.quit()

if __name__ == "__main__":
    main()