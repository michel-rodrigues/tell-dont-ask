import collections
import time

from watering_service.models import PlantType, RaisedBed, WaterValve
from watering_service.repositories import RaisedBedRepository, WaterValveRepository


WateringCommand = collections.namedtuple("WateringCommand", "bed_id")


class InterruptedException(Exception):
    ...


class Watering:
    def __init__(self, raised_bed_repository: RaisedBedRepository, water_valve_repository: WaterValveRepository):
        self._raised_bed_repository = raised_bed_repository
        self._water_valve_repository = water_valve_repository

    def perform(self, command: WateringCommand) -> bool:
        raised_bed = self._raised_bed_repository.get_bed(command.bed_id)
        water_valve = self._water_valve_repository.get_water_valve()
        successfully_watered = self._water_bed(raised_bed, water_valve)
        if successfully_watered:
            self._water_valve_repository.save(water_valve)
            self._raised_bed_repository.save(raised_bed)
        return successfully_watered

    def _wating_water_to_flow(self):
        time.sleep(0.1)

    def _water_bed(self, raised_bed: RaisedBed, water_valve: WaterValve) -> bool:
        for plant in raised_bed.plants:
            needs_watering = False
            match plant.type:
                case PlantType.VEGETABLE:
                    needs_watering = plant.soil_moisture_percentage < 60
                case PlantType.FLOWER:
                    needs_watering = plant.soil_moisture_percentage < 50
                case PlantType.TREE:
                    needs_watering = plant.soil_moisture_percentage < 45

            if needs_watering:
                try:
                    water_valve.open = True
                    plant.soil_moisture_percentage = plant.soil_moisture_percentage + 20
                    plant.watering_count = plant.watering_count + 1
                    self._wating_water_to_flow()
                except InterruptedException:
                    return False
                finally:
                    water_valve.open = False

        return True
