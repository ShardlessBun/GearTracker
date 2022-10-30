from enum import StrEnum, Enum, unique, auto, IntEnum
from enum import StrEnum


@unique
class ItemType(StrEnum):
    WEAPON = "weapon"
    HEAD = "head"
    BODY = "body"
    HANDS = "hands"
    LEGS = "legs"
    FEET = "feet"
    OFFHAND = "offhand"
    EARS = "ears"
    NECK = "neck"
    WRISTS = "wrists"
    RING = "ring"
    POLISH = "polish"
    TWINE = "twine"
    COATING = "coating"
    TOMESTONE = "tomestone"


@unique
class SourceType(Enum):
    CRAFTED = "crafted"
    TOME = "tome"
    RAID = "raid"


@unique
class EventType(Enum):
    DROP = "drop"
    PURCHASE = "purchase"
    OTHER = "other"


@unique
class StaticRole(IntEnum):
    """Enum to represent the role of a static member. Lower value means greater permissions."""
    OWNER = 1
    LEADER = 2
    MEMBER = 3
