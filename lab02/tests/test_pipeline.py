import pytest
from pipeline_pkg import (
    Pipeline, Pipeline_step,
    House, Context_house,
    Change_owner_step, Print_house_step
)

def test_change_owner_step():
    house = House("Alex", 50, 100)
    context = Context_house(house)
    pipeline = Pipeline[Context_house]()
    pipeline.add_step(Change_owner_step("Artur"))
    pipeline.run(context)

    assert context.house.owner == "Artur"
    assert "Alex" in context.previous_owners

def test_pipeline_stops_when_is_done():
    house = House("Alex", 50, 100)
    context = Context_house(house)
    context.is_done = True  # заранее останавливаем пайплайн

    pipeline = Pipeline[Context_house]()
    pipeline.add_step(Change_owner_step("Artur"))
    pipeline.run(context)

    # шаг не должен выполниться
    assert context.house.owner == "Alex"

def test_logging_decorator(capsys):
    house = House("Alex", 50, 100)
    context = Context_house(house)

    # оборачиваем Change_owner_step в Logging_step
    from pipeline_pkg.steps import Logging_step
    step = Logging_step(Change_owner_step("Artur"))

    pipeline = Pipeline[Context_house]()
    pipeline.add_step(step)
    pipeline.run(context)

    captured = capsys.readouterr()
    assert "BEFORE step" in captured.out
    assert "AFTER step" in captured.out
    assert context.house.owner == "Artur"