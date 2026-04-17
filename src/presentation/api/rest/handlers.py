from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.application import exceptions as ex


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


async def provider_timeout(
    request: Request,
    exc: ex.ProviderTimeout,
):
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={"detail": exc.message},
    )


async def ticket_not_reg_handler(
    request: Request,
    exc: ex.TicketIsNotRegistered,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


async def ticket_already_exist_handler(
    request: Request,
    exc: ex.TicketIsRegistered,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )


async def event_not_found_handler(
    request: Request,
    exc: ex.EventNotFound,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


async def reg_deadline_handler(
    request: Request,
    exc: ex.RegistrationDeadlinePasses,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )


async def seat_not_available_handler(
    request: Request,
    exc: ex.SeatNotAvailable,
):
    return JSONResponse(
        status_code=status.HTTP_400_NOT_FOUND,
        content={"detail": exc.message},
    )


async def provider_errors_handler(
    request: Request,
    exc: ex.ProviderError,
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message},
    )


async def event_not_published_handler(
    request: Request,
    exc: ex.EventNotPublished,
):
    return JSONResponse(
        status_code=status.HTTP_400_NOT_FOUND,
        content={"detail": exc.message},
    )


async def event_already_finished_handler(
    request: Request, exc: ex.EventAlreadyFinished
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


handlers_mapping = {
    RequestValidationError: validation_error_handler,
    ex.ProviderError: provider_errors_handler,
    ex.EventNotPublished: event_not_published_handler,
    ex.EventAlreadyFinished: event_already_finished_handler,
    ex.ProviderTimeout: provider_timeout,
    ex.TicketIsNotRegistered: ticket_not_reg_handler,
    ex.TicketIsRegistered: ticket_already_exist_handler,
    ex.EventNotFound: event_not_found_handler,
    ex.RegistrationDeadlinePasses: reg_deadline_handler,
}
