from tests.watering_service.test_models import FakePlant
from watering_service.models import RaisedBed, WaterValve
from watering_service.repositories import RaisedBedRepository, WaterValveRepository
from watering_service.service import InterruptedException, Watering, WateringCommand


class FakeRaisedBed:
    def __init__(self):
        self.was_called_with = None

    def water_with(self, water_valve: WaterValve):
        self.was_called_with = water_valve


class FakeRaisedBedRepository(RaisedBedRepository):
    def __init__(self, raised_bed: RaisedBed) -> None:
        self._raised_bed = raised_bed
        self.save_was_called_with = None

    def save(self, raised_bed: RaisedBed):
        self.save_was_called_with = raised_bed


class FakeWaterValveRepository(WaterValveRepository):
    def __init__(self, water_valve):
        self._water_valve = water_valve


def raise_exception():
    raise InterruptedException()


def test_it_should_delegate_watering_process():
    raised_bed = FakeRaisedBed()
    raised_bed_repository = FakeRaisedBedRepository(raised_bed)
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert raised_bed.was_called_with == water_valve


def test_it_should_persist_changed_states_when_watering_successfully():
    raised_bed = RaisedBed(plants=[FakePlant()])
    raised_bed_repository = FakeRaisedBedRepository(raised_bed)
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    result = watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert result is True
    assert raised_bed_repository.save_was_called_with == raised_bed


def test_it_should_not_persist_changed_states_when_watering_fails():
    raised_bed = RaisedBed(plants=[FakePlant(raise_exception=True)])
    raised_bed_repository = FakeRaisedBedRepository(raised_bed)
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert raised_bed_repository.save_was_called_with is None
