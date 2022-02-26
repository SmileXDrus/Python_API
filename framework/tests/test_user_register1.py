from framework.test_lib.assertions import Assertions
from framework.test_lib.base_case import BaseCase
from framework.test_lib.my_requests import MyRequests
from framework.tests.tests_data_test import *


class TestUserRegister(BaseCase):

    def test_create_user_success(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(URL_USER, data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post(URL_USER, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_bad_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post(URL_USER, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content: {response.content}"
