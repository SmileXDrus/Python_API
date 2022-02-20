from datetime import datetime

import pytest
import requests

from framework.test_lib.assertions import Assertions
from framework.test_lib.base_case import BaseCase


class TestUserRegister:
    def setup(self):
        base_port = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_port}{random_part}@{domain}"


    def test_create_user_success(self):
        data = {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"
