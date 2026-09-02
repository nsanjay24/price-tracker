"""
********************************************    Buyhatke API calls   *********************************************************************
Our database.py is going to fetch prices from buyhatke since fetching prices from actual amazon and flipkart is kinda hazzle, so we'll use 
buyhatke as our pivit point. And convert the retrieved data into usable format.

Give me a Buyhatke store ID and product ID.

Build the required JSON request.

Try sending it to Buyhatke.

If HTTP failed:
    return nothing.

Convert the response into Python data.

Build the exact key Buyhatke uses for this product.

Make sure Buyhatke actually returned the product.

Take the product's JSON string.

Convert that string into a Python dictionary.

Read the price.

Read whether it's out of stock.

Convert Buyhatke's 0/1 stock system
into our Yes/No system.

Return price and stock.

If networking or bad-data errors occur:
    don't crash;
    return None instead.

"""

import requests                                                     #This library is responsible to communicate with external APIs'
import json                                                         #This library is used to handle JSON format data
import re
from database import track_product
from urllib.parse import urlparse, parse_qs

def extract_flipkart_product_id(url):
  parsed_url = urlparse(url)
  query_params = parse_qs(parsed_url.query)
  product_id = query_params.get("pid")
  if product_id:
    return product_id[0]
  return None


def extract_amazon_asin(url):
  match = re.search(r"/(?:dp|gp/product)/([A-Z0-9]{10})", url)
  if match:
    return match.group(1)
  return None


def get_buyhatke_price(store_id, product_id):
  url = "https://search-new.bitbns.com/buyhatke/thunder/priceData"    #Endpoint of buyhatke(obtained from DevTool)

  headers = {
    "Content-Type": "application/json",                               #"I'm sending JSON data in request body"
    "Origin": "https://buyhatke.com",                                 #Origin? Again from DevTool --> Tells where the request is being sennt from
    "Referer": "https://buyhatke.com/",
    "User-Agent": "Mozilla/5.0"                                       #Identifies type of client making the request
  }

  payload = {                                                         #Data we want to send to an API via HTTP request
    "param": [                                                        #param is the name that is pointing to List[]
      [store_id, product_id]  
    ]
  }

  try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)    # API CALL ****************************************************

    if response.status_code != 200:                                             #200 is success, if not succcess we terminate the function flow
      print("Request failed:", response.status_code)
      return None, None

    result = response.json()                                      #Converts JSON into python dictionary

    key = f"{store_id}~**~{product_id}"                           #?????????????????????????????????????????????????

    if "data" not in result:
      print("No data field in response")                          #If data isnt fetched we terminate the function flow
      return None, None

    if key not in result["data"]:
      print("Product not found in response")                      #Data is fetched but not related to to the product, we terminate the function
      return None, None

    raw_data = result["data"][key]

    product_data = json.loads(raw_data)

    price = product_data["price"]
    oos = product_data["oos"]

    if oos == 0:
      stock = "Yes"
    else:
      stock = "No"

    return price, stock

  except requests.exceptions.Timeout:                             #If no response within 10 seconds
    print("Request timed out")
    return None, None

  except requests.exceptions.RequestException as error:           #DNS, Network, Connection, SSL, Server issues
    print("Network/request error:", error)
    return None, None

  except (json.JSONDecodeError, KeyError, TypeError) as error:    #If fetched data isnt json data
    print("Invalid data received:", error)
    return None, None


def fetch_product_price(store, product_url):
  store = store.lower()

  if store == "amazon":
    product_id = extract_amazon_asin(product_url)
    store_id = 63
  elif store == "flipkart":
    product_id = extract_flipkart_product_id(product_url)
    store_id = 2
  else:
    print("store not supported for now")
    return None, None

  if product_id is None:
    print("could not extract product ID")
    return None, None
  price, stock = get_buyhatke_price(store_id, product_id)
  return product_id, price, stock


def track_from_url(name, store, product_url):
  product_id, price, stock = fetch_product_price(store, product_url)

  if price is None:
    # print("Could not fetch product data")
    return

  print("Product:", name)
  print("Store:", store)
  print("Product Id:", product_id)
  print("Price:", price)
  print("Stock:", stock)

  track_product(name, store, product_id, price, stock)

  return {"name":name, "store":store, "product_id":product_id, "price":price, "stock":stock}

#----------------------------------------------------------------------------------------------------------------------------------
#Test

if __name__ == "__main__":
  amazon_url = "https://www.amazon.in/dp/B0FQF5DG3P"
  flipkart_url = "https://www.flipkart.com/jbl-tune-770nc-active-noise-cancelling-70hr-playtime-fast-pair-multi-connect-bluetooth-gaming/p/itmdf5c83684df50?pid=ACCGQZVZWZFFPGYE&lid=LSTACCGQZVZWZFFPGYEMY9W0I&hl_lid=&marketplace=FLIPKART&fm=eyJ3dHAiOiJyZWNvIiwicHJwdCI6ImhwIiwibWlkIjoicGVyc29uYWxpc2VkUmVjb21tZW5kYXRpb24vcDJwLXNhbWUifQ%3D%3D&pageUID=1787767367650"

  track_from_url(
    "iPhone 17 Pro",
    "Amazon",
    amazon_url
  )

  track_from_url(
    "JBL Tune 770NC",
    "Flipkart",
    flipkart_url
  )
