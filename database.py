"""
********************************************      Price & stock tracker   *********************************************************************
 
Stores the last known price/stock for each (product, store) pair in a local SQLite database. Each run compares freshly-fetched values against
what's stored and prints an alert when something changes (price drop,price increase, or a stock status flip). Price drops trigger WhatsApp 
alerts through the WhatsApp Cloud API..
"""

import sqlite3
from whatsapp.whatsapp import send_whatsapp_message

def get_product(productStore, productId):                                         #To fetch data using funtion
  cursor.execute("""
    SELECT * FROM Products WHERE Store = ? AND ProductId = ?
  """, (productStore, productId))
  return(cursor.fetchone())                                                       #Will print value of only one product

def add_product(productName, productStore, productId, productPrice, productStock):           #To add data into the table using function
  cursor.execute("""
  INSERT INTO Products (Name, Store, productId, Price, Stock) VALUES (?, ?, ?, ?, ?)
  """,(productName, productStore, productId, productPrice, productStock))
  connection.commit()

def update_product(productStore, productId, productPrice, productStock):        #To update product details (Price/Stock) using function
  cursor.execute("""
  UPDATE Products SET Price = ?, Stock = ? WHERE Store = ? AND ProductId = ?
  """,(productPrice, productStock, productStore, productId))
  connection.commit()

def priceChange(newPrice, oldPrice):                                              #To check if there is a change in price                    
  if(newPrice < oldPrice):
    return "dropped"
  elif(newPrice > oldPrice):
    return "increased"
  else:
    return "unchanged"

def stockChange(oldStock, newStock):                                              #To check if there is a change in stock
  if oldStock == "No" and newStock == "Yes":
    return "Back in stock"
  elif oldStock == "Yes" and newStock == "No":
    return "Out of stock!"
  else:
    return "Unchanged"

def create_alert(name, store, oldPrice, newPrice):                                #To create a alert message ONLY WHEN THERE IS PRICE CHANGE
  difference = oldPrice - newPrice
  message = f"""
  PRICE DROP!!
  
  Product: {name}
  Store: {store}

  Old price: ₹{oldPrice}
  New price: ₹{newPrice}

  You save: ₹{difference}
  """
  return message

def track_product(productName, productStore, productId, productPrice, productStock):         #The actual function which tracks the product by comparing 
  old_product = get_product(productStore, productId)                              #Fetching and storing the old data into a variable
  #print(old_product)
  if(old_product is None):                                                        #Chcking if product alr exists in our database
    print("This is new item!")
    add_product(productName, productStore, productId, productPrice, productStock)            #If the product dosent exist we add a new entry into the database
  else:                                                                           #If the product exists in our database then:
    old_price = old_product[4]                                                    #Extracting old price of the specific product
    old_stock = old_product[5]                                                    #Exracting old stock status of the specific product
    # print("Old price : ",old_price)                                             #TO_CHECK
    # print("Old stock : ",old_stock)                                             #TO_CHECK

    stockStatus = stockChange(old_stock, productStock)                            #Function call to check change in status of stock
    priceStatus = priceChange(productPrice, old_price)                            #Function call to check change in price
    # print("Price :",priceStatus)                                                #TO_CHECK
    # print("Stock :",stockStatus)                                                #TO_CHECK

    if stockStatus == "Back in stock":                                            #If the product is available to buy (BACK IN STOCK)
      print("🟢 BACK IN STOCK!")
    elif stockStatus == "Out of stock!":                                          #If the product is unavailable to buy (OUT OF STOCK)
      print("🔴 OUT OF STOCK!")

    if priceStatus == "dropped":
      send_whatsapp_message(productName, productStore, old_price, productPrice)   #This'll trigger the alert mechanism in whatsapp.py


    update_product(productStore, productId, productPrice, productStock)         #Updates the database with new changes


#------------------------------------------------------------------------------------------------------------------------------------------------  
connection = sqlite3.connect('price_tracker.db')
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products(
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT,
  Store TEXT,
  ProductId TEXT,
  Price INTEGER,
  Stock TEXT,
  UNIQUE(Store, ProductId)
)
""")
connection.commit()

'''-------------------------------------------------------------To Print the data of the table------------------------------------------------'''
# cursor.execute("""SELECT * FROM Products""")              
# Data = cursor.fetchall()
# print(Data)

'''--------------------------------------------------------------To inspect data table--------------------------------------------------------'''
# cursor.execute("""
# SELECT sql
# FROM sqlite_master
# WHERE type = 'table'
# AND name = 'Products'
# """)
# print(cursor.fetchone())

#-----------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
  name = "RTX 5070"
  store = "Amazon"
  pid = "TEST123456"
  price = 58000
  stock = "Yes"

  track_product(name, store, pid, price, stock)