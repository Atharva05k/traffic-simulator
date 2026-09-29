import pygame

from traffic_simulator.config import (
    WIDTH,
    HEIGHT,
    FPS,
    TITLE,
)

from traffic_simulator.simulation import (
    TrafficSimulation,
)

from traffic_simulator.controller import (
    ControllerMode,
)

from traffic_simulator.renderer import (
    draw_intersection,
    draw_traffic_lights,
    draw_vehicles,
    draw_dashboard,
)


def main():

    pygame.init()


    screen = pygame.display.set_mode(
        (
            WIDTH,
            HEIGHT,
        )
    )


    clock = pygame.time.Clock()


    simulation = (
        TrafficSimulation(
            seed=7
        )
    )


    running = True


    while running:

        dt = (
            clock.tick(FPS)
            / 1000.0
        )


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False


            if event.type == pygame.KEYDOWN:

                if (
                    event.key
                    == pygame.K_ESCAPE
                ):

                    running = False


                elif (
                    event.key
                    == pygame.K_a
                ):

                    simulation.controller.set_mode(
                        ControllerMode.ADAPTIVE
                    )

                    simulation.reset()

                    print(
                        "Mode: ADAPTIVE"
                    )


                elif (
                    event.key
                    == pygame.K_f
                ):

                    simulation.controller.set_mode(
                        ControllerMode.FIXED
                    )

                    simulation.reset()

                    print(
                        "Mode: FIXED"
                    )


                elif (
                    event.key
                    == pygame.K_r
                ):

                    simulation.reset()

                    print(
                        "Simulation reset"
                    )


        simulation.update(
            dt
        )


        pygame.display.set_caption(
            f"{TITLE} | "
            f"{simulation.controller.mode.value}"
        )


        draw_intersection(
            screen
        )


        draw_traffic_lights(
            screen,
            simulation.controller,
        )


        draw_vehicles(
            screen,
            simulation.lanes,
        )


        draw_dashboard(
            screen,
            simulation,
        )


        pygame.display.flip()


    pygame.quit()


if __name__ == "__main__":

    main()