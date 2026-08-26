import sqlite3

connection = sqlite3.connect("price_tracker.db")
cursor = connection.cursor()

cursor.execute("""
  UPDATE Products
  SET Price = ?
  WHERE Name = ? AND Store = ?
""", (155000, "iPhone 17 Pro", "Amazon"))

connection.commit()
connection.close()

print("Price changed for testing")