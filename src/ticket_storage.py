from src.parking_slots import Size
from src.exceptions import (
    TicketNotFoundError,
    NotSavedTicketError,
    SaveStorageError,
    RetrieveStorageError,
)
from datetime import datetime
from typing import Optional, TypedDict
from pathlib import Path
import json


class TicketStorage:
    """Interface for any storage saving active parking tickets."""

    def __init__(self):
        raise NotImplementedError

    def save(self, ticket_id: str, slot_size: Size) -> bool:
        raise NotImplementedError

    def retrieve(self, ticket_id: str, slot_size: Size) -> bool:
        raise NotImplementedError


class TicketIdRecord(TypedDict):
    date: str
    ticket_id: str
    slot_size: Size


# self._active_tickets: Dict[str, Size] = {}
# ticket_id = str(uuid.uuid4())
# self._active_tickets[ticket_id] = size


class TicketJsonFileStorage(TicketStorage):

    def __init__(self, jsonfile: Path):
        self._jsonfile = jsonfile
        self._init_storage()

    def save(self, ticket_id: str, slot_size: Size) -> bool:
        try:
            parking_data = self._read_parking_data()
            parking_data.append(
                {
                    "date": str(datetime.now()),
                    "ticket_id": ticket_id,
                    "slot_size": slot_size,
                }
            )
            self._write_parking_data(parking_data)
        except NotSavedTicketError as e:
            print(e)
            print(
                f"\n Ticket: {ticket_id}, Slot_size: {slot_size}, Date: {str(datetime.now())}"
            )
            return False
        else:
            return True

    # def get_ticket_id_from_storage(self, ticket_id: str, slot_size: Size) -> Optional[str]:
    #     parking_data = self._read_parking_data()
    #     for record in parking_data:
    #         if record["ticket_id"] == ticket_id and record["slot_size"] == slot_size:
    #             return record["ticket_id"]
    #     return None

    def retrieve(self, ticket_id: str, slot_size: Size) -> bool:
        parking_data = self._read_parking_data()
        for i, record in enumerate(parking_data):
            if record["ticket_id"] == ticket_id and record["slot_size"] == slot_size:
                del parking_data[i]
                self._write_parking_data(parking_data)
                return True
        return False

    def _init_storage(self) -> None:
        if not self._jsonfile.exists():
            self._jsonfile.write_text("[]")

    def _read_parking_data(self) -> list[TicketIdRecord]:
        with open(self._jsonfile, "r") as f:
            return json.load(f)

    def _write_parking_data(self, parking_data: list[TicketIdRecord]) -> None:
        with open(self._jsonfile, "w") as f:
            json.dump(parking_data, f, ensure_ascii=False, indent=4)
            # self._jsonfile.write_text(str(history))


def save_ticket_id_to_storage(
    storage: TicketStorage, ticket_id: str, slot_size: Size
) -> bool:
    """Saves active parking tickets to storage"""
    try:
        if not storage.save(ticket_id, slot_size):
            raise SaveStorageError(f"Ticket {ticket_id} not saved")
        return True
    except SaveStorageError as e:
        print(e)
        return False


def retrieve_ticket_id_from_storage(
    storage: TicketStorage, ticket_id: str, slot_size: Size
) -> bool:
    """Retrieves active parking tickets from storage"""
    try:
        if not storage.retrieve(ticket_id, slot_size):
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")
        return True
    except TicketNotFoundError as e:
        print(e)
        return False
