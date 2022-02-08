import requests
from json.decoder import JSONDecodeError

payload_1 = {"name": "boy"}
url_1 = "https://playground.learnqa.ru/api/hello"
url_redirect = "https://playground.learnqa.ru/api/long_redirect"


# Cколько редиректов происходит от изначальной точки назначения до итоговой. И какой URL итоговый.
def count_redirect(url):
    response = requests.get(url, allow_redirects=True)
    count = 0
    last = url
    for i in response.history:
        # print(i.url, i.status_code)
        count += 1
    print("Count redirect:", count-1, "\n", "Last url:", i.url)


count_redirect(url_redirect)


def get_param_from_json(url, payload):
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


