# Valet Parking System

A robust Valet Parking System implemented in Python using Object-Oriented Programming (OOP) principles. This system efficiently manages parking slot allocation based on vehicle and slot size compatibility.

## 📋 Overview

The system implements the following business logic:
1.  **3 Car Types**: Small, Medium, Large.
2.  **3 Parking Slot Sizes**: Small, Medium, Large.
3.  **Parking Rules**: A car can be parked in a slot of its own size or larger.
    *   *Small Car* → Small, Medium, or Large Slot.
    *   *Medium Car* → Medium or Large Slot.
    *   *Large Car* → Large Slot only.

## 🏗 Project Structure

```text
valet-parking/
├── main.py                # Main script to run the system
├── requirements.txt       # Project dependencies
└── src/
    ├── __init__.py        # Package initialization
    ├── config.py          # Configuration (Number of slots, parking class)
    ├── exceptions.py      # Errors and Exceptions
    ├── parking_slots.py   # Sizes and Slots descriptions 
    ├── parking_system.py  # Core ValetParking logic
    └── ticket_storage.py  # Ticket storage description and logic
└── tests/
    ├── __init__.py        # Package initialization
    ├── test_parking.py    # Parking system tests
```

## 🛠 Installation and Setup

### Prerequisites
*   Python 3.10 or higher

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KotRukodel/valet-parking.git
    cd valet-parking
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    
    # Windows:
    .\venv\Scripts\activate
    
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

The system uses a 'manage_car' function to handle the allocation and retrieval of vehicles.

```python
from src import manage_car, ManageCarError, Size
from src.config import parking
import logging

log = logging.getLogger(__name__)


def main():
    """Here you can try to launch parking system actions and check its work"""
    try:
        manage_car(
            parking,
            action="park",  # you can change action
            size=Size.SMALL,  # you can change size: SMALL, MEDIUM or LARGE
            ticket_id="1d89ab4d-7bd8-4a76-8a7e-7a8e398260a0",  # you can change ticket_id
        )
    except ManageCarError as e:
        log.error(f"Car management error: {e}")
        print(e)
        exit(1)


if __name__ == "__main__":
    main()