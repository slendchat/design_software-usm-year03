from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, Mapping
from types import MappingProxyType
from model_mutable import Currency, Price, Product, Category, Catalog

@dataclass(frozen=True)
class Price_immutable:
  amount: float
  discount_percent: int = 0

@dataclass(frozen=True)
class Product_immutable:
  name: str
  prices: Mapping[Currency, Price_immutable]
  description: Optional[str] = None

@dataclass(frozen=True)
class Category_immutable:
  name: str
  products: Tuple[Product_immutable,...]

@dataclass(frozen=True)
class Catalog_immutable:
  name: str
  categories: Tuple[Category_immutable,...]

def to_immutable_price(price: Price) -> Price_immutable:
  # if price is None:
  #   raise ValueError("Price cannot be None")
  # elif price.amount <= 0:
  #   raise ValueError("Price amount must be positive")
  # elif not (0 <= price.discount_percent <= 100):
  #   raise ValueError("Discount must be between 0 and 100")
  return Price_immutable(float(price.amount), int(price.discount_percent))

def to_immutable_product(product: Product) -> Product_immutable:
  # if product is None:
  #   raise ValueError("Product cannot be None")
  prices_immutable = {currency: to_immutable_price(price) for currency, price in product.prices.items()}
  return Product_immutable(
    name=product.name, 
    description=product.description, 
    prices=MappingProxyType(prices_immutable)
  )

def to_immutable_category(category: Category) -> Category_immutable:
  return Category_immutable(
    name=category.name, 
    products=tuple(to_immutable_product(product) for product in category.products)
  )

def to_immutable_catalog(catalog: Catalog) -> Catalog_immutable:
  return Catalog_immutable(
    name=catalog.name, 
    categories=tuple(to_immutable_category(category) for category in catalog.categories)
  )