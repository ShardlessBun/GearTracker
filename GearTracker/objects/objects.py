import re
from typing import Dict, List
from uuid import UUID


def is_raid_gear(item_name: str) -> bool:
    prefixes = ["Asphodelos", "Abyssos"]
    for prefix in prefixes:
        if prefix in item_name:
            return True
    return False


def is_tome_gear(item_name: str) -> bool:
    gear_names = ["Radiant's", "Lunar Envoy's"]
    for name in gear_names:
        if name in item_name:
            return True
    return False


class Equipment(object):
    id: int
    name: str
    description: str

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def params(self) -> Dict[int, int]:
        params = {}
        if self.param0:
            params[self.param0] = self.param0Value
        if self.param1:
            params[self.param1] = self.param1Value
        if self.param2:
            params[self.param2] = self.param2Value
        if self.param3:
            params[self.param3] = self.param3Value
        if self.param4:
            params[self.param4] = self.param4Value
        if self.param5:
            params[self.param5] = self.param5Value

        return params

    @property
    def gear_type(self) -> str:
        if self.advancedMelding:
            return 'crafted'
        elif is_tome_gear(self.name):
            return 'tomestone'
        elif is_raid_gear(self.name):
            return "raid"

        return 'other'

    @property
    def jobs(self) -> List[str]:
        return self.jobName.split()

