class ParkingSystemErrors(Exception):
    """Base exception for parking system errors."""

    def __init__(self, message="Base exception for parking system errors."):
        super().__init__(message)


class TicketStorageErrors(Exception):
    """Base exception for ticket storage errors."""

    def __init__(self, message="Base exception for ticket storage errors."):
        super().__init__(message)


class CarSizeError(ParkingSystemErrors):
    def __init__(self, message="Invalid car size is provided."):
        super().__init__(message)


class SlotsError(ParkingSystemErrors):
    def __init__(self, message="Issue with parking slots configuration."):
        super().__init__(message)


class ParkingInitError(ParkingSystemErrors):
    def __init__(self, message="Parking system initialization fails."):
        super().__init__(message)


class ManageCarError(ParkingSystemErrors):
    def __init__(self, message="Error during car management operations."):
        super().__init__(message)


class SaveStorageError(TicketStorageErrors):
    def __init__(self, message="Error in saving ticket_id to storage."):
        super().__init__(message)


class NotSavedTicketError(SaveStorageError):
    def __init__(self, message="Ticket not saved to storage."):
        super().__init__(message)


class RetrieveStorageError(TicketStorageErrors):
    def __init__(self, message="Error in retrieving ticket_id from storage."):
        super().__init__(message)


class TicketNotFoundError(RetrieveStorageError):
    def __init__(self, message="Ticket not found in storage."):
        super().__init__(message)
