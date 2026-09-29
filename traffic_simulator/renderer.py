from pathlib import Path

import pygame

from traffic_simulator.config import (
    WIDTH,
    HEIGHT,
    ROAD_WIDTH,
    CENTER_X,
    CENTER_Y,
    ROAD_COLOR,
    BACKGROUND_COLOR,
    WHITE,
    YELLOW,
    STOP_LINE_DISTANCE,
)

from traffic_simulator.models import (
    Direction,
)

from traffic_simulator.controller import (
    SignalState,
)


ASSET_DIR = (
    Path(__file__).resolve().parent.parent
    / "assets"
)

CAR_IMAGES = None


def draw_dashed_line(
    screen,
    color,
    start,
    end,
):

    x1, y1 = start
    x2, y2 = end

    dash_length = 20
    gap = 14


    if x1 == x2:

        y = y1

        while y < y2:

            pygame.draw.line(
                screen,
                color,
                (x1, y),
                (
                    x1,
                    min(
                        y + dash_length,
                        y2,
                    ),
                ),
                2,
            )

            y += (
                dash_length + gap
            )


    else:

        x = x1

        while x < x2:

            pygame.draw.line(
                screen,
                color,
                (x, y1),
                (
                    min(
                        x + dash_length,
                        x2,
                    ),
                    y1,
                ),
                2,
            )

            x += (
                dash_length + gap
            )


def draw_intersection(
    screen,
):

    screen.fill(
        BACKGROUND_COLOR
    )

    half_road = (
        ROAD_WIDTH // 2
    )


    # Vertical road
    pygame.draw.rect(
        screen,
        ROAD_COLOR,
        (
            CENTER_X - half_road,
            0,
            ROAD_WIDTH,
            HEIGHT,
        ),
    )


    # Horizontal road
    pygame.draw.rect(
        screen,
        ROAD_COLOR,
        (
            0,
            CENTER_Y - half_road,
            WIDTH,
            ROAD_WIDTH,
        ),
    )


    # Vertical centre lines
    draw_dashed_line(
        screen,
        YELLOW,
        (
            CENTER_X,
            0,
        ),
        (
            CENTER_X,
            CENTER_Y - half_road,
        ),
    )


    draw_dashed_line(
        screen,
        YELLOW,
        (
            CENTER_X,
            CENTER_Y + half_road,
        ),
        (
            CENTER_X,
            HEIGHT,
        ),
    )


    # Horizontal centre lines
    draw_dashed_line(
        screen,
        YELLOW,
        (
            0,
            CENTER_Y,
        ),
        (
            CENTER_X - half_road,
            CENTER_Y,
        ),
    )


    draw_dashed_line(
        screen,
        YELLOW,
        (
            CENTER_X + half_road,
            CENTER_Y,
        ),
        (
            WIDTH,
            CENTER_Y,
        ),
    )


    draw_stop_lines(
        screen
    )

    draw_crosswalks(
        screen
    )


def draw_stop_lines(
    screen,
):

    half_road = (
        ROAD_WIDTH // 2
    )


    north_y = (
        CENTER_Y
        - STOP_LINE_DISTANCE
    )

    south_y = (
        CENTER_Y
        + STOP_LINE_DISTANCE
    )

    west_x = (
        CENTER_X
        - STOP_LINE_DISTANCE
    )

    east_x = (
        CENTER_X
        + STOP_LINE_DISTANCE
    )


    pygame.draw.line(
        screen,
        WHITE,
        (
            CENTER_X
            - half_road + 10,
            north_y,
        ),
        (
            CENTER_X - 10,
            north_y,
        ),
        5,
    )


    pygame.draw.line(
        screen,
        WHITE,
        (
            CENTER_X + 10,
            south_y,
        ),
        (
            CENTER_X
            + half_road - 10,
            south_y,
        ),
        5,
    )


    pygame.draw.line(
        screen,
        WHITE,
        (
            west_x,
            CENTER_Y + 10,
        ),
        (
            west_x,
            CENTER_Y
            + half_road - 10,
        ),
        5,
    )


    pygame.draw.line(
        screen,
        WHITE,
        (
            east_x,
            CENTER_Y
            - half_road + 10,
        ),
        (
            east_x,
            CENTER_Y - 10,
        ),
        5,
    )


def draw_crosswalks(
    screen,
):

    half_road = (
        ROAD_WIDTH // 2
    )

    stripe_size = 10
    gap = 10


    # Top and bottom crosswalks
    for x in range(
        CENTER_X - half_road + 15,
        CENTER_X + half_road - 15,
        stripe_size + gap,
    ):

        pygame.draw.rect(
            screen,
            WHITE,
            (
                x,
                CENTER_Y
                - half_road - 35,
                stripe_size,
                20,
            ),
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (
                x,
                CENTER_Y
                + half_road + 15,
                stripe_size,
                20,
            ),
        )


    # Left and right crosswalks
    for y in range(
        CENTER_Y - half_road + 15,
        CENTER_Y + half_road - 15,
        stripe_size + gap,
    ):

        pygame.draw.rect(
            screen,
            WHITE,
            (
                CENTER_X
                - half_road - 35,
                y,
                20,
                stripe_size,
            ),
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (
                CENTER_X
                + half_road + 15,
                y,
                20,
                stripe_size,
            ),
        )


def load_car_images():

    global CAR_IMAGES


    if CAR_IMAGES is not None:

        return CAR_IMAGES


    filenames = [
        "car_red.png",
        "car_yellow.png",
        "car_blue.png",
        "car_green.png",
    ]


    CAR_IMAGES = []


    for filename in filenames:

        path = (
            ASSET_DIR
            / filename
        )


        image = pygame.image.load(
            str(path)
        ).convert_alpha()


        image = (
            pygame.transform.smoothscale(
                image,
                (30, 50),
            )
        )


        CAR_IMAGES.append(
            image
        )


    return CAR_IMAGES


def draw_vehicles(
    screen,
    lanes,
):

    lane_offset = (
        ROAD_WIDTH // 4
    )

    car_images = (
        load_car_images()
    )


    for direction, lane in lanes.items():

        for vehicle in lane.vehicles:

            distance = (
                vehicle.distance_to_center
            )


            image = car_images[
                vehicle.vehicle_id
                % len(car_images)
            ]


            if (
                direction
                == Direction.NORTH
            ):

                x = (
                    CENTER_X
                    - lane_offset
                )

                y = (
                    CENTER_Y
                    - distance
                )

                angle = 180


            elif (
                direction
                == Direction.SOUTH
            ):

                x = (
                    CENTER_X
                    + lane_offset
                )

                y = (
                    CENTER_Y
                    + distance
                )

                angle = 0


            elif (
                direction
                == Direction.WEST
            ):

                x = (
                    CENTER_X
                    - distance
                )

                y = (
                    CENTER_Y
                    + lane_offset
                )

                angle = -90


            else:

                x = (
                    CENTER_X
                    + distance
                )

                y = (
                    CENTER_Y
                    - lane_offset
                )

                angle = 90


            rotated = (
                pygame.transform.rotate(
                    image,
                    angle,
                )
            )


            rect = (
                rotated.get_rect(
                    center=(
                        int(x),
                        int(y),
                    )
                )
            )


            screen.blit(
                rotated,
                rect,
            )


def draw_signal(
    screen,
    signal,
    position,
):

    housing = pygame.Rect(
        0,
        0,
        20,
        54,
    )

    housing.center = position


    pygame.draw.rect(
        screen,
        (30, 30, 30),
        housing,
        border_radius=5,
    )


    colors = {
        SignalState.RED:
            (230, 55, 55),

        SignalState.YELLOW:
            (235, 190, 45),

        SignalState.GREEN:
            (50, 200, 90),
    }


    bulb_positions = {
        SignalState.RED:
            (
                housing.centerx,
                housing.top + 10,
            ),

        SignalState.YELLOW:
            (
                housing.centerx,
                housing.centery,
            ),

        SignalState.GREEN:
            (
                housing.centerx,
                housing.bottom - 10,
            ),
    }


    for state, position in (
        bulb_positions.items()
    ):

        color = (
            colors[state]
            if signal == state
            else (70, 70, 70)
        )

        pygame.draw.circle(
            screen,
            color,
            position,
            6,
        )


def draw_traffic_lights(
    screen,
    controller,
):

    half_road = (
        ROAD_WIDTH // 2
    )


    positions = {

        Direction.NORTH: (
            CENTER_X
            - half_road - 22,

            CENTER_Y
            - half_road - 22,
        ),

        Direction.SOUTH: (
            CENTER_X
            + half_road + 22,

            CENTER_Y
            + half_road + 22,
        ),

        Direction.WEST: (
            CENTER_X
            - half_road - 22,

            CENTER_Y
            + half_road + 22,
        ),

        Direction.EAST: (
            CENTER_X
            + half_road + 22,

            CENTER_Y
            - half_road - 22,
        ),
    }


    for direction, position in (
        positions.items()
    ):

        signal = (
            controller.get_signal(
                direction
            )
        )


        draw_signal(
            screen,
            signal,
            position,
        )


def draw_dashboard(
    screen,
    simulation,
):

    panel = pygame.Rect(
        15,
        15,
        265,
        185,
    )


    pygame.draw.rect(
        screen,
        (25, 30, 38),
        panel,
        border_radius=10,
    )


    title_font = pygame.font.Font(
        None,
        28,
    )

    text_font = pygame.font.Font(
        None,
        20,
    )


    title = title_font.render(
        "TRAFFIC SIMULATOR",
        True,
        WHITE,
    )


    screen.blit(
        title,
        (
            panel.x + 15,
            panel.y + 12,
        ),
    )


    mode = (
        simulation.controller.mode.value
    )

    phase = (
        simulation.controller
        .phase.value
        .replace("_", " ")
    )


    lines = [
        f"Mode: {mode}",
        f"Phase: {phase}",
        (
            "Processed: "
            f"{simulation.total_departed}"
        ),
        (
            "Currently waiting: "
            f"{simulation.total_queue}"
        ),
        (
            "Average wait: "
            f"{simulation.average_wait_time:.1f}s"
        ),
        (
            "Max queue: "
            f"{simulation.max_queue}"
        ),
    ]


    y = panel.y + 48


    for line in lines:

        surface = text_font.render(
            line,
            True,
            WHITE,
        )

        screen.blit(
            surface,
            (
                panel.x + 15,
                y,
            ),
        )

        y += 21


    controls = text_font.render(
        "A Adaptive | F Fixed | R Reset",
        True,
        (190, 195, 205),
    )


    screen.blit(
        controls,
        (
            15,
            HEIGHT - 28,
        ),
    )