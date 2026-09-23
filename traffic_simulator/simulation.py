import random

from traffic_simulator.config import (
    WIDTH,
    HEIGHT,
    VEHICLE_SPEED,
    MIN_SPAWN_INTERVAL,
    MAX_SPAWN_INTERVAL,
    MIN_VEHICLE_GAP,
    EXIT_DISTANCE,
    STOP_LINE_DISTANCE,
    SPAWN_MARGIN,
)

from traffic_simulator.models import (
    Direction,
    Lane,
    Vehicle,
)

from traffic_simulator.controller import (
    SignalState,
    TrafficLightController,
)

class TrafficSimulation:

    def __init__(self, seed=None):

        self.random = random.Random(seed)

        self.time = 0.0

        self.next_vehicle_id = 1

        self.spawn_timer = 0.0

        self.lanes = {
            direction: Lane(direction)
            for direction in Direction
        }

        self.controller = TrafficLightController()

    def get_spawn_distance(self, direction):

        if direction in (
            Direction.NORTH,
            Direction.SOUTH,
        ):
            return HEIGHT / 2 + SPAWN_MARGIN

        return WIDTH / 2 + SPAWN_MARGIN

    def can_spawn(self, lane, spawn_distance):

        if not lane.vehicles:
            return True

        last_vehicle = lane.vehicles[-1]

        return (
            last_vehicle.distance_to_center
            <= spawn_distance - MIN_VEHICLE_GAP
        )

    def spawn_vehicle(self):

        directions = list(Direction)

        self.random.shuffle(directions)

        for direction in directions:

            lane = self.lanes[direction]

            spawn_distance = self.get_spawn_distance(
                direction
            )

            if not self.can_spawn(
                lane,
                spawn_distance
            ):
                continue

            vehicle = Vehicle(
                vehicle_id=self.next_vehicle_id,
                direction=direction,
                spawn_time=self.time,
                distance_to_center=spawn_distance,
                speed=VEHICLE_SPEED,
            )

            lane.add_vehicle(vehicle)

            self.next_vehicle_id += 1

            return vehicle

        return None

    def update(self, dt):

        self.time += dt

        self.controller.update(dt)

        self.spawn_timer -= dt

        if self.spawn_timer <= 0:

            self.spawn_vehicle()

            self.spawn_timer = self.random.uniform(
                MIN_SPAWN_INTERVAL,
                MAX_SPAWN_INTERVAL,
            )

            for lane in self.lanes.values():

                vehicles = list(lane.vehicles)

                signal = self.controller.get_signal(
                    lane.direction
                )

                for index, vehicle in enumerate(vehicles):

                    new_distance = (
                        vehicle.distance_to_center
                        - vehicle.speed * dt
                    )

                    # Stop approaching vehicles at red/yellow lights.
                    if (
                        signal != SignalState.GREEN
                        and vehicle.distance_to_center
                        >= STOP_LINE_DISTANCE
                    ):

                        new_distance = max(
                            new_distance,
                            STOP_LINE_DISTANCE,
                        )

                    # Maintain safe distance from the vehicle ahead.
                    if index > 0:

                        vehicle_ahead = vehicles[
                            index - 1
                        ]

                        minimum_distance = (
                            vehicle_ahead.distance_to_center
                            + MIN_VEHICLE_GAP
                        )

                        new_distance = max(
                            new_distance,
                            minimum_distance,
                        )

                    vehicle.distance_to_center = new_distance

                while (
                    lane.vehicles
                    and lane.vehicles[0].distance_to_center
                    < -EXIT_DISTANCE
                ):
                    lane.remove_vehicle()

