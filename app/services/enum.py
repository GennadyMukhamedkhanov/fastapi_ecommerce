from enum import StrEnum, auto
from strenum import UppercaseStrEnum


class UserRoles(StrEnum):
    seller = auto()
    buyer = auto()


class UserRolesUpper(UppercaseStrEnum):
    SELLER = auto()
    BUYER = auto()