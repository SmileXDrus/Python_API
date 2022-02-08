import json

import requests
from json.decoder import JSONDecodeError
payload = {"name":"boy"}
url = "https://playground.learnqa.ru/api/hello"
response = requests.get(url, payload, allow_redirects=False)
print("Response text:", response.text)

try:
    parsing_json = response.json()
    # parsing_json = json.loads(response.text)
    # print(type(parsing_json))
    key = "answer"
    if key in parsing_json:
        print(parsing_json[key])
    else:
        print(f"Key {key} not in obj")
except JSONDecodeError:
    print("Respons is not JSON format")
