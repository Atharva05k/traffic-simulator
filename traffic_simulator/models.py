from collections import deque
from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


@dataclass
class Vehicle:
    vehicle_id: int
    direction: Direction
    distance_to_center: float
    speed: float

    wait_time: float = 0.0
    is_waiting: bool = False


@dataclass
class Lane:
    direction: Direction

    vehicles: deque = field(
        default_factory=deque
    )

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def remove_vehicle(self):
        if self.vehicles:
            return self.vehicles.popleft()

        return None

    def vehicle_count(self):
        return len(self.vehicles)