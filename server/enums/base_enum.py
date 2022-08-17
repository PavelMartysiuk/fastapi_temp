from enum import Enum, unique
from functools import lru_cache
from operator import attrgetter
from typing import Dict, Tuple


@unique
class BaseEnum(Enum):
    @classmethod
    @lru_cache(None)
    def values(cls) -> Tuple:
        return tuple(map(attrgetter("value"), cls))

    @classmethod
    @lru_cache(None)
    def names(cls) -> Tuple:
        return tuple(map(attrgetter("name"), cls))

    @classmethod
    @lru_cache(None)
    def items(cls) -> Tuple:
        return tuple(zip(cls.values(), cls.names()))

    @classmethod
    @lru_cache(None)
    def revert_items(cls) -> Tuple:
        return tuple(zip(cls.names(), cls.values()))

    @classmethod
    @lru_cache(None)
    def members(cls) -> Dict:
        return dict(cls.items())

    @classmethod
    @lru_cache(None)
    def revert_members(cls) -> Dict:
        return dict(cls.revert_items())

    def _generate_next_value_(name, start, count, last_values):
        return name
