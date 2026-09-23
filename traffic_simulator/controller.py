from enum import Enum

from traffic_simulator.config import (
    GREEN_DURATION,
    YELLOW_DURATION,
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
    EAST_WEST_YELLLOW = "EAST_WEST_YELLOW"

class TrafficLightController:

    def __init__(self):

        self.phase = TrafficPhase.NORTH_SOUTH_GREEN

        self.elapsed_time = 0.0

    def update(self,dt):

        self.elapsed_time += dt

        if self.phase == TrafficPhase.NORTH_SOUTH_GREEN:

            if self.elapsed_time >= GREEN_DURATION:

                self.phase = (
                    TrafficPhase.NORTH_SOUTH_YELLOW
                )

                self.elapsed_time = 0.0

        elif self.phase == TrafficPhase.NORTH_SOUTH_YELLOW:

            if self.elapsed_time >= YELLOW_DURATION:

                self.phase = (
                    TrafficPhase.EAST_WEST_GREEN
                )

                self.elapsed_time = 0.0

        elif self.phase == TrafficPhase.EAST_WEST_GREEN:

            if self.elapsed_time >= GREEN_DURATION:

                self.phase = (
                    TrafficPhase.EAST_WEST_YELLLOW
                )

                self.elapsed_time = 0.0

        elif self.phase == TrafficPhase.EAST_WEST_YELLLOW:

            if self.elapsed_time >= YELLOW_DURATION:

                self.phase = (
                    TrafficPhase.NORTH_SOUTH_GREEN
                )

                self.elapsed_time = 0.0

    def get_signal(self, direction):

        north_south = (
            Direction.NORTH,
            Direction.SOUTH,
        )

        east_west = (
            Direction.EAST,
            Direction.WEST,
        )

        if self.phase == TrafficPhase.NORTH_SOUTH_GREEN:

            if direction in north_south:
                return SignalState.GREEN

            return SignalState.RED

        if self.phase == TrafficPhase.NORTH_SOUTH_YELLOW:

            if direction in north_south:
                return SignalState.YELLOW

            return SignalState.RED

        if self.phase == TrafficPhase.EAST_WEST_GREEN:

            if direction in east_west:
                return SignalState.GREEN

            return SignalState.RED

        if direction in east_west:
            return SignalState.YELLOW

        return SignalState.RED
