from enum import Enum

from traffic_simulator.config import (
    MIN_GREEN_DURATION,
    MAX_GREEN_DURATION,
    YELLOW_DURATION,
    QUEUE_WEIGHT,
    WAIT_WEIGHT,
    SWITCH_MULTIPLIER,
    STARVATION_LIMIT,
    STOP_LINE_DISTANCE,
)
from traffic_simulator.models import Direction

class SignalState(Enum):
   RED = "RED"
   YELLOW = "YELLOW"
   GREEN = "GREEN"

class TrafficPhase(Enum):
    NORTH_SOUTH_GREEN = "NORTH_SOUTH_GREEEN"
    NORTH_SOUTH_YELLOW = "NORTH_SOUTH_YELLOW"
    EAST_WEST_GREEN = "EAST_WEST_GREEN"
    EAST_WEST_YELLOW = "EAST_WEST_YELLOW"

NORTH_SOUTH = (
    Direction.NORTH,
    Direction.SOUTH,
)

EAST_WEST = (
    Direction.EAST,
    Direction.WEST,
)

class TrafficLightController:

    def __init__(self):

        self.phase = TrafficPhase.NORTH_SOUTH_GREEN

        self.elapsed_time = 0.0

    def change_phase(self, new_phase):

        self.phase = new_phase
        self.elapsed_time = 0.0

    def get_group_metrics(
        self,
        directions,
        lanes,
    ):

        queue_count = 0
        longest_wait = 0.0

        for direction in directions:

            lane = lanes[direction]

            for vehicle in lane.vehicles:

                if (
                    vehicle.distance_to_center
                    >= STOP_LINE_DISTANCE
                ):

                    queue_count += 1

                    longest_wait = max(
                        longest_wait,
                        vehicle.wait_time,
                    )

        score = (
            queue_count * QUEUE_WEIGHT
            + longest_wait * WAIT_WEIGHT
        )

        return (
            score,
            queue_count,
            longest_wait,
        )

    def update(self, dt, lanes):

        self.elapsed_time += dt

         # Yellow phases have fixed duration.

        if self.phase == TrafficPhase.NORTH_SOUTH_YELLOW:

            if self.elapsed_time >= YELLOW_DURATION:

                self.change_phase(
                    TrafficPhase.EAST_WEST_GREEN
                )

            return

        if self.phase == TrafficPhase.EAST_WEST_YELLOW:

            if self.elapsed_time >= YELLOW_DURATION:

                self.change_phase(
                    TrafficPhase.NORTH_SOUTH_GREEN
                )

            return

        # Determine which direction currently has green.

        if self.phase == TrafficPhase.NORTH_SOUTH_GREEN:

            current_group = NORTH_SOUTH
            opposing_group = EAST_WEST

            yellow_phase = (
                TrafficPhase.NORTH_SOUTH_YELLOW
            )

        else:

            current_group = EAST_WEST
            opposing_group = NORTH_SOUTH

            yellow_phase = (
                TrafficPhase.EAST_WEST_YELLOW
            )

        # Always provide a minimum green time.

        if self.elapsed_time < MIN_GREEN_DURATION:
            return

        (
            current_score,
            current_queue,
            current_wait,
        ) = self.get_group_metrics(
            current_group,
            lanes,
        )

        (
            opposing_score,
            opposing_queue,
            opposing_wait,
        ) = self.get_group_metrics(
            opposing_group,
            lanes,
        )

        # Nobody is waiting on the opposite side.
        if opposing_queue == 0:
            return

        should_switch = False

        # Maximum green reached.
        if self.elapsed_time >= MAX_GREEN_DURATION:

            should_switch = True

        # Current road has no demand.
        elif current_queue == 0:

            should_switch = True

        # Prevent a road from waiting forever.
        elif opposing_wait >= STARVATION_LIMIT:

            should_switch = True

        # Opposite road is significantly busier.
        elif (
            opposing_score
            > current_score * SWITCH_MULTIPLIER
        ):

            should_switch = True

        if should_switch:

            self.change_phase(
                yellow_phase
            )

    def get_signal(self, direction):

        if self.phase == TrafficPhase.NORTH_SOUTH_GREEN:

            if direction in NORTH_SOUTH:
                return SignalState.GREEN

            return SignalState.RED

        if self.phase == TrafficPhase.NORTH_SOUTH_YELLOW:

            if direction in NORTH_SOUTH:
                return SignalState.YELLOW

            return SignalState.RED

        if self.phase == TrafficPhase.EAST_WEST_GREEN:

            if direction in EAST_WEST:
                return SignalState.GREEN

            return SignalState.RED

        if direction in EAST_WEST:
            return SignalState.YELLOW

        return SignalState.RED
