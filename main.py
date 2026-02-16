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
