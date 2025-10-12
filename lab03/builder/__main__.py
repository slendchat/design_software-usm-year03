from model_builder import Catalog_builder
from model_mutable import Currency
from pprint import pprint

def main():

  #creating builder
  test_builder = Catalog_builder("Alpha_catalog").add_category("Alpha_category")

  #building with no scope
  #wrong data but builder works by final state
  test_builder.add_product(
    name="Alpha_product1", 
    price=-222220.0, 
    currency=Currency.USD, 
    discount=1543502,
    description="The first product"
    )
  
  # test_builder.add_product(
  #   name="Beta_product1", 
  #   price=-222220.0, 
  #   currency=Currency.USD, 
  #   discount=1543502,
  #   description="The first product"
  #   )
  
  #building with scope
  with test_builder.scope(currency=Currency.EUR, discount=10, description_suffix="(from scope)"):
    test_builder.add_product(
      name="Alpha_product2", 
      price=20.0, 
      description="The second product"
      )
    test_builder.add_product(
      name="Alpha_product3", 
      price=30.0
      )
    with test_builder.scope(discount=20):
      test_builder.add_product(
        name="Alpha_product4", 
        price=40.0, 
        currency=Currency.MDL,
        description="The fourth product"
        )
      
  #building with config lambda (delegate)
  test_builder.add_product(
    name="Alpha_product5", 
    price=50.0, 
    currency=Currency.USD,
    config=lambda product: product.set_discount(33)
    )
  
  test_builder.copy_pricing(
    from_product_name="Alpha_product5", 
    to_product_name="Alpha_product1", 
    currencies=[Currency.USD, Currency.EUR], 
    copy_discounts=True
  )


  catalog_i = test_builder.build()

  pprint(catalog_i)

if __name__ == "__main__":
  main()