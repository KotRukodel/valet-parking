from typing import Any, Mapping, NamedTuple
from enum import IntEnum
from src.exceptions import SlotsError


class Size(IntEnum):
    """Enumeration for parking slot sizes."""

    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Slots(NamedTuple):
    """Immutable container for initial slot counts."""

    small_slots: int
    medium_slots: int
    large_slots: int


class ParkingSlots(Mapping[Size, int]):
    """Manages the count of available parking slots for each size."""

    def __init__(self, slots: Slots) -> None:
        self._small_slots = slots.small_slots
        self._medium_slots = slots.medium_slots
        self._large_slots = slots.large_slots

    def __iter__(self) -> Any:
        """Iterates over available slot sizes."""
        return iter([Size.SMALL, Size.MEDIUM, Size.LARGE])

    def __len__(self) -> int:
        """Returns the number of slot types."""
        return 3

    def __getitem__(self, key: Size) -> int:
        """Retrieves the number of available slots for a given size."""
        if key == Size.SMALL:
            return self._small_slots
        elif key == Size.MEDIUM:
            return self._medium_slots
        elif key == Size.LARGE:
            return self._large_slots

    def __setitem__(self, name: Size, value: int) -> None:
        """Updates the number of available slots for a given size."""
        if name == Size.SMALL:
            self._small_slots = value
        elif name == Size.MEDIUM:
            self._medium_slots = value
        elif name == Size.LARGE:
            self._large_slots = value


def get_parking_slots(small: int, medium: int, large: int) -> ParkingSlots:
    """Factory function to create a ParkingSlots instance with validation."""
    if small < 0 or medium < 0 or large < 0:
        raise SlotsError
    get_slots_number = Slots(small_slots=small, medium_slots=medium, large_slots=large)
    return ParkingSlots(get_slots_number)
