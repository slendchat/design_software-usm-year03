from pipeline import Pipeline_step
from functions import Functions
from context import Context


class Change_owner_step(Pipeline_step):
  def __init__(self, new_owner:str):
    self.new_owner = new_owner

  def execute(self, context:"Context"):
    Functions.change_owner(context, self.new_owner)

  def introspect(self):
    print(f"ChangeOwner({self.new_owner})")

class Print_owners_step(Pipeline_step):
  def execute(self, context:"Context"):
    Functions.print_owners(context)

  def introspect(self):
    pass

class Print_house_step(Pipeline_step):
  def execute(self, context:"Context"):
    Functions.pring_house(context)

  def introspect(self):
    pass