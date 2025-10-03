from .models import House, Order

class Context_house:
  def __init__(self, house:House, previous_owners:list=list()):
    self.house = house
    self.previous_owners = previous_owners
    self.is_done:bool = False

class Context_order:
  def __init__(self, order:Order):
    self.order = order
    self.is_done:bool = False