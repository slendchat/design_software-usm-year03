from enum import Enum

class Order_status(Enum):
  YES = "YES"
  NO = "NO"
  NEW = "NEW"
  PROCESSING = "PROCESSING"

class House:
  def __init__(self, owner:str, area:float, price: int):
    self.owner = owner
    self.area = area
    self.price = price

class Order:
  def __init__(self, order_id:int,status:Order_status):
    self.order_id = order_id
    self.status = status