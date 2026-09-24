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
    STOP_LINE_DISTANCE,
    SIDEBAR_WIDTH,
    PANEL_COLOR,
    PANEL_TEXT_COLOR,
    MUTED_TEXT_COLOR,
    ACCENT_COLOR,
)

from traffic_simulator.models import Direction

from traffic_simulator.controller import SignalState

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

    draw_stop_lines(screen)
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

def draw_stop_lines(screen):

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    half_road = ROAD_WIDTH // 2

    # North Approach
    north_y = center_y - STOP_LINE_DISTANCE

    pygame.draw.line(
        screen,
        WHITE,
        (
            center_x - half_road + 10,
            north_y,
        ),
        (
            center_x - 10,
            north_y,
        ),
        5,
    )

    # South Approach
    south_y = center_y + STOP_LINE_DISTANCE
    
    pygame.draw.line(
        screen,
        WHITE,
        (
            center_x + 10,
            south_y,
        ),
        (
            center_x + half_road - 10,
            south_y,
        ),
        5,
    )

    # West Approach
    west_x = center_x - STOP_LINE_DISTANCE
    
    pygame.draw.line(
        screen,
        WHITE,
        (
            west_x,
            center_y + 10,
        ),
        (
            west_x,
            center_y + half_road - 10,
        ),
        5,
    )

    # East Approach
    east_x = center_x + STOP_LINE_DISTANCE
    
    pygame.draw.line(
        screen,
        WHITE,
        (
            east_x,
            center_y - half_road + 10,
        ),
        (
            east_x,
            center_y - 10,
        ),
        5,
    )

def draw_traffic_lights(
    screen,
    controller,
):

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    half_road = ROAD_WIDTH // 2

    signal_positions = {
        Direction.NORTH: (
            center_x - half_road - 30,
            center_y - half_road - 30,
        ),

        Direction.SOUTH: (
            center_x + half_road + 30,
            center_y + half_road + 30,
        ),

        Direction.WEST: (
            center_x - half_road - 30,
            center_y + half_road + 30,
        ),

        Direction.EAST: (
            center_x + half_road + 30,
            center_y - half_road - 30,
        ),
    }

    colors = {
        SignalState.RED: (220, 60, 60),
        SignalState.YELLOW: (240, 190, 40),
        SignalState.GREEN: (50, 200, 90),
    }

    for direction, position in signal_positions.items():

        signal = controller.get_signal(direction)

        pygame.draw.circle(
            screen,
            (30, 30, 30),
            position,
            15,
        )

        pygame.draw.circle(
            screen,
            colors[signal],
            position,
            10,
        )

def draw_dashboard(
    screen,
    simulation,
):

    panel_rect = pygame.Rect(
        0,
        0,
        SIDEBAR_WIDTH,
        HEIGHT,
    )

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        panel_rect,
    )

    title_font = pygame.font.Font(
        None,
        34,
    )

    heading_font = pygame.font.Font(
        None,
        25,
    )

    text_font = pygame.font.Font(
        None,
        22,
    )

    small_font = pygame.font.Font(
        None,
        19,
    )

    # Title
    title = title_font.render(
        "TRAFFIC SIMULATOR",
        True,
        PANEL_TEXT_COLOR,
    )

    screen.blit(
        title,
        (20, 25),
    )

    subtitle = small_font.render(
        "Adaptive Intersection",
        True,
        MUTED_TEXT_COLOR,
    )

    screen.blit(
        subtitle,
        (20, 60),
    )

    # Controller information
    mode = (
        simulation.controller.mode.value
    )

    phase = (
        simulation.controller.phase.value
    )

    mode_text = heading_font.render(
        f"Mode: {mode}",
        True,
        ACCENT_COLOR,
    )

    screen.blit(
        mode_text,
        (20, 105),
    )

    phase_text = small_font.render(
        phase.replace("_", " "),
        True,
        PANEL_TEXT_COLOR,
    )

    screen.blit(
        phase_text,
        (20, 140),
    )

    # Statistics
    y = 195

    stats = [
        (
            "Vehicles processed",
            simulation.total_departed,
        ),
        (
            "Vehicles waiting",
            simulation.total_queue,
        ),
        (
            "Average wait",
            f"{simulation.average_wait_time:.1f}s",
        ),
        (
            "Maximum wait",
            f"{simulation.max_wait_time:.1f}s",
        ),
    ]

    for label, value in stats:

        label_surface = text_font.render(
            label,
            True,
            MUTED_TEXT_COLOR,
        )

        value_surface = text_font.render(
            str(value),
            True,
            PANEL_TEXT_COLOR,
        )

        screen.blit(
            label_surface,
            (20, y),
        )

        screen.blit(
            value_surface,
            (190, y),
        )

        y += 32

    # Lane queues
    y += 20

    queue_heading = heading_font.render(
        "Lane Queues",
        True,
        PANEL_TEXT_COLOR,
    )

    screen.blit(
        queue_heading,
        (20, y),
    )

    y += 38

    for direction in Direction:

        count = (
            simulation
            .lanes[direction]
            .vehicle_count()
        )

        queue_text = text_font.render(
            f"{direction.value}: {count}",
            True,
            PANEL_TEXT_COLOR,
        )

        screen.blit(
            queue_text,
            (20, y),
        )

        y += 28

    # Controls
    y += 20

    controls_heading = heading_font.render(
        "Controls",
        True,
        PANEL_TEXT_COLOR,
    )

    screen.blit(
        controls_heading,
        (20, y),
    )

    y += 36

    controls = [
        "[A] Adaptive",
        "[F] Fixed",
        "[R] Reset",
        "[ESC] Exit",
    ]

    for control in controls:

        control_surface = small_font.render(
            control,
            True,
            MUTED_TEXT_COLOR,
        )

        screen.blit(
            control_surface,
            (20, y),
        )

        y += 25