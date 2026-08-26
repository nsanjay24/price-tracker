"""
*********************************************************   WHATSAPP API CALLS    ************************************************************
Receive message information → send it through Meta WhatsApp Cloud API → report whether it worked.
"""

import os, requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
RECIPIENT = os.getenv("WHATSAPP_RECIPIENT")
API_VERSION = "v26.0"

def send_whatsapp_message(product, store, old_price, new_price):
  url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"

  savings = old_price - new_price

  headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json" 
  }

  payload = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT,
    "type": "template",
    "template": {
      "name": "price_drop_alert",
      "language": {
        "code": "en"
      },
      "components" : [
        {
          "type" : "body",
          "parameters" : [
            {
              "type" : "text",
              "text" : str(product)
            },
            {
              "type" : "text",
              "text" : str(store)
            },
            {
              "type" : "text",
              "text" : str(old_price)
            },
            {
              "type" : "text",
              "text" : str(new_price)
            },
            {
              "type" : "text",
              "text" : str(savings)
            }
          ]
        }
      ]
    }
  }

  try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)

    if response.status_code == 200:
      print("WhatsApp price alert sent!")
      return True

    print("WhatsApp message failed")
    print("Status:", response.status_code)
    print("Response:", response.text)
    return False

  except requests.exceptions.Timeout:
    print("WhatsApp request timed out")
    return False

  except requests.exceptions.RequestException as error:
    print("WhatsApp request error:", error)
    return False


if __name__ == "__main__":
  send_whatsapp_message("RTX 5080","Amazon",60000,58000)