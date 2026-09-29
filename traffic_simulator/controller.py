from enum import Enum

from traffic_simulator.config import (
    FIXED_GREEN_DURATION,
    MIN_GREEN_DURATION,
    MAX_GREEN_DURATION,
    YELLOW_DURATION,
    ALL_RED_DURATION,
    STOP_LINE_DISTANCE,
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

        self.mode = ControllerMode.ADAPTIVE

        self.phase = (
            TrafficPhase.NORTH_SOUTH_GREEN
        )

        self.elapsed_time = 0.0


    def reset(self):

        self.phase = (
            TrafficPhase.NORTH_SOUTH_GREEN
        )

        self.elapsed_time = 0.0


    def set_mode(self, mode):

        self.mode = mode

        self.reset()


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


    def get_demand(
        self,
        directions,
        lanes,
    ):

        count = 0

        for direction in directions:

            for vehicle in lanes[
                direction
            ].vehicles:

                if (
                    vehicle.distance_to_center
                    >= STOP_LINE_DISTANCE
                ):

                    count += 1

        return count


    def handle_transition_phases(
        self,
        lanes,
    ):

        if (
            self.phase
            == TrafficPhase.NORTH_SOUTH_YELLOW
        ):

            if (
                self.elapsed_time
                >= YELLOW_DURATION
            ):

                self.change_phase(
                    TrafficPhase
                    .ALL_RED_TO_EAST_WEST
                )

            return True


        if (
            self.phase
            == TrafficPhase
            .ALL_RED_TO_EAST_WEST
        ):

            if (
                self.elapsed_time
                >= ALL_RED_DURATION
                and self.intersection_is_clear(
                    lanes
                )
            ):

                self.change_phase(
                    TrafficPhase
                    .EAST_WEST_GREEN
                )

            return True


        if (
            self.phase
            == TrafficPhase.EAST_WEST_YELLOW
        ):

            if (
                self.elapsed_time
                >= YELLOW_DURATION
            ):

                self.change_phase(
                    TrafficPhase
                    .ALL_RED_TO_NORTH_SOUTH
                )

            return True


        if (
            self.phase
            == TrafficPhase
            .ALL_RED_TO_NORTH_SOUTH
        ):

            if (
                self.elapsed_time
                >= ALL_RED_DURATION
                and self.intersection_is_clear(
                    lanes
                )
            ):

                self.change_phase(
                    TrafficPhase
                    .NORTH_SOUTH_GREEN
                )

            return True


        return False


    def update_fixed(
        self,
        dt,
        lanes,
    ):

        self.elapsed_time += dt


        if self.handle_transition_phases(
            lanes
        ):

            return


        if (
            self.phase
            == TrafficPhase.NORTH_SOUTH_GREEN
        ):

            if (
                self.elapsed_time
                >= FIXED_GREEN_DURATION
            ):

                self.change_phase(
                    TrafficPhase
                    .NORTH_SOUTH_YELLOW
                )


        elif (
            self.phase
            == TrafficPhase.EAST_WEST_GREEN
        ):

            if (
                self.elapsed_time
                >= FIXED_GREEN_DURATION
            ):

                self.change_phase(
                    TrafficPhase
                    .EAST_WEST_YELLOW
                )


    def update_adaptive(
        self,
        dt,
        lanes,
    ):

        self.elapsed_time += dt


        if self.handle_transition_phases(
            lanes
        ):

            return


        # Always allow a minimum amount
        # of green time first.
        if (
            self.elapsed_time
            < MIN_GREEN_DURATION
        ):

            return


        if (
            self.phase
            == TrafficPhase.NORTH_SOUTH_GREEN
        ):

            current_group = NORTH_SOUTH
            opposite_group = EAST_WEST

            yellow_phase = (
                TrafficPhase.NORTH_SOUTH_YELLOW
            )


        elif (
            self.phase
            == TrafficPhase.EAST_WEST_GREEN
        ):

            current_group = EAST_WEST
            opposite_group = NORTH_SOUTH

            yellow_phase = (
                TrafficPhase.EAST_WEST_YELLOW
            )


        else:

            return


        current_demand = self.get_demand(
            current_group,
            lanes,
        )

        opposite_demand = self.get_demand(
            opposite_group,
            lanes,
        )


        # No reason to switch if
        # the opposite road is empty.
        if opposite_demand == 0:

            return


        should_switch = False


        # Opposite road has more traffic.
        if (
            opposite_demand
            > current_demand
        ):

            should_switch = True


        # Current road has no traffic,
        # but opposite road does.
        elif current_demand == 0:

            should_switch = True


        # Prevent one road from holding
        # green indefinitely.
        elif (
            self.elapsed_time
            >= MAX_GREEN_DURATION
        ):

            should_switch = True


        if should_switch:

            self.change_phase(
                yellow_phase
            )


    def update(
        self,
        dt,
        lanes,
    ):

        if (
            self.mode
            == ControllerMode.FIXED
        ):

            self.update_fixed(
                dt,
                lanes,
            )

        else:

            self.update_adaptive(
                dt,
                lanes,
            )


    def get_signal(
        self,
        direction,
    ):

        if self.phase in (
            TrafficPhase.ALL_RED_TO_EAST_WEST,
            TrafficPhase.ALL_RED_TO_NORTH_SOUTH,
        ):

            return SignalState.RED


        if (
            self.phase
            == TrafficPhase.NORTH_SOUTH_GREEN
        ):

            if direction in NORTH_SOUTH:

                return SignalState.GREEN

            return SignalState.RED


        if (
            self.phase
            == TrafficPhase.NORTH_SOUTH_YELLOW
        ):

            if direction in NORTH_SOUTH:

                return SignalState.YELLOW

            return SignalState.RED


        if (
            self.phase
            == TrafficPhase.EAST_WEST_GREEN
        ):

            if direction in EAST_WEST:

                return SignalState.GREEN

            return SignalState.RED


        if (
            self.phase
            == TrafficPhase.EAST_WEST_YELLOW
        ):

            if direction in EAST_WEST:

                return SignalState.YELLOW

            return SignalState.RED


        return SignalState.RED