from __future__ import annotations
from typing import Optional, List, Dict, Callable, Iterable
from model_mutable import *
from model_immutable import *
from validation_utils import mark_created_here, get_created_at

class Catalog_builder:
  def __init__(self, name: str):
    self._pending_errors: List[str] = []
    if not name:
      self._pending_errors.append("Catalog name cannot be empty")
      name = ""
    self._catalog = Catalog(name)
    mark_created_here(self._catalog)
    self._current_category: Optional[Category] = None
    self._scope_stack: List[Dict[str, object]] = []

  # ---------- helpers ----------
  def _err(self, obj, msg: str) -> None:
    self._pending_errors.append(
      f"[{get_created_at(obj) if obj is not None else '<unknown>'}] {msg}"
    )

  def _try(self, obj, fn, *args, **kwargs) -> None:
    try:
      fn(*args, **kwargs)
    except ValueError as e:
      self._err(obj, f"{obj.__class__.__name__} '{getattr(obj, 'name', '<no-name>')}': {e}")

  # ---------- scope ----------
  class Scope_context:
    def __init__(self, builder: "Catalog_builder", scope_data: dict):
      self.builder = builder
      self.scope_data = scope_data
    def __enter__(self):
      self.builder._scope_stack.append(self.scope_data)
      return self.builder
    def __exit__(self, exc_type, exc_value, traceback):
      self.builder._scope_stack.pop()

  def scope(
    self,
    currency: Optional[Currency] = None,
    discount: Optional[int] = None,
    description_suffix: Optional[str] = None,
  ) -> "Catalog_builder.Scope_context":
    return Catalog_builder.Scope_context(
      self,
      {"currency": currency, "discount": discount, "description_suffix": description_suffix},
    )

  # ---------- API ----------
  def add_category(self, name: str) -> "Catalog_builder":
    if not name:
      self._err(self._catalog, "Category name cannot be empty")
      name = ""
    category = Category(name, [])
    mark_created_here(category)
    self._catalog.categories.append(category)
    self._current_category = category
    return self

  def add_product(
    self,
    name: str,
    price: float,
    currency: Optional[Currency] = None,
    discount: Optional[int] = None,
    description: Optional[str] = None,
    config: Optional[Callable[[Product], None]] = None,
  ) -> "Catalog_builder":
    if self._current_category is None:
      self._err(self._catalog, "No category defined. Please add a category before adding products.")
      return self
    if not name:
      self._err(self._current_category, "Product name cannot be empty")
      name = ""

    scope = self._scope_stack[-1] if self._scope_stack else {}
    eff_currency = currency if currency is not None else scope.get("currency")
    if eff_currency is None:
      self._err(self._current_category, "Currency must be specified either in product or in scope")
      return self

    eff_description = description
    suf = scope.get("description_suffix")
    if suf:
      eff_description = (eff_description or "") + " " + str(suf)

    product = Product(name, eff_description)
    mark_created_here(product)

    self._try(product, product.set_price, eff_currency, price)
    if discount is None:
      discount = scope.get("discount")
    if discount is not None:
      self._try(product, product.set_discount, int(discount))

    if config:
      try:
        config(product)
      except ValueError as e:
        self._err(product, f"config error: {e}")

    self._current_category.add_product(product)
    return self

  def set_price_with_discount(
    self,
    product_name: str,
    currency: Currency,
    amount: float,
    discount: int,
  ) -> "Catalog_builder":
    if self._current_category is None:
      self._err(self._catalog, "Select category first")
      return self
    for p in self._current_category.products:
      if p.name == product_name:
        self._try(p, p.set_price, currency, amount)
        self._try(p, p.set_discount, discount)
        return self
    self._err(self._current_category, f"Product '{product_name}' not found")
    return self

  def copy_pricing(
    self,
    *,
    from_product_name: str,
    to_product_name: str,
    currencies: Optional[Iterable[Currency]] = None,
    copy_discounts: bool = True,
  ) -> "Catalog_builder":
    if self._current_category is None:
      self._err(self._catalog, "Select category first")
      return self

    src = dst = None
    for p in self._current_category.products:
      if p.name == from_product_name:
        src = p
      if p.name == to_product_name:
        dst = p

    if src is None:
      self._err(self._current_category, f"Product '{from_product_name}' not found")
      return self
    if dst is None:
      self._err(self._current_category, f"Product '{to_product_name}' not found")
      return self

    cur_list = list(currencies) if currencies is not None else list(src.prices.keys())
    for cur in cur_list:
      price = src.prices.get(cur)
      if price is None:
        continue
      self._try(dst, dst.set_price, cur, price.amount)
      if copy_discounts:
        self._try(dst, dst.set_discount, price.discount_percent)
    return self

  def build(self) -> Catalog_immutable:
    from validation_utils import validate_catalog_collect_all
    errors = list(self._pending_errors)
    errors += validate_catalog_collect_all(self._catalog)
    if errors:
      raise ValueError("Catalog validation failed:\n  - " + "\n  - ".join(errors))
    return to_immutable_catalog(self._catalog)
