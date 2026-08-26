import requests
from bs4 import BeautifulSoup
import re



url = "https://buyhatke.com/amazon-jbl-tune-770nc-wireless-over-ear-headphones-with-adaptive-noise-cancellation-upto-70h-battery-smart-ambient-speed-charge-customized-eq-google-fas-price-in-india-63-65866191"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9"
}

response = requests.get(
    url,
    headers=headers,
    timeout=15
)

api_links = re.findall(r'https?://[^"\']+', response.text)

for link in api_links:
    if "api" in link.lower():
        print(link)

# print("Status:", response.status_code)
# print(response.text[:500])

# soup = BeautifulSoup(response.text, "html.parser")
# title = soup.select_one("#productTitle")
# print(title)

# print("JBL" in response.text)
# print("₹" in response.text)
# print("price" in response.text.lower())