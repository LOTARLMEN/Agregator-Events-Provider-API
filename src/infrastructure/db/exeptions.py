from fastapi import HTTPException


class EventNotFoundException(HTTPException): ...


class TicketIsRegisteredException(HTTPException): ...


class SeatException(HTTPException): ...
