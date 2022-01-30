import requests

url = "https://playground.learnqa.ru/api/get_text"
response = requests.get(url)
t = response.text
print(t)