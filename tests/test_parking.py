import pytest
import uuid
from unittest.mock import patch, MagicMock

# Import classes and functions from the project
from src.parking_slots import get_parking_slots, Size, ParkingSlots
from src.exceptions import SlotsError, CarSizeError
from src.parking_system import CarParking, parking_init


# --- Fixtures ---


@pytest.fixture
def empty_slots() -> ParkingSlots:
    """Returns a ParkingSlots object with 0 slots of each size."""
    return get_parking_slots(0, 0, 0)


@pytest.fixture
def standard_slots() -> ParkingSlots:
    """Returns a ParkingSlots object with 10 small, 20 medium, and 30 large slots."""
    return get_parking_slots(10, 20, 30)


@pytest.fixture
def limited_slots() -> ParkingSlots:
    """Returns a ParkingSlots object with 1 slot of each size."""
    return get_parking_slots(1, 1, 1)


# --- Tests for parking_slots.py ---


def test_get_parking_slots_success():
    """Tests successful creation of ParkingSlots."""
    slots = get_parking_slots(5, 10, 15)
    assert isinstance(slots, ParkingSlots)
    assert slots[Size.SMALL] == 5
    assert slots[Size.MEDIUM] == 10
    assert slots[Size.LARGE] == 15


def test_get_parking_slots_raises_error_on_negative_values():
    """Tests that SlotsError is raised for negative slot values."""
    with pytest.raises(SlotsError):
        get_parking_slots(-1, 10, 10)
    with pytest.raises(SlotsError):
        get_parking_slots(10, -1, 10)
    with pytest.raises(SlotsError):
        get_parking_slots(10, 10, -1)


def test_parking_slots_getitem(standard_slots: ParkingSlots):
    """Tests the __getitem__ method for ParkingSlots."""
    assert standard_slots[Size.SMALL] == 10
    assert standard_slots[Size.MEDIUM] == 20
    assert standard_slots[Size.LARGE] == 30


def test_parking_slots_setitem(standard_slots: ParkingSlots):
    """Tests the __setitem__ method for ParkingSlots."""
    standard_slots[Size.SMALL] = 5
    assert standard_slots[Size.SMALL] == 5
    standard_slots[Size.MEDIUM] = 15
    assert standard_slots[Size.MEDIUM] == 15
    standard_slots[Size.LARGE] = 25
    assert standard_slots[Size.LARGE] == 25


def test_parking_slots_iteration_and_length(standard_slots: ParkingSlots):
    """Tests iteration and length of ParkingSlots."""
    sizes = list(standard_slots)
    assert len(sizes) == 3
    assert len(standard_slots) == 3
    assert Size.SMALL in sizes
    assert Size.MEDIUM in sizes
    assert Size.LARGE in sizes


# --- Tests for parking_system.py ---


def test_parking_init(standard_slots: ParkingSlots):
    """Tests the parking_init function."""
    parking = parking_init(slots=standard_slots, parking_class=CarParking)
    assert isinstance(parking, CarParking)
    assert parking._slots is standard_slots


@pytest.fixture
def parking_system(limited_slots: ParkingSlots) -> CarParking:
    """Returns a CarParking system with 1 slot of each size."""
    return CarParking(limited_slots)


@patch("src.parking_system.TicketJsonFileStorage")
@patch("src.parking_system.save_ticket_id_to_storage")
def test_park_small_car_in_small_slot(
    mock_save, mock_storage, parking_system: CarParking
):
    """Tests parking a small car in an available small slot."""
    mock_save.return_value = True
    ticket_id, slot_name = parking_system.park_car(Size.SMALL)

    assert ticket_id is not None
    assert slot_name == Size.SMALL.name
    assert parking_system._slots[Size.SMALL] == 0


@patch("src.parking_system.TicketJsonFileStorage")
@patch("src.parking_system.save_ticket_id_to_storage")
def test_park_small_car_in_medium_slot(mock_save, mock_storage):
    """Tests parking a small car in a medium slot when small slots are occupied."""
    slots = get_parking_slots(small=0, medium=1, large=1)
    parking = CarParking(slots)
    mock_save.return_value = True

    ticket_id, slot_name = parking.park_car(Size.SMALL)

    assert ticket_id is not None
    assert slot_name == Size.MEDIUM.name
    assert parking._slots[Size.SMALL] == 0
    assert parking._slots[Size.MEDIUM] == 0


@patch("src.parking_system.TicketJsonFileStorage")
@patch("src.parking_system.save_ticket_id_to_storage")
def test_park_small_car_in_large_slot(mock_save, mock_storage):
    """Tests parking a small car in a large slot when small and medium slots are occupied."""
    slots = get_parking_slots(small=0, medium=0, large=1)
    parking = CarParking(slots)
    mock_save.return_value = True

    ticket_id, slot_name = parking.park_car(Size.SMALL)

    assert ticket_id is not None
    assert slot_name == Size.LARGE.name
    assert parking._slots[Size.LARGE] == 0


@patch("src.parking_system.TicketJsonFileStorage")
@patch("src.parking_system.save_ticket_id_to_storage")
def test_park_medium_car_in_large_slot(mock_save, mock_storage):
    """Tests parking a medium car in a large slot when medium slots are occupied."""
    slots = get_parking_slots(small=1, medium=0, large=1)
    parking = CarParking(slots)
    mock_save.return_value = True

    ticket_id, slot_name = parking.park_car(Size.MEDIUM)

    assert ticket_id is not None
    assert slot_name == Size.LARGE.name
    assert parking._slots[Size.LARGE] == 0


def test_no_slots_for_small_car(empty_slots: ParkingSlots):
    """Tests that a small car cannot be parked when all slots are occupied."""
    parking = CarParking(empty_slots)
    with pytest.raises(CarSizeError):
        parking.park_car(Size.SMALL)


def test_no_slots_for_medium_car():
    """Tests that a medium car cannot be parked when only small slots are available."""
    slots = get_parking_slots(small=1, medium=0, large=0)
    parking = CarParking(slots)
    with pytest.raises(CarSizeError):
        parking.park_car(Size.MEDIUM)


def test_no_slots_for_large_car():
    """Tests that a large car cannot be parked when only small/medium slots are available."""
    slots = get_parking_slots(small=1, medium=1, large=0)
    parking = CarParking(slots)
    with pytest.raises(CarSizeError):
        parking.park_car(Size.LARGE)


@patch("src.parking_system.TicketJsonFileStorage")
@patch("src.parking_system.save_ticket_id_to_storage")
@patch("src.parking_system.retrieve_ticket_id_from_storage")
def test_return_car_success(
    mock_retrieve, mock_save, mock_storage, parking_system: CarParking
):
    """Tests successful car return with a valid ticket."""
    mock_save.return_value = True
    mock_retrieve.return_value = True

    ticket_id, slot_name = parking_system.park_car(Size.MEDIUM)
    assert parking_system._slots[Size.MEDIUM] == 0

    result = parking_system.return_car(ticket_id, Size.MEDIUM)
    assert result is True
    assert parking_system._slots[Size.MEDIUM] == 1


@patch("src.parking_system.TicketJsonFileStorage")
@patch("src.parking_system.retrieve_ticket_id_from_storage")
def test_return_car_invalid_ticket(
    mock_retrieve, mock_storage, parking_system: CarParking
):
    """Tests car return with an invalid or non-existent ticket."""
    mock_retrieve.return_value = False

    fake_ticket = str(uuid.uuid4())
    result = parking_system.return_car(fake_ticket, Size.SMALL)
    assert result is False
    # Slot count should remain unchanged (1 for limited_slots)
    assert parking_system._slots[Size.SMALL] == 1
