from watering_service.models import Plant, PlantType, RaisedBed, WaterValve
from watering_service.repositories import RaisedBedRepository, WaterValveRepository
from watering_service.service import InterruptedException, Watering, WateringCommand


class FakeRaisedBedRepository(RaisedBedRepository):
    def __init__(self, plants) -> None:
        self._raised_bed = RaisedBed(plants)


class FakeWaterValveRepository(WaterValveRepository):
    def __init__(self, water_valve, raise_exception=False):
        self._water_valve = water_valve


def raise_exception():
    raise InterruptedException()


def test_it_should_persist_changed_states_when_watering_successfully():
    vegetable = Plant(type=PlantType.VEGETABLE, soil_moisture_percentage=59, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([vegetable])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    result = watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert result is True
    assert raised_bed_repository._raised_bed.plants[0].soil_moisture_percentage == 79
    assert raised_bed_repository._raised_bed.plants[0].watering_count == 2


def test_it_should_not_persist_changed_states_when_watering_fails():
    vegetable = Plant(type=PlantType.VEGETABLE, soil_moisture_percentage=59, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([vegetable])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service._wating_water_to_flow = raise_exception

    result = watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert result is False
    assert raised_bed_repository._raised_bed.plants[0] == vegetable


# -------------------- VEGETABLE ----------------------------------------------


def test_it_should_watering_vegetables_when_soil_moisture_percentage_is_less_than_60():
    vegetable = Plant(type=PlantType.VEGETABLE, soil_moisture_percentage=59, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([vegetable])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert vegetable.soil_moisture_percentage == 79


def test_it_should_increment_watering_counter_when_perform_vegetable_watering():
    vegetable = Plant(type=PlantType.VEGETABLE, soil_moisture_percentage=59, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([vegetable])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert vegetable.watering_count == 2


def test_it_should_not_watering_vegetables_when_soil_moisture_percentage_is_greather_than_59():
    vegetable = Plant(type=PlantType.VEGETABLE, soil_moisture_percentage=60, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([vegetable])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert vegetable.soil_moisture_percentage == 60


def test_it_should_not_increment_watering_counter_when_not_perform_vegetable_watering():
    vegetable = Plant(type=PlantType.VEGETABLE, soil_moisture_percentage=60, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([vegetable])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert vegetable.watering_count == 1


# -------------------- FLOWER -------------------------------------------------


def test_it_should_watering_flowers_when_soil_moisture_percentage_is_less_than_60():
    flower = Plant(type=PlantType.FLOWER, soil_moisture_percentage=49, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([flower])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert flower.soil_moisture_percentage == 69


def test_it_should_increment_watering_counter_when_perform_flower_watering():
    flower = Plant(type=PlantType.FLOWER, soil_moisture_percentage=49, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([flower])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert flower.watering_count == 2


def test_it_should_not_watering_flowers_when_soil_moisture_percentage_is_greather_than_49():
    flower = Plant(type=PlantType.FLOWER, soil_moisture_percentage=50, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([flower])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert flower.soil_moisture_percentage == 50


def test_it_should_not_increment_watering_counter_when_not_perform_flower_watering():
    flower = Plant(type=PlantType.FLOWER, soil_moisture_percentage=50, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([flower])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert flower.watering_count == 1


# -------------------- TREE ---------------------------------------------------


def test_it_should_watering_trees_when_soil_moisture_percentage_is_less_than_45():
    tree = Plant(type=PlantType.TREE, soil_moisture_percentage=44, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([tree])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert tree.soil_moisture_percentage == 64


def test_it_should_increment_watering_counter_when_perform_tree_watering():
    tree = Plant(type=PlantType.TREE, soil_moisture_percentage=44, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([tree])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert tree.watering_count == 2


def test_it_should_not_watering_trees_when_soil_moisture_percentage_is_greather_than_44():
    tree = Plant(type=PlantType.TREE, soil_moisture_percentage=45, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([tree])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert tree.soil_moisture_percentage == 45


def test_it_should_not_increment_watering_counter_when_not_perform_tree_watering():
    tree = Plant(type=PlantType.TREE, soil_moisture_percentage=45, watering_count=1)
    raised_bed_repository = FakeRaisedBedRepository([tree])
    water_valve = WaterValve(open=False)
    water_valve_repository = FakeWaterValveRepository(water_valve)

    watering_service = Watering(raised_bed_repository, water_valve_repository)
    watering_service.perform(WateringCommand(bed_id="dummy-id"))

    assert tree.watering_count == 1
