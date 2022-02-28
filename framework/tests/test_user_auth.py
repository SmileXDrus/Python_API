import allure
import pytest
from framework.test_lib.base_case import BaseCase
from framework.test_lib.assertions import Assertions
from framework.test_lib.my_requests import MyRequests
from framework.tests.tests_data_test import *


@allure.link('https://playground.learnqa.ru/api/map', name='LearnQA API')
@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ('no_cookie'),
        ('no_token'),
        ('')
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post(URL_LOGIN, data=data)
        self.auth_sid = self.get_cookie(response1, 'auth_sid')
        self.token = self.get_header(response1, 'x-csrf-token')
        self.user_id = self.get_json_value(response1, 'user_id')

    @allure.title("Positive test authorization")
    @allure.description("This test successfully authorize user by email and password")
    def test_positive_auth_check(self):
        # auth_sid, token, user_id = self.get_response()
        with allure.step('request to get token and auth_sid'):
            response2 = MyRequests.get(
                URL_AUTH,
                headers={"x-csrf-token": self.token},
                cookies={"auth_sid": self.auth_sid}
            )
        with allure.step('check user id from login is equal user id from auth request'):
            Assertions.assert_json_value_by_name(
                response2,
                'user_id',
                self.user_id,
                'User id from login is not equal user id from auth request'
            )

    @allure.description("This test checks authorization status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        # auth_sid, token, user_id = self.get_response()
        if condition == 'no_cookie':
            response2 = MyRequests.get(
                URL_AUTH,
                headers={'x-csrf-token': self.token}
            )
        elif condition == 'no_token':
            response2 = MyRequests.get(
                URL_AUTH,
                cookies={"auth_sid": self.auth_sid}
            )
        else:
            response2 = MyRequests.get(
                URL_AUTH
            )
        Assertions.assert_json_value_by_name(
            response2,
            'user_id',
            0,
            'User is authorized with condition {condition}'
        )
