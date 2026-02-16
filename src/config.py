import logging
from src import (
    CarParking,
    parking_init,
    get_parking_slots,
    SlotsError,
    ParkingInitError,
)

# MAIN VARIABLES THAT CAN BE CHANGED
########################################################
# Number of parking slots
SMALL_SLOTS = 10
MEDIUM_SLOTS = 20
LARGE_SLOTS = 30

# Parking class
PARKING_CLASS = CarParking

########################################################
logging.basicConfig(
    filename="parking.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

try:
    slots = get_parking_slots(small=SMALL_SLOTS, medium=MEDIUM_SLOTS, large=LARGE_SLOTS)
except SlotsError as e:
    logging.error(f"Slots initialization error: {e}")
    print(e)
    exit(1)

try:
    parking = parking_init(parking_class=PARKING_CLASS, slots=slots)
except ParkingInitError as e:
    logging.error(f"Parking initialization error: {e}")
    print(e)
    exit(1)
