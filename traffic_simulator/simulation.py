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
    TrafficPhase,
)

class TrafficSimulation:

    @property
    def total_queue(self):

        return sum(
            lane.vehicle_count()
            for lane in self.lanes.values()
        )
    @property
    def average_wait_time(self):

        if self.total_departed == 0:
            return 0.0

        return (
            self.total_wait_time
            / self.total_departed
        )
    
    def __init__(self, seed=None):

        self.random = random.Random(seed)

        self.time = 0.0

        self.next_vehicle_id = 1

        self.spawn_timer = 0.0

        self.total_departed = 0

        self.total_wait_time = 0.0

        self.max_wait_time = 0.0

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

        self.controller.update(dt, self.lanes,)

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

                    old_distance = vehicle.distance_to_center

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

                    if (
                        abs(new_distance - old_distance) < 0.01
                        and vehicle.distance_to_center >= STOP_LINE_DISTANCE
                    ):
                        vehicle.wait_time += dt

                while (
                    lane.vehicles
                    and lane.vehicles[0].distance_to_center
                    < -EXIT_DISTANCE
                ):
                    departed_vehicle = (
                        lane.remove_vehicle()
                    )

                    if departed_vehicle is not None:

                        self.total_departed += 1

                        self.total_wait_time += (
                            departed_vehicle.wait_time
                        )

                        self.max_wait_time = max(
                            self.max_wait_time,
                            departed_vehicle.wait_time,
                        )

    def reset(self):

        self.time = 0.0

        self.next_vehicle_id = 1

        self.spawn_timer = 0.0

        self.total_departed = 0

        self.total_wait_time = 0.0

        self.max_wait_time = 0.0

        self.lanes = {
            direction: Lane(direction)
            for direction in Direction
        }

        self.controller.phase = (
            TrafficPhase.NORTH_SOUTH_GREEN
        )

        self.controller.elapsed_time = 0.0