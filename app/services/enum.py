from enum import Enum as PyEnum


class UserRoles(str, PyEnum):
    BUYER = "buyer"
    SELLER = "seller"
