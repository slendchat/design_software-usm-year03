# requiered:
# models (data, house owner etc.)
# context
# steps real pipeline steps
# pipeline base
# functions
# main - here

from models import House
from context import Context
from pipeline import Pipeline
from steps import Change_owner_step, Print_house_step, Print_owners_step

if __name__ == "__main__":
  house = House("Alex", 31.5, 250)
  context = Context(house)

  pipeline = Pipeline()
  pipeline.add_step(Change_owner_step("Artur"))
  pipeline.add_step(Print_house_step())
  pipeline.add_step(Print_owners_step())

  pipeline.run(context)