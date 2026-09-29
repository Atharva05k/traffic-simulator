import random

from traffic_simulator.config import (
    WIDTH,
    HEIGHT,
    CENTER_X,
    CENTER_Y,
    VEHICLE_SPEED,
    MIN_VEHICLE_GAP,
    MIN_SPAWN_INTERVAL,
    MAX_SPAWN_INTERVAL,
    SPAWN_MARGIN,
    EXIT_DISTANCE,
    STOP_LINE_DISTANCE,
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

    def __init__(
        self,
        seed=7,
    ):

        self.seed = seed

        self.random = random.Random(
            self.seed
        )

        self.time = 0.0

        self.next_vehicle_id = 1

        self.spawn_timer = 0.0

        self.total_departed = 0

        self.total_wait_time = 0.0

        self.max_wait_time = 0.0

        self.max_queue = 0

        self.lanes = {
            direction: Lane(direction)
            for direction in Direction
        }

        self.controller = (
            TrafficLightController()
        )


    @property
    def total_queue(self):

        return sum(
            self.get_queue_count(direction)
            for direction in Direction
        )


    @property
    def average_wait_time(self):

        if self.total_departed == 0:

            return 0.0

        return (
            self.total_wait_time
            / self.total_departed
        )


    def get_spawn_distance(
        self,
        direction,
    ):

        if direction == Direction.NORTH:

            return (
                CENTER_Y
                + SPAWN_MARGIN
            )


        if direction == Direction.SOUTH:

            return (
                HEIGHT
                - CENTER_Y
                + SPAWN_MARGIN
            )


        if direction == Direction.WEST:

            return (
                CENTER_X
                + SPAWN_MARGIN
            )


        return (
            WIDTH
            - CENTER_X
            + SPAWN_MARGIN
        )


    def can_spawn(
        self,
        lane,
        spawn_distance,
    ):

        if not lane.vehicles:

            return True


        newest_vehicle = (
            lane.vehicles[-1]
        )


        return (
            newest_vehicle.distance_to_center
            <= spawn_distance
            - MIN_VEHICLE_GAP
        )


    def spawn_vehicle(self):

        directions = list(Direction)

        self.random.shuffle(
            directions
        )


        for direction in directions:

            lane = self.lanes[
                direction
            ]

            spawn_distance = (
                self.get_spawn_distance(
                    direction
                )
            )


            if not self.can_spawn(
                lane,
                spawn_distance,
            ):

                continue


            vehicle = Vehicle(
                vehicle_id=(
                    self.next_vehicle_id
                ),
                direction=direction,
                distance_to_center=(
                    spawn_distance
                ),
                speed=VEHICLE_SPEED,
            )


            lane.add_vehicle(
                vehicle
            )

            self.next_vehicle_id += 1

            return


    def update(
        self,
        dt,
    ):

        self.time += dt


        # -----------------------------
        # UPDATE SIGNAL CONTROLLER
        # -----------------------------

        self.controller.update(
            dt,
            self.lanes,
        )


        # -----------------------------
        # SPAWN VEHICLES
        # -----------------------------

        self.spawn_timer -= dt


        if self.spawn_timer <= 0:

            self.spawn_vehicle()

            self.spawn_timer = (
                self.random.uniform(
                    MIN_SPAWN_INTERVAL,
                    MAX_SPAWN_INTERVAL,
                )
            )


        # -----------------------------
        # MOVE VEHICLES
        # -----------------------------

        for lane in self.lanes.values():

            vehicles = list(
                lane.vehicles
            )

            signal = (
                self.controller.get_signal(
                    lane.direction
                )
            )


            for index, vehicle in enumerate(
                vehicles
            ):

                old_distance = (
                    vehicle.distance_to_center
                )


                new_distance = (
                    old_distance
                    - vehicle.speed * dt
                )


                # Stop at red or yellow
                # before crossing stop line.
                if (
                    signal
                    != SignalState.GREEN
                    and old_distance
                    >= STOP_LINE_DISTANCE
                ):

                    new_distance = max(
                        new_distance,
                        STOP_LINE_DISTANCE,
                    )


                # Maintain distance from
                # vehicle in front.
                if index > 0:

                    vehicle_ahead = (
                        vehicles[index - 1]
                    )

                    minimum_distance = (
                        vehicle_ahead
                        .distance_to_center
                        + MIN_VEHICLE_GAP
                    )

                    new_distance = max(
                        new_distance,
                        minimum_distance,
                    )


                vehicle.distance_to_center = (
                    new_distance
                )


                vehicle.is_waiting = (
                    abs(
                        new_distance
                        - old_distance
                    )
                    < 0.01
                    and new_distance
                    >= STOP_LINE_DISTANCE
                )


                if vehicle.is_waiting:

                    vehicle.wait_time += dt


            # -------------------------
            # REMOVE EXITED VEHICLES
            # -------------------------

            while (
                lane.vehicles
                and lane.vehicles[0]
                .distance_to_center
                < -EXIT_DISTANCE
            ):

                departed_vehicle = (
                    lane.remove_vehicle()
                )


                self.total_departed += 1

                self.total_wait_time += (
                    departed_vehicle.wait_time
                )

                self.max_wait_time = max(
                    self.max_wait_time,
                    departed_vehicle.wait_time,
                )


        self.max_queue = max(
            self.max_queue,
            self.total_queue,
        )


    def get_queue_count(
        self,
        direction,
    ):

        lane = self.lanes[
            direction
        ]

        return sum(
            1
            for vehicle in lane.vehicles
            if vehicle.is_waiting
        )


    def reset(self):

        # Resetting the random generator
        # gives each controller the same
        # traffic pattern.
        self.random = random.Random(
            self.seed
        )

        self.time = 0.0

        self.next_vehicle_id = 1

        self.spawn_timer = 0.0

        self.total_departed = 0

        self.total_wait_time = 0.0

        self.max_wait_time = 0.0

        self.max_queue = 0


        self.lanes = {
            direction: Lane(direction)
            for direction in Direction
        }


        self.controller.reset()