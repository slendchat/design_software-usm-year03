from models import House

class Context:
  def __init__(self, house:House, previous_owners:list=list()):
    self.house = house
    self.previous_owners = previous_owners