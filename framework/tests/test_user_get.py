from framework.test_lib.base_case import BaseCase
from framework.test_lib.assertions import Assertions
from framework.test_lib.my_requests import MyRequests
from framework.tests.tests_data_test import *


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get(f"{URL_USER}2")
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post(URL_LOGIN, data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_if_from_auth_method = self.get_json_value(response1, 'user_id')

        print(auth_sid)
        print(token)
        response2 = MyRequests.get(
            f"{URL_USER}{user_if_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

