from enum import StrEnum
from typing import Sequence

from mixins import RepresentationMixin


class PlantType(StrEnum):
    VEGETABLE = "vegetable"
    FLOWER = "flower"
    TREE = "tree"


class Plant(RepresentationMixin):
    def __init__(self, type: PlantType, soil_moisture_percentage: int, watering_count: int):
        self.type = type
        self.soil_moisture_percentage = soil_moisture_percentage
        self.watering_count = watering_count


class RaisedBed(RepresentationMixin):
    def __init__(self, plants: Sequence[Plant]):
        self.plants = plants


class WaterValve(RepresentationMixin):
    def __init__(self, open: bool):
        self.open = open
