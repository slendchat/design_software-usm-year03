from models import House
from context import Context

class Functions:
  @staticmethod
  def change_owner(context:"Context",new_owner:str):
    if context.house.owner is not None:
      context.previous_owners.append(context.house.owner)
    context.house.owner = new_owner

  @staticmethod
  def print_owners(context:"Context"):
    for owner in context.previous_owners:
      print(owner)
  
  @staticmethod
  def pring_house(context:"Context"):
    print(context.house.owner, context.house.area, context.house.price)