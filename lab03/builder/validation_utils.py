# validation_utils.py
from model_mutable import Catalog, Category, Product, Currency, Price
from typing import List
from typing import Any
import traceback

_CREATED_AT_ATTR = "__created_at"

def mark_created_here(obj: Any, *, skip_frames: int = 2) -> None:
  frame = traceback.extract_stack(limit=skip_frames + 1)[0]
  setattr(obj, _CREATED_AT_ATTR, f"{frame.filename}:{frame.lineno}")

def get_created_at(obj: Any) -> str:
  return getattr(obj, _CREATED_AT_ATTR, "<unknown>")



def validate_catalog_collect_all(catalog: Catalog) -> List[str]:
  errors: List[str] = []
  
  if not getattr(catalog, "name", "").strip():
    errors.append(f"[{get_created_at(catalog)}] Catalog: name is empty")
  if not getattr(catalog, "categories", None):
    errors.append(f"[{get_created_at(catalog)}] Catalog '{catalog.name}': no categories")
  
  
  for cattegory in getattr(catalog, "categories", []):
    if not getattr(cattegory, "name", "").strip():
      errors.append(f"[{get_created_at(cattegory)}] Category: name is empty")
    if not getattr(cattegory, "products", None):
      errors.append(f"[{get_created_at(cattegory)}] Category '{cattegory.name}': no products")
    
    
    for product in getattr(cattegory, "products", []):
      if not getattr(product, "name", "").strip():
        errors.append(f"[{get_created_at(product)}] Product: name is empty (category '{cattegory.name}')")
      
      prices = getattr(product, "prices", {})
      if not prices:
        errors.append(f"[{get_created_at(product)}] Product '{product.name}' in '{cattegory.name}': no prices")
      
      for currency, price in prices.items():
        if price.amount <= 0:
          errors.append(
            f"[{get_created_at(product)}] Product '{product.name}' in '{cattegory.name}': "
            f"non-positive price for {currency.name} ({price.amount})"
          )
        
        if not (0 <= price.discount_percent <= 100):
          errors.append(
            f"[{get_created_at(product)}] Product '{product.name}' in '{cattegory.name}': "
            f"invalid discount {price.discount_percent} for {currency.name} (must be 0..100)"
          )
  return errors
