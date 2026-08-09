import requests
response = requests.get("https://jsonplaceholder.typicode.com/todos/101")
print(response)
data = response.json()
print(data["title"])