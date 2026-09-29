from traffic_simulator.config import (
    STOP_LINE_DISTANCE,
)

from traffic_simulator.models import (
    Direction,
    Lane,
    Vehicle,
)

from traffic_simulator.controller import (
    ControllerMode,
    SignalState,
    TrafficLightController,
    TrafficPhase,
)


def create_empty_lanes():

    return {
        direction: Lane(direction)
        for direction in Direction
    }


def test_controller_starts_in_adaptive_mode():

    controller = TrafficLightController()

    assert (
        controller.mode
        == ControllerMode.ADAPTIVE
    )

    assert (
        controller.phase
        == TrafficPhase.NORTH_SOUTH_GREEN
    )


def test_north_south_is_green_initially():

    controller = TrafficLightController()

    assert (
        controller.get_signal(
            Direction.NORTH
        )
        == SignalState.GREEN
    )

    assert (
        controller.get_signal(
            Direction.SOUTH
        )
        == SignalState.GREEN
    )

    assert (
        controller.get_signal(
            Direction.EAST
        )
        == SignalState.RED
    )


def test_fixed_mode_switches_after_timer():

    controller = TrafficLightController()

    controller.set_mode(
        ControllerMode.FIXED
    )

    lanes = create_empty_lanes()

    controller.update(
        6.0,
        lanes,
    )

    assert (
        controller.phase
        == TrafficPhase.NORTH_SOUTH_YELLOW
    )


def test_adaptive_mode_switches_for_larger_queue():

    controller = TrafficLightController()

    lanes = create_empty_lanes()

    # One vehicle waiting on North/South.
    lanes[Direction.NORTH].add_vehicle(
        Vehicle(
            vehicle_id=1,
            direction=Direction.NORTH,
            distance_to_center=STOP_LINE_DISTANCE,
            speed=0,
        )
    )

    # Three vehicles waiting on East/West.
    for vehicle_id in range(2, 5):

        lanes[Direction.EAST].add_vehicle(
            Vehicle(
                vehicle_id=vehicle_id,
                direction=Direction.EAST,
                distance_to_center=STOP_LINE_DISTANCE,
                speed=0,
            )
        )

    controller.update(
        3.1,
        lanes,
    )

    assert (
        controller.phase
        == TrafficPhase.NORTH_SOUTH_YELLOW
    )