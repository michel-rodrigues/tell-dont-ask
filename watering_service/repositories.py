from watering_service.models import Plant, PlantType, RaisedBed, WaterValve


class RaisedBedRepository:
    def __init__(self) -> None:
        plants = (
            Plant(type=PlantType.VEGETABLE, soil_moisture_percentage=59, watering_count=int),
            Plant(type=PlantType.FLOWER, soil_moisture_percentage=49, watering_count=int),
            Plant(type=PlantType.TREE, soil_moisture_percentage=44, watering_count=int),
        )
        self._raised_bed = RaisedBed(plants)

    def get_bed(self, bed_id: str) -> RaisedBed:
        return self._raised_bed

    def save(self, raised_bed: RaisedBed):
        self._raised_bed = raised_bed


class WaterValveRepository:
    def __init__(self):
        self._water_valve = WaterValve(open=False)

    def get_water_valve(self) -> WaterValve:
        return self._water_valve

    def save(self, water_valve: WaterValve):
        self._water_valve = water_valve
