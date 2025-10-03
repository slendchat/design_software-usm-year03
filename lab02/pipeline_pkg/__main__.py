from .models import House, Order, Order_status
from .context import Context_house, Context_order
from .pipeline import Pipeline
from .steps import Change_owner_step, Print_house_step, Print_owners_step, Change_order_status_step, Print_order, Ask_for_step, Metric_step, Logging_step

def main():
  house = House("Alex", 31.5, 250)
  order = Order(1, Order_status.YES)
  
  context_house = Context_house(house)
  context_order = Context_order(order)

  house_pipeline = Pipeline[Context_house]()
  house_pipeline.add_step(Metric_step(Change_owner_step("Artur")))
  house_pipeline.add_step(Logging_step(Print_house_step()))
  house_pipeline.add_step(Print_owners_step())

  order_pipeline = Pipeline[Context_order]()
  order_pipeline.add_step(Ask_for_step(Change_order_status_step(Order_status.NO)))
  order_pipeline.add_step(Print_order())

  house_pipeline.run(context_house)
  order_pipeline.run(context_order)

if __name__ == "__main__":
  main()
