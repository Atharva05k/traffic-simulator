from enum import Enum

from traffic_simulator.config import (
    FIXED_GREEN_DURATION,
    MIN_GREEN_DURATION,
    MAX_GREEN_DURATION,
    YELLOW_DURATION,
    QUEUE_WEIGHT,
    WAIT_WEIGHT,
    SWITCH_MULTIPLIER,
    STARVATION_LIMIT,
    STOP_LINE_DISTANCE,
    ALL_RED_DURATION,
    INTERSECTION_CLEAR_DISTANCE,
)
from traffic_simulator.models import Direction

class SignalState(Enum):
   RED = "RED"
   YELLOW = "YELLOW"
   GREEN = "GREEN"

class ControllerMode(Enum):
    FIXED = "FIXED"
    ADAPTIVE = "ADAPTIVE"

class TrafficPhase(Enum):
    NORTH_SOUTH_GREEN = "NORTH_SOUTH_GREEN"
    NORTH_SOUTH_YELLOW = "NORTH_SOUTH_YELLOW"
    ALL_RED_TO_EAST_WEST = "ALL_RED_TO_EAST_WEST"
    EAST_WEST_GREEN = "EAST_WEST_GREEN"
    EAST_WEST_YELLOW = "EAST_WEST_YELLOW"
    ALL_RED_TO_NORTH_SOUTH = "ALL_RED_TO_NORTH_SOUTH"

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

        self.mode = ControllerMode.ADAPTIVE

    def change_phase(self, new_phase):

        self.phase = new_phase
        self.elapsed_time = 0.0

    def intersection_is_clear(
        self,
        lanes,
    ):

        for lane in lanes.values():

            for vehicle in lane.vehicles:

                if (
                    abs(
                        vehicle.distance_to_center
                    )
                    <= INTERSECTION_CLEAR_DISTANCE
                ):

                    return False

        return True    

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

    def update_adaptive(self, dt, lanes):

        self.elapsed_time += dt

        # -----------------------------------
        # YELLOW / ALL-RED TRANSITION PHASES
        # -----------------------------------

        if self.phase == TrafficPhase.NORTH_SOUTH_YELLOW:

            if self.elapsed_time >= YELLOW_DURATION:

                self.change_phase(
                    TrafficPhase.ALL_RED_TO_EAST_WEST
                )

            return


        if self.phase == TrafficPhase.ALL_RED_TO_EAST_WEST:

            if (
                self.elapsed_time >= ALL_RED_DURATION
                and self.intersection_is_clear(
                    lanes
                )
            ):

                self.change_phase(
                    TrafficPhase.EAST_WEST_GREEN
                )

            return


        if self.phase == TrafficPhase.EAST_WEST_YELLOW:

            if self.elapsed_time >= YELLOW_DURATION:

                self.change_phase(
                    TrafficPhase.ALL_RED_TO_NORTH_SOUTH
                )

            return


        if self.phase == TrafficPhase.ALL_RED_TO_NORTH_SOUTH:

            if (
                self.elapsed_time >= ALL_RED_DURATION
                and self.intersection_is_clear(
                    lanes
                )
            ):

                self.change_phase(
                    TrafficPhase.NORTH_SOUTH_GREEN
                )

            return


        # -----------------------------------
        # DETERMINE CURRENT GREEN DIRECTION
        # -----------------------------------

        if self.phase == TrafficPhase.NORTH_SOUTH_GREEN:

            current_group = NORTH_SOUTH
            opposing_group = EAST_WEST

            yellow_phase = (
                TrafficPhase.NORTH_SOUTH_YELLOW
            )

        elif self.phase == TrafficPhase.EAST_WEST_GREEN:

            current_group = EAST_WEST
            opposing_group = NORTH_SOUTH

            yellow_phase = (
                TrafficPhase.EAST_WEST_YELLOW
            )

        else:
            return


        # -----------------------------------
        # MINIMUM GREEN TIME
        # -----------------------------------

        if self.elapsed_time < MIN_GREEN_DURATION:
            return


        # -----------------------------------
        # CALCULATE TRAFFIC DEMAND
        # -----------------------------------

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


        # No reason to switch if nobody
        # is waiting on the other road.
        if opposing_queue == 0:
            return


        # -----------------------------------
        # DECIDE WHETHER TO SWITCH
        # -----------------------------------

        should_switch = False

        # Green has lasted too long.
        if self.elapsed_time >= MAX_GREEN_DURATION:

            should_switch = True

        # Current road has no waiting traffic.
        elif current_queue == 0:

            should_switch = True

        # Prevent opposite road starvation.
        elif opposing_wait >= STARVATION_LIMIT:

            should_switch = True

        # Opposite side has much higher demand.
        elif (
            opposing_score
            > current_score * SWITCH_MULTIPLIER
        ):

            should_switch = True


        # -----------------------------------
        # BEGIN SAFE SIGNAL TRANSITION
        # -----------------------------------

        if should_switch:

            self.change_phase(
                yellow_phase
            )

    def update_fixed(self, dt, lanes):

        self.elapsed_time += dt

        if self.phase == TrafficPhase.NORTH_SOUTH_GREEN:

            if self.elapsed_time >= FIXED_GREEN_DURATION:

                self.change_phase(
                    TrafficPhase.NORTH_SOUTH_YELLOW
                )

        elif self.phase == TrafficPhase.NORTH_SOUTH_YELLOW:

            if self.elapsed_time >= YELLOW_DURATION:

                self.change_phase(
                    TrafficPhase.ALL_RED_TO_EAST_WEST
                )

        elif (
            self.phase
            == TrafficPhase.ALL_RED_TO_EAST_WEST
        ):

            if (
                self.elapsed_time
                >= ALL_RED_DURATION
                and self.intersection_is_clear(
                    lanes
                )
            ):

                self.change_phase(
                    TrafficPhase.EAST_WEST_GREEN
                )

        elif self.phase == TrafficPhase.EAST_WEST_GREEN:

            if self.elapsed_time >= FIXED_GREEN_DURATION:

                self.change_phase(
                    TrafficPhase.EAST_WEST_YELLOW
                )

        elif self.phase == TrafficPhase.EAST_WEST_YELLOW:

            if self.elapsed_time >= YELLOW_DURATION:

                self.change_phase(
                    TrafficPhase.ALL_RED_TO_NORTH_SOUTH
                )

        elif (
            self.phase
            == TrafficPhase.ALL_RED_TO_NORTH_SOUTH
        ):

            if (
                self.elapsed_time
                >= ALL_RED_DURATION
                and self.intersection_is_clear(
                    lanes
                )
            ):

                self.change_phase(
                    TrafficPhase.NORTH_SOUTH_GREEN
                )

    def update(self, dt, lanes):

        if self.mode == ControllerMode.FIXED:

            self.update_fixed(dt, lanes,)

        else:

            self.update_adaptive(
                dt,
                lanes,
            )

    def get_signal(self, direction):

        if self.phase in (
            TrafficPhase.ALL_RED_TO_EAST_WEST,
            TrafficPhase.ALL_RED_TO_NORTH_SOUTH,
        ):

            return SignalState.RED


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


        if self.phase == TrafficPhase.EAST_WEST_YELLOW:

            if direction in EAST_WEST:
                return SignalState.YELLOW

            return SignalState.RED


        return SignalState.RED

    def set_mode(self, mode):

        if not isinstance(mode, ControllerMode):
            raise ValueError(
                "mode must be a ControllerMode"
            )

        self.mode = mode

        self.phase = (
            TrafficPhase.NORTH_SOUTH_GREEN
        )

        self.elapsed_time = 0.0