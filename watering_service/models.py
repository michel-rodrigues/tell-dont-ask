import time
from enum import StrEnum
from typing import Sequence


class InterruptedException(Exception):
    ...


class WaterValve:
    def __init__(self, open: bool):
        self._open = open

    def open(self):
        self._open = True

    def close(self):
        self._open = False


class WateringProblems(StrEnum):
    VALVE_MALFUNCTION = "valve_malfunction"


class WateringResult:
    def __init__(self, successful: bool, reason_why_it_cannot_be_done: WateringProblems = ""):
        self.successful = successful
        self.reason_why_it_cannot_be_done = reason_why_it_cannot_be_done
        if self.successful and reason_why_it_cannot_be_done:
            raise Exception("Successful result do not demand a reason")

    @classmethod
    def success(cls):
        return cls(successful=True)

    @classmethod
    def valve_malfunction(cls):
        return cls(successful=False, reason_why_it_cannot_be_done=WateringProblems.VALVE_MALFUNCTION)

    def was_it_a_valve_malfunction(self):
        return self.reason_why_it_cannot_be_done == WateringProblems.VALVE_MALFUNCTION


class Plant:
    _soil_moisture_percentage_threshold = None

    def __init__(self, soil_moisture_percentage: int, watering_count: int):
        self._soil_moisture_percentage = soil_moisture_percentage
        self._watering_count = watering_count
        if self._soil_moisture_percentage_threshold is None:
            raise NotImplementedError("soil_moisture_percentage_threshold must be set")

    def _wating_water_to_flow(self):
        time.sleep(0.1)

    @property
    def _needs_watering(self):
        return self._soil_moisture_percentage < self._soil_moisture_percentage_threshold

    def water_with(self, water_valve: WaterValve) -> WateringResult:
        if self._needs_watering:
            try:
                water_valve.open()
                self._soil_moisture_percentage = self._soil_moisture_percentage + 20
                self._watering_count = self._watering_count + 1
                self._wating_water_to_flow()
            except InterruptedException:
                return WateringResult.valve_malfunction()
            finally:
                water_valve.close()

        return WateringResult.success()


class Vegetable(Plant):
    _soil_moisture_percentage_threshold = 60


class Flower(Plant):
    _soil_moisture_percentage_threshold = 50


class Tree(Plant):
    _soil_moisture_percentage_threshold = 45


class RaisedBed:
    def __init__(self, plants: Sequence[Plant]):
        self._plants = plants

    def water_with(self, water_valve: WaterValve) -> WateringResult:
        for plant in self._plants:
            result = plant.water_with(water_valve)
            if not result.successful:
                return result
        return result
