from tests.watering_service.test_models import FakePlant
from watering_service.models import RaisedBed, WaterValve, WateringResult
from watering_service.repositories import RaisedBedRepository, WaterValveRepository
from watering_service.service import Watering, WateringCommand


class FakeRaisedBed:
    def __init__(self, result=True):
        self.was_called_with = None
        self.result = result

    def water_with(self, water_valve: WaterValve):
        self.was_called_with = water_valve
        return self.result


class FakeRaisedBedRepository(RaisedBedRepository):
    def __init__(self, raised_bed):
        self._raised_bed = raised_bed
        self.save_was_called_with = None

    def save(self, raised_bed: RaisedBed):
        self.save_was_called_with = raised_bed


class FakeWaterValveRepository(WaterValveRepository):
    def __init__(self, water_valve):
        self._water_valve = water_valve


def test_it_should_delegate_watering_process():
    raised_bed = FakeRaisedBed(result=WateringResult.success())
    raised_bed_repository = FakeRaisedBedRepository(raised_bed)
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert raised_bed.was_called_with == water_valve


def test_it_should_persist_changed_states_when_watering_successfully():
    raised_bed = RaisedBed(plants=[FakePlant(result=WateringResult.success())])
    raised_bed_repository = FakeRaisedBedRepository(raised_bed)
    water_valve_repository = FakeWaterValveRepository(WaterValve(open=False))

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    result = watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert result.successful is True
    assert raised_bed_repository.save_was_called_with == raised_bed


def test_it_should_not_persist_changed_states_when_watering_fails():
    raised_bed = RaisedBed(plants=[FakePlant(result=WateringResult.valve_malfunction())])
    raised_bed_repository = FakeRaisedBedRepository(raised_bed)
    water_valve_repository = FakeWaterValveRepository(WaterValve(open=False))

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    result = watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert result.successful is False
    assert raised_bed_repository.save_was_called_with is None
