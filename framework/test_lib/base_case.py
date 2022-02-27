import json.decoder
import random
import string
from datetime import datetime
from requests import Response
from framework.test_lib.my_requests import MyRequests
from framework.tests.tests_data_test import *


def get_random_string(lenn):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(lenn))
    return rand_string


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f'Cannot find cookie with name {cookie_name} in the last response'
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f'Cannot find header with name {header_name} in the last response'
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in Json format. Response text is {response.text}'
        assert name in response_as_dict, f'Response doesn"t have key {name}'
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_port = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_port}{random_part}@{domain}"
        return {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def create_user_with_random_email(self, param: str = None):
        data = self.prepare_registration_data()
        response = MyRequests.post(URL_USER, data=data)
        if param == "all":
            return self.get_json_value(response, 'id'), data["username"], \
                   data["firstName"], data["lastName"], data["email"], data["password"]
        elif param == "firstName":
            return self.get_json_value(response, 'id'), data["firstName"], data["email"], data["password"]
        elif param == "auth":
            return self.get_json_value(response, 'id'), data["email"], data["password"]
        elif param == "username":
            return self.get_json_value(response, 'id'), data["username"]
        else:
            return self.get_json_value(response, 'id')

