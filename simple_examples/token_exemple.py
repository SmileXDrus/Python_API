import json
import time
import requests
from json import JSONDecodeError


def get_param(strng, key):
    try:
        prs_json = json.loads(strng)
        if key in prs_json:
            return prs_json[key]
        else:
            print(f"Key {key} not in json")
    except JSONDecodeError:
        print("Respons is not JSON format")


url_1 = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url_1)
print(response.text)
pause = get_param(response.text, 'seconds')
token = get_param(response.text, 'token')

response_check = requests.get(url_1, params={"token": token})
transit_status = get_param(response_check.text, 'status')
if transit_status == 'Job is NOT ready':
    print(f"Transitional status test passed. Status = {transit_status}")
    time.sleep(pause)
    response = requests.get(url_1, params={"token": token})
    result = get_param(response.text, 'result')
    status = get_param(response.text, 'status')
    if result is not None:
        print(get_param(response.text, 'result'))
    if status == "Job is ready":
        print(f"Final status test passed. Status = {status}")
else:
    print(f"Transitional status test not passed. Status = {transit_status}")




