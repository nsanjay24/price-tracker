import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.in/JBL-Wireless-Headphones-Speedcharge-Customize/dp/B09CYX92NB/ref=sr_1_7?crid=2WNVRZ0G9FUG1&dib=eyJ2IjoiMSJ9.n3iYhhfqM3LTOOgDbyu-5u1g5wp42CfAUnmAslAfSZxbLtNLQBWtwajfGjKN54ccs6Qo-qrMksCClcOqUer17fsEIcf6OmF3vaC4D6PrsEkw1yVtRAO0yrw36QYXfmSzlS28SflOr1bo35GfzdseL9tUxhurDb3V9C1EBKT59VARBaWsvqamTXQhIe43IAm_7tNcOxJjUSCsy3AWzgtheQKIQOep9D3IAPB3dphqREI.MXoOAdKORUST0pPOn2NDEHU9EyBvTUhrKp_rhTtuwd4&dib_tag=se&keywords=headset%2Bjbl&nsdOptOutParam=true&qid=1787420020&sprefix=%2Caps%2C361&sr=8-7&th=1"

# headers = {
#   "User-Agents" : "Mozilla/5.0"
# }

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}



response = requests.get(url , headers=headers, timeout=15)

print(response.text[:1000])

soup = BeautifulSoup(response.text, "html.parser")
title = soup.select_one("#productTitle")
print(title)

# print(response.url)