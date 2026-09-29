from traffic_simulator.config import (
    VEHICLE_SPEED,
    MIN_VEHICLE_GAP,
    STOP_LINE_DISTANCE,
)

from traffic_simulator.models import (
    Direction,
    Vehicle,
)

from traffic_simulator.simulation import (
    TrafficSimulation,
)


def test_green_vehicle_moves():

    simulation = TrafficSimulation(seed=7)

    # Prevent random spawning during test.
    simulation.spawn_timer = 999

    vehicle = Vehicle(
        vehicle_id=1,
        direction=Direction.NORTH,
        distance_to_center=STOP_LINE_DISTANCE + 100,
        speed=VEHICLE_SPEED,
    )

    simulation.lanes[
        Direction.NORTH
    ].add_vehicle(vehicle)

    start_distance = (
        vehicle.distance_to_center
    )

    simulation.update(0.1)

    assert (
        vehicle.distance_to_center
        < start_distance
    )


def test_red_vehicle_stops_at_stop_line():

    simulation = TrafficSimulation(seed=7)

    simulation.spawn_timer = 999

    # East is RED initially because
    # North/South starts GREEN.
    vehicle = Vehicle(
        vehicle_id=1,
        direction=Direction.EAST,
        distance_to_center=STOP_LINE_DISTANCE,
        speed=VEHICLE_SPEED,
    )

    simulation.lanes[
        Direction.EAST
    ].add_vehicle(vehicle)

    simulation.update(0.1)

    assert (
        vehicle.distance_to_center
        == STOP_LINE_DISTANCE
    )

    assert vehicle.is_waiting is True


def test_vehicle_gap_is_preserved():

    simulation = TrafficSimulation(seed=7)

    simulation.spawn_timer = 999

    front_vehicle = Vehicle(
        vehicle_id=1,
        direction=Direction.NORTH,
        distance_to_center=STOP_LINE_DISTANCE + 100,
        speed=VEHICLE_SPEED,
    )

    back_vehicle = Vehicle(
        vehicle_id=2,
        direction=Direction.NORTH,
        distance_to_center=STOP_LINE_DISTANCE + 150,
        speed=VEHICLE_SPEED,
    )

    lane = simulation.lanes[
        Direction.NORTH
    ]

    lane.add_vehicle(front_vehicle)
    lane.add_vehicle(back_vehicle)

    simulation.update(0.1)

    gap = (
        back_vehicle.distance_to_center
        - front_vehicle.distance_to_center
    )

    assert gap >= MIN_VEHICLE_GAP


def test_reset_repeats_same_random_traffic():

    simulation = TrafficSimulation(seed=7)

    simulation.spawn_vehicle()

    first_direction = next(
        direction
        for direction, lane
        in simulation.lanes.items()
        if lane.vehicles
    )

    simulation.reset()

    simulation.spawn_vehicle()

    second_direction = next(
        direction
        for direction, lane
        in simulation.lanes.items()
        if lane.vehicles
    )

    assert (
        first_direction
        == second_direction
    )