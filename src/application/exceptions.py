class ApplicationException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class TicketIsNotRegistered(ApplicationException):
    pass


class TicketIsRegistered(ApplicationException):
    pass


class EventNotFound(ApplicationException):
    pass


class RegistrationDeadlinePasses(ApplicationException):
    pass


class SeatNotAvailable(ApplicationException):
    pass


class ProviderTimeout(ApplicationException):
    pass


class ProviderError(ApplicationException):
    pass


class EventNotPublished(ApplicationException):
    pass


class EventAlreadyFinished(ApplicationException):
    pass
