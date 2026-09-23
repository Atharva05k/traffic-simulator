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
    spawn_time: float

    distance_to_center: float = 0.0
    speed: float = 120.0

@dataclass
class Lane:
    direction: Direction

    vehicles: deque[Vehicle] = field(
        default_factory=deque
    )

    def add_vehicle(self, vehicle:Vehicle):
        self.vehicles.append(vehicle)

    def remove_vehicle(self):
        if self.vehicles:
            return self.vehicles.popleft()

        return None

    def next_vehicle(self):
        if self.vehicles:
            return self.vehicles[0]

        return None

    def vehicle_count(self):
        return len(self.vehicles)