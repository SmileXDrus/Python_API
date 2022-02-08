import requests

payload = {"param1":"value1"}
header = {"SomeHeader": "sh"}
response = requests.get("https://playground.learnqa.ru/api/check_type", params=payload)
print("From GET:", response.text)
response1 = requests.post("https://playground.learnqa.ru/api/check_type", data=payload)
print("From POST:", response1.text, response1.status_code)
response3 = requests.post("https://playground.learnqa.ru/api/get_301", header)
first_response = response3.history[0]
print(first_response.url, '\n', response3.url, response3.headers['Server'])
