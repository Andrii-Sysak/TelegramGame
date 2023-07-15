from enum import (
    StrEnum,
    auto
)

from pydantic_yaml import YamlModel


class UpdateStrategy(StrEnum):
    polling = auto()
    webhook = auto()


class Durations(YamlModel):
    movement: int


class Settings(YamlModel):
    token: str
    updates_strategy: UpdateStrategy
    durations: Durations


class Config(YamlModel):
    c: Settings
