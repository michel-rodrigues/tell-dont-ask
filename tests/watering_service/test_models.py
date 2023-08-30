from watering_service.models import Flower, InterruptedException, RaisedBed, Tree, Vegetable, WaterValve


def test_it_should_increment_watering_counter_when_perform_watering():
    vegetable = Vegetable(soil_moisture_percentage=59, watering_count=1)
    water_valve = WaterValve(open=False)

    vegetable.water_with(water_valve)

    assert vegetable._watering_count == 2


def test_it_should_not_increment_watering_counter_when_not_perform_watering():
    vegetable = Vegetable(soil_moisture_percentage=60, watering_count=1)
    water_valve = WaterValve(open=False)

    vegetable.water_with(water_valve)

    assert vegetable._watering_count == 1


# -------------------- VEGETABLE ----------------------------------------------


def test_it_should_watering_vegetables_when_soil_moisture_percentage_is_less_than_60():
    vegetable = Vegetable(soil_moisture_percentage=59, watering_count=1)
    water_valve = WaterValve(open=False)

    vegetable.water_with(water_valve)

    assert vegetable._soil_moisture_percentage == 79


def test_it_should_not_watering_vegetables_when_soil_moisture_percentage_is_greather_than_59():
    vegetable = Vegetable(soil_moisture_percentage=60, watering_count=1)
    water_valve = WaterValve(open=False)

    vegetable.water_with(water_valve)

    assert vegetable._soil_moisture_percentage == 60


# -------------------- FLOWER -------------------------------------------------


def test_it_should_watering_flowers_when_soil_moisture_percentage_is_less_than_60():
    flower = Flower(soil_moisture_percentage=49, watering_count=1)
    water_valve = WaterValve(open=False)

    flower.water_with(water_valve)

    assert flower._soil_moisture_percentage == 69


def test_it_should_not_watering_flowers_when_soil_moisture_percentage_is_greather_than_49():
    flower = Flower(soil_moisture_percentage=50, watering_count=1)
    water_valve = WaterValve(open=False)

    flower.water_with(water_valve)

    assert flower._soil_moisture_percentage == 50


# -------------------- TREE ---------------------------------------------------


def test_it_should_watering_trees_when_soil_moisture_percentage_is_less_than_45():
    tree = Tree(soil_moisture_percentage=44, watering_count=1)
    water_valve = WaterValve(open=False)

    tree.water_with(water_valve)

    assert tree._soil_moisture_percentage == 64


def test_it_should_not_watering_trees_when_soil_moisture_percentage_is_greather_than_44():
    tree = Tree(soil_moisture_percentage=45, watering_count=1)
    water_valve = WaterValve(open=False)

    tree.water_with(water_valve)

    assert tree._soil_moisture_percentage == 45


# -------------------- RaisedBed ---------------------------------------------------


class FakePlant:
    def __init__(self, raise_exception=False):
        self.was_called_with = None
        self.raise_exception = raise_exception

    def water_with(self, water_valve: WaterValve):
        if self.raise_exception:
            raise InterruptedException()
        self.was_called_with = water_valve


def test_it_should_water_all_plants():
    plant1 = FakePlant()
    plant2 = FakePlant()
    raised_bed = RaisedBed(plants=[plant1, plant2])
    water_valve = WaterValve(open=False)

    raised_bed.water_with(water_valve)

    assert plant1.was_called_with == water_valve
    assert plant2.was_called_with == water_valve
