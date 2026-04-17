from enum import Enum


class EventStatus(str, Enum):
    PUBLISHED = "published"
    DRAFT = "draft"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    REGISTRATION_CLOSED = "registration_closed"
