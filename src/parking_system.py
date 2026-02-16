import logging
import re
import uuid
from pathlib import Path
from typing import Dict, Literal
from src.parking_slots import Size, ParkingSlots
from src.exceptions import CarSizeError
from src.ticket_storage import (
    save_ticket_id_to_storage,
    retrieve_ticket_id_from_storage,
    TicketJsonFileStorage,
)

logger = logging.getLogger(__name__)


class ValetParking:
    """Abstract base class for a valet parking system."""

    def __init__(self, slots: ParkingSlots) -> None:
        raise NotImplementedError

    def park_car(self, car_size: Size) -> tuple[str, str]:
        """Parks a car of the given size and returns a ticket ID."""
        raise NotImplementedError

    def return_car(self, ticket_id: str, slot_size: Size) -> bool:
        """Returns a car associated with the given ticket ID."""
        raise NotImplementedError


# There is only CarParking here now. But we can easily add other
# parking classes: for example, TruckParking and etc.
class CarParking(ValetParking):
    """Concrete implementation of the valet parking system."""

    def __init__(self, slots: ParkingSlots):
        self._slots = slots
        self._active_tickets: Dict[str, Size] = {}

    def _generate_ticket_id(self) -> str:
        """Generates a unique ticket ID."""
        return str(uuid.uuid4())

    def park_car(self, car_size: Size) -> tuple[str, str]:
        """Internal logic to find a slot and park the car."""
        for slot_size in Size:
            if slot_size >= car_size and self._slots[slot_size] > 0:
                ticket_id = self._generate_ticket_id()
                save_ticket_id = save_ticket_id_to_storage(
                    TicketJsonFileStorage(Path.cwd() / "tickets.json"),
                    ticket_id,
                    slot_size,
                )

                if save_ticket_id:
                    self._slots[slot_size] -= 1
                    logger.info(
                        f"Parked car size {car_size.name} in slot {slot_size.name}. Ticket: {ticket_id}"
                    )
                return (ticket_id, slot_size.name)
        logger.warning(
            f"Failed to park car size {car_size.name}: No suitable slots found."
        )
        raise CarSizeError

    def return_car(self, ticket_id: str, slot_size: Size) -> bool:
        """Internal logic to retrieve a car and free the slot."""
        retrieve_ticket_id = retrieve_ticket_id_from_storage(
            TicketJsonFileStorage(Path.cwd() / "tickets.json"), ticket_id, slot_size
        )

        if retrieve_ticket_id:
            self._slots[slot_size] += 1
            logger.info(
                f"Returned car with ticket {ticket_id}. Freed slot {slot_size.name}."
            )
            return True
        logger.warning(f"Failed to return car: Ticket {ticket_id} not found.")
        return False


def parking_init(
    slots: ParkingSlots, parking_class: type[ValetParking]
) -> ValetParking:
    """Initializes the parking system with specific slots and class."""
    return parking_class(slots=slots)


def _action_park_car(parking: ValetParking, car_size: Size) -> None:
    """Parks a car of the given size and returns a ticket ID."""
    ticket_id, slot_size = parking.park_car(car_size)
    print(
        "Your car is succefully parked!\n "
        f"Your ticket_id is: {ticket_id}\n"
        f"Your parking_slot_size is: {slot_size}"
    )


def _action_return_car(parking: ValetParking, ticket_id: str, slot_size: Size) -> None:
    """Returns a car associated with the given ticket ID."""
    clean_ticket_id = re.sub(r"[^А-Яа-яA-Za-z0-9-]", "", ticket_id)
    result = parking.return_car(clean_ticket_id, slot_size)
    if result:
        print("Your car is succefully returned!")
    else:
        print("Something went wrong. Try again later!")


# Manages park system operations: return or park a car
def manage_car(
    parking: ValetParking,
    action: Literal["park"] | Literal["return"],
    size: Size,
    ticket_id: str | None = None,
) -> None:

    if action == "park":
        _action_park_car(parking, size)
    elif action == "return":
        if ticket_id is not None:
            _action_return_car(parking, ticket_id, size)
        else:
            ticket_id = input("Please, enter your ticket id: ")
            _action_return_car(parking, ticket_id, size)
    else:
        raise CarSizeError
