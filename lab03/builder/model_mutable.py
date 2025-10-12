from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class Currency(Enum):
  EUR = "EUR"
  USD = "USD"
  MDL = "MDL"

@dataclass
class Price:
  amount: float
  discount_percent: int = 0 

@dataclass
class Product:
  name: str
  description: Optional[str] = None 
  prices: Dict[Currency, Price] = field(default_factory=dict)

  def set_price(self, currency: Currency, amount: float):
    # if amount <= 0:
    #   raise ValueError("Price amount must be positive")
    old = self.prices.get(currency)
    discount_percent = old.discount_percent if old else 0
    self.prices[currency] = Price(amount, discount_percent)

  def set_name(self, name: str): 
    # if not name:
    #   raise ValueError("Product name cannot be empty")
    self.name = name

  def set_description(self, description: str):
    self.description = description

  def set_discount(self, discount_percent: int):
    # if not (0 <= discount_percent <= 100):
    #   raise ValueError("Discount must be between 0 and 100")
    for price in self.prices.values():
      price.discount_percent = discount_percent
  
  def get_price(self, currency: Currency) -> Optional[Price]:
    return self.prices.get(currency)

  def remove_price(self, currency: Currency) -> bool:
    return self.prices.pop(currency, None) is not None

@dataclass
class Category:
  name: str
  products: List[Product] = field(default_factory=list)

  def add_product(self, product: Product):
    self.products.append(product)

  def remove_product(self, product: Product):
    self.products.remove(product)

@dataclass
class Catalog:
  name: str
  categories: List[Category] = field(default_factory=list)

  def add_category(self, category: Category):
    self.categories.append(category)

  def remove_category(self, category: Category):
    # if category.products.__len__() > 0:
      # raise Exception("To remove category its product should be empty")
    self.categories.remove(category)
