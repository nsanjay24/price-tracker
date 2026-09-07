from flask import Flask, render_template, request, redirect
from product_fetcher import track_from_url, get_buyhatke_price
from database import(get_all_products, delete_product, get_lowest_price, get_history_count, get_product_history, track_product)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
  message = None
  product = None 

  if request.method == "POST":
    name = request.form["name"]
    # store = request.form["store"]
    product_url = request.form["product_url"]

    product = track_from_url(name, product_url)

    if product is not None:
      message = "Product tracked successfully!"
    else:
      message = "Could not fetch product data"

  tracked_products = get_all_products()
  product_cards = []
  for item in tracked_products:
    name = item[0]
    store = item[1]
    product_id = item[2]
    price = item[3]
    stock = item[4]

    lowest_price = get_lowest_price(
      store,
      product_id
    )

    history_count = get_history_count(
      store,
      product_id
    )

    product_cards.append({
      "name": name,
      "store": store,
      "product_id": product_id,
      "price": price,
      "stock": stock,
      "lowest_price": lowest_price,
      "history_count": history_count
    })
  return render_template("index.html", message=message, product=product, product_cards=product_cards)


@app.route("/delete", methods=["POST"])
def delete():
  store = request.form["store"]
  product_id = request.form["product_id"]

  delete_product(store,product_id)

  return redirect("/")


@app.route("/history/<store>/<product_id>")
def history(store, product_id):
  history = get_product_history(store, product_id)
  lowest_price = get_lowest_price(store, product_id)
  return render_template("history.html", store = store, product_id = product_id, history = history, lowest_price = lowest_price)

@app.route("/refresh", methods = ["POST"])
def refresh():
  name = request.form["name"]
  store = request.form["store"]
  product_id = request.form["product_id"]
  if store.lower() == "amazon":
    store_id = 63
  elif store.lower() == "flipkart":
    store_id = 2
  else:
    return redirect("/")
  price, stock = get_buyhatke_price(store_id, product_id)
  if price is not None:
    track_product(name, store, product_id, price, stock)
  return redirect("/")

if __name__ == "__main__":
  app.run(debug=True)