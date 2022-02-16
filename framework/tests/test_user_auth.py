import pytest
import requests
from framework.test_lib.base_case import BaseCase
from framework.test_lib.assertions import Assertions

class TestUserAuth(BaseCase):
    exclude_params = [
        ('no_cookie'),
        ('no_token'),
        ('')
    ]
    url_auth = 'https://playground.learnqa.ru/api/user/auth'

    def setup(self):
        url_login = 'https://playground.learnqa.ru/api/user/login'
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post(url_login, data=data)
        self.auth_sid = self.get_cookie(response1, 'auth_sid')
        self.token = self.get_header(response1, 'x-csrf-token')
        self.user_id = self.get_json_value(response1, 'user_id')

    def test_positive_auth_check(self):
        # auth_sid, token, user_id = self.get_response()
        response2 = requests.get(
            self.url_auth,
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response2,
            'user_id',
            self.user_id,
            'User id from login is not equal user id from auth request'
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        # auth_sid, token, user_id = self.get_response()

        if condition == 'no_cookie':
            response2 = requests.get(
                self.url_auth,
                headers={'x-csrf-token': self.token}
            )
        elif condition == 'no_token':
            response2 = requests.get(
                self.url_auth,
                cookies={"auth_sid": self.auth_sid}
            )
        else:
            response2 = requests.get(
                self.url_auth
            )
        Assertions.assert_json_value_by_name(
            response2,
            'user_id',
            0,
            'User is authorized with condition {condition}'
        )

