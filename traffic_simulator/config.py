WIDTH = 1000
HEIGHT = 700

FPS = 60

TITLE = "Traffic Simulator "

# -----------------------------
# INTERSECTION
# -----------------------------

ROAD_WIDTH = 240

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

ROAD_COLOR = (52, 56, 62)
BACKGROUND_COLOR = (165, 195, 150)

WHITE = (235, 235, 235)
YELLOW = (220, 185, 70)

# -----------------------------
# VEHICLES
# -----------------------------

VEHICLE_SPEED = 170.0

MIN_VEHICLE_GAP = 60

MIN_SPAWN_INTERVAL = 0.6
MAX_SPAWN_INTERVAL = 1.1

SPAWN_MARGIN = 70

EXIT_DISTANCE = 100

# -----------------------------
# TRAFFIC SIGNALS
# -----------------------------

FIXED_GREEN_DURATION = 6.0

MIN_GREEN_DURATION = 3.0
MAX_GREEN_DURATION = 8.0

YELLOW_DURATION = 1.5
ALL_RED_DURATION = 1.0

STOP_LINE_DISTANCE = (
    ROAD_WIDTH // 2 + 60
)

INTERSECTION_CLEAR_DISTANCE = (
    ROAD_WIDTH // 2 + 35
)