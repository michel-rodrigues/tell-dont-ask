import collections

from watering_service.models import WateringResult
from watering_service.repositories import RaisedBedRepository, WaterValveRepository


WateringCommand = collections.namedtuple("WateringCommand", "bed_id")


class Watering:
    def __init__(self, raised_bed_repository: RaisedBedRepository, water_valve_repository: WaterValveRepository):
        self._raised_bed_repository = raised_bed_repository
        self._water_valve_repository = water_valve_repository

    def perform(self, command: WateringCommand) -> WateringResult:
        raised_bed = self._raised_bed_repository.get_bed(command.bed_id)
        water_valve = self._water_valve_repository.get_water_valve()
        result = raised_bed.water_with(water_valve)
        if result.successful:
            self._water_valve_repository.save(water_valve)
            self._raised_bed_repository.save(raised_bed)
        return result
