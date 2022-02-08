import json
from json.decoder import JSONDecodeError

json_str = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And ' \
           'this is a second message","timestamp":"2021-06-04 16:41:01"}]} '

json_dict = {
    "messages":
        [
            {"message": "This is the first message", "timestamp": "2021-06-04 16:40:53"},
            {"message": "And this is a second message", "timestamp": "2021-06-04 16:41:01"}
        ]
}
json_any = "something wrong"


def parsing_json_str(any_json):
    try:
        if (type(any_json)) == str:
            any_json = json.loads(any_json)
            print("str -> dict")
    except JSONDecodeError:
        print("Respons is not JSON format")
    if (type(any_json)) == dict:
        list_el = any_json['messages']
        print(list_el, type(list_el))
        print(list_el[1]['message'])
    else:
        print("Format is not str/dict")


parsing_json_str(json_str)
parsing_json_str(json_dict)
parsing_json_str(json_any)
