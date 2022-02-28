import allure
from framework.test_lib.base_case import BaseCase
from framework.test_lib.assertions import Assertions
from framework.test_lib.my_requests import MyRequests
from framework.tests.tests_data_test import *

@allure.epic("Get cases")
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

        response2 = MyRequests.get(
            f"{URL_USER}{user_if_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_other_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post(URL_LOGIN, data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        # user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        new_user_id = self.create_user_with_random_email()

        response2 = MyRequests.get(
            f"{URL_USER}{new_user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )
        Assertions.assert_json_has_not_key(response2, 'email')
        Assertions.assert_json_has_not_key(response2, 'firstName')
        Assertions.assert_json_has_not_key(response2, 'lastName')
        Assertions.assert_json_has_key(response2, 'username')

    def create_user_with_random_email(self):
        data = self.prepare_registration_data()
        response = MyRequests.post(URL_USER, data=data)
        return self.get_json_value(response, 'id')
