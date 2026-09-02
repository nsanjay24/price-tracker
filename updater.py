from database import get_all_products, track_product
from product_fetcher import get_buyhatke_price


def update_all_products():
  products = get_all_products()

  print("Checking", len(products), "products...")

  for product in products:
    name = product[0]
    store = product[1]
    product_id = product[2]

    if store.lower() == "amazon":
      store_id = 63

    elif store.lower() == "flipkart":
      store_id = 2

    else:
      print("Unsupported store:", store)
      continue

    print()
    print("Checking:", name)

    price, stock = get_buyhatke_price(
      store_id,
      product_id
    )

    if price is None:
      print("Could not fetch:", name)
      continue

    print("Fresh price:", price)
    print("Fresh stock:", stock)

    track_product(
      name,
      store,
      product_id,
      price,
      stock
    )


if __name__ == "__main__":
  update_all_products()   