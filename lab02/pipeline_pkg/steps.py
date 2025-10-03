import time
from .pipeline import Pipeline_step, TContext
from .functions import Functions
from .context import Context_house, Context_order
from .models import Order_status


class Change_owner_step(Pipeline_step[Context_house]):
  def __init__(self, new_owner:str):
    self.new_owner = new_owner

  def execute(self, context:Context_house):
    Functions.change_owner(context, self.new_owner)

  def introspect(self):
    print(f"ChangeOwner({self.new_owner})")

class Print_owners_step(Pipeline_step[Context_house]):
  def execute(self, context:Context_house):
    Functions.print_owners(context)

  def introspect(self):
    pass

class Print_house_step(Pipeline_step[Context_house]):
  def execute(self, context:Context_house):
    Functions.print_house(context)

  def introspect(self):
    pass


class Change_order_status_step(Pipeline_step[Context_order]):
  def __init__(self,status:Order_status):
    self.status = status
  
  def execute(self, context:Context_order):
    Functions.change_order_status(context, self.status)

  def introspect(self):
    print(f"ChangeOrderStatus({self.status})")

class Print_order(Pipeline_step[Context_order]):
  def execute(self, context:"Context_order"):
    Functions.print_order(context)

  def introspect(self):
    pass



class Logging_step(Pipeline_step[TContext]):
  def __init__(self, pipeline_step:Pipeline_step[TContext]):
    self.step = pipeline_step

  def execute(self,context:TContext):
    print("BEFORE step")
    self.step.execute(context)
    print("AFTER step")
  
  def introspect(self):
    print("LoggingDecorator ->", end=" ")
    self.step.introspect()

class Metric_step(Pipeline_step[TContext]):
  def __init__(self, pipeline_step:Pipeline_step[TContext]):
    self.step = pipeline_step

  def execute(self,context:TContext):
    start_time = time.perf_counter()
    self.step.execute(context)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f}")

  def introspect(self):
    print("LoggingDecorator ->", end=" ")
    self.step.introspect()

class Ask_for_step(Pipeline_step[TContext]):
  def __init__(self, pipeline_step:Pipeline_step[TContext]):
    self.step = pipeline_step

  def execute(self,context:TContext):
    user_responce = input("Do you want to proceed? (Y/n): ")
    if str.capitalize(user_responce) == 'Y':
      self.step.execute(context)
    else:
      print("Action canceled")
      context.is_done = True
  
  def introspect(self):
    print("LoggingDecorator ->", end=" ")
    self.step.introspect()