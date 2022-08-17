from server.enums.base_enum import BaseEnum


class StatusEnum(str, BaseEnum):
    success = "Success"
    failure = "Failure"
