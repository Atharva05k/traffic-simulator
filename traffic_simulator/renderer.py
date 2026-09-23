import pygame

from traffic_simulator.config import (
    WIDTH,
    HEIGHT,
    ROAD_WIDTH,
    BACKGROUND_COLOR,
    ROAD_COLOR,
    SIDEWALK_COLOR,
    WHITE,
    YELLOW,
    TEXT_COLOR,
)

from traffic_simulator.models import Direction

def draw_dashed_line(
        screen,
        color,
        start,
        end,
        dash_length = 20,
        gap_length = 15,
        width = 3,
):
    x1, y1 = start
    x2, y2 = end

    if x1 == x2:
        y = y1

        while y < y2:
            pygame.draw.line(
                screen,
                color,
                (x1, y),
                (x1, min(y + dash_length, y2)),
                width,
            )

            y += dash_length + gap_length

    elif y1 == y2:
        x = x1

        while x < x2:
            pygame.draw.line(
                screen,
                color,
                (x, y1),
                (min(x  + dash_length, x2), y1),
                width,
            )

            x += dash_length + gap_length


def draw_horizontal_crosswalk(screen, y):

    center_x = WIDTH // 2
    half_road = ROAD_WIDTH // 2

    stripe_width = 14
    gap = 10

    x = center_x - half_road + 10

    while x < center_x + half_road - 10:

        pygame.draw.rect(
            screen,
            WHITE,
            (
                x,
                y,
                stripe_width,
                32,
            ),
        )

        x += stripe_width + gap

def draw_vertical_crosswalk(screen, x):

    center_y = HEIGHT // 2
    half_road = ROAD_WIDTH // 2

    stripe_height = 14
    gap = 10

    y = center_y - half_road + 10

    while y < center_y + half_road - 10:

        pygame.draw.rect(
            screen,
            WHITE,
            (
                x,
                y,
                32,
                stripe_height,
            ),
        )

        y += stripe_height + gap

def draw_intersection(screen):

    screen.fill(BACKGROUND_COLOR)

    center_x  = WIDTH // 2
    center_y = HEIGHT // 2

    half_road = ROAD_WIDTH // 2

    sidewalk_size = 18

    # Sidewalks around the vertical road.

    pygame.draw.rect(
        screen,
        SIDEWALK_COLOR,
        (
            center_x - half_road - sidewalk_size,
            0,
            sidewalk_size,
            HEIGHT,
        ),
    )

    pygame.draw.rect(
        screen,
        SIDEWALK_COLOR,
        (
            center_x + half_road,
            0,
            sidewalk_size,
            HEIGHT,
        ),
    )

    # Sidewalks around the horizontal road.

    pygame.draw.rect(
        screen,
        SIDEWALK_COLOR,
        (
            0,
            center_y + half_road,
            WIDTH,
            sidewalk_size,
        ),
    )

    pygame.draw.rect(
        screen,
        SIDEWALK_COLOR,
        (
            0,
            center_y + half_road,
            WIDTH,
            sidewalk_size,
        ),
    )

    # Vertical road
    pygame.draw.rect(
        screen,
        ROAD_COLOR,
        (
            center_x - half_road,
            0,
            ROAD_WIDTH,
            HEIGHT,
        ),
    )

    # Horizontal Road
    pygame.draw.rect(
        screen,
        ROAD_COLOR,
        (
            0,
            center_y - half_road,
            WIDTH,
            ROAD_WIDTH,
        ),
    )

    # Vertical center markings
    draw_dashed_line(
        screen,
        YELLOW,
        (center_x, 0),
        (center_x, center_y - half_road),
    )

    draw_dashed_line(
        screen,
        YELLOW,
        (center_x, center_y + half_road),
        (center_x, HEIGHT),
    )


    # Horizontal center markings
    draw_dashed_line(
        screen,
        YELLOW,
        (0, center_y),
        (center_x - half_road, center_y),
    )

    draw_dashed_line(
        screen,
        YELLOW,
        (center_x + half_road, center_y),
        (WIDTH, center_y),
    )

    # Crosswalks
    draw_horizontal_crosswalk(
        screen,
        center_y - half_road - 45,
    )

    draw_horizontal_crosswalk(
        screen,
        center_y + half_road + 13,
    )

    draw_vertical_crosswalk(
        screen,
        center_x - half_road - 45,
    )

    draw_vertical_crosswalk(
        screen,
        center_x + half_road + 13,
    )

    draw_direction_labels(screen)

def draw_direction_labels(screen):

    font = pygame.font.Font(None, 30)

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    labels = {
        "NORTH": (center_x + 170, 40),
        "SOUTH": (center_x - 230, HEIGHT -60),
        "WEST": (40, center_y - 170),
        "EAST": (WIDTH - 100, center_y + 170),
    }

    for text, position in labels.items():

        surface = font.render(
            text,
            True,
            TEXT_COLOR,
        )

        screen.blit(
            surface,
            position,
        )

def draw_vehicles(screen,lanes):

    center_x = WIDTH // 2
    center_y = HEIGHT //2

    lane_offset = ROAD_WIDTH // 4

    car_colors = [
        (52, 152, 219),
        (231, 76, 60),
        (241, 196, 15),
        (46, 204, 113),
        (155, 89, 182),
    ]

    for direction, lane in lanes.items():

        for vehicle in lane.vehicles:

            distance = vehicle.distance_to_center

            if direction == Direction.NORTH:

                x = center_x - lane_offset
                y = center_y - distance

                width = 26
                height = 44

            elif direction == Direction.SOUTH:

                x = center_x + lane_offset
                y = center_y + distance

                width = 26
                height = 44

            elif direction == Direction.WEST:

                x = center_x - distance
                y = center_y + lane_offset

                width = 44
                height = 26

            else:

                x = center_x + distance
                y = center_y - lane_offset

                width = 44
                height = 26


            car_rect = pygame.Rect(
                0,
                0,
                width,
                height,
            )

            car_rect.center = (
                int(x),
                int(y),
            )

            color = car_colors[
                vehicle.vehicle_id
                % len(car_colors)
            ]

            pygame.draw.rect(
                screen,
                color,
                car_rect,
                border_radius=5,
            )

            pygame.draw.rect(
                screen,
                WHITE,
                car_rect,
                width=2,
                border_radius=5,
            )