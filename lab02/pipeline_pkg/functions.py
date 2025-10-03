from .models import House, Order_status
from .context import Context_house, Context_order

class Functions:
  @staticmethod
  def change_owner(context:"Context_house",new_owner:str):
    if context.house.owner is not None:
      context.previous_owners.append(context.house.owner)
    context.house.owner = new_owner

  @staticmethod
  def print_owners(context:"Context_house"):
    for owner in context.previous_owners:
      print(owner)
  
  @staticmethod
  def print_house(context:"Context_house"):
    print(context.house.owner, context.house.area, context.house.price)

  @staticmethod
  def change_order_status(context:Context_order,status:Order_status):
    context.order.status = status

  @staticmethod
  def print_order(context:"Context_order"):
    print(context.order.order_id, context.order.status)