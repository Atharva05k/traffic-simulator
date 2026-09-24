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
    draw_traffic_lights,
)

from traffic_simulator.simulation import TrafficSimulation

from traffic_simulator.controller import (
    ControllerMode,
)

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

                elif event.key == pygame.K_a:

                    simulation.controller.set_mode(
                        ControllerMode.ADAPTIVE
                    )       

                    simulation.reset()

                    print(
                        "Controller mode: ADAPTIVE"
                    )

                elif event.key == pygame.K_f:
                    
                    simulation.controller.set_mode(
                        ControllerMode.FIXED
                    )

                    simulation.reset()

                    print(
                        "Controller mode: FIXED"
                    )

                elif event.key == pygame.K_r:

                    print(
                        f"Mode: "
                        f"{simulation.controller.mode.value}"
                    )

                    print(
                        f"Vehicles processed: "
                        f"{simulation.total_departed}"
                    )

                    print(
                        f"Average wait: "
                        f"{simulation.average_wait_time:.2f}s"
                    )

                    print(
                        f"Maximum wait: "
                        f"{simulation.max_wait_time:.2f}s"
                    )

                    print(
                        f"Vehicles currently queued: "
                        f"{simulation.total_queue}"
                    )

                    print("-" * 40)

                    simulation.reset()

                    print("Simulation reset")  

        simulation.update(dt)

        mode = simulation.controller.mode.value

        pygame.display.set_caption(
            f"{TITLE} | Mode: {mode}"
        )

        draw_intersection(screen)

        draw_traffic_lights(
            screen,
            simulation.controller,
        )

        draw_vehicles(
            screen,
            simulation.lanes,
        )

        pygame.display.flip()
      
    pygame.quit()

if __name__ == "__main__":
    main()