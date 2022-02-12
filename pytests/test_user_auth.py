import pytest
import requests


class TestUserAuth:
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
        assert 'auth_sid' in response1.cookies, 'There is no auth cookie'
        assert 'x-csrf-token' in response1.headers, 'There is no x-csrt-token'
        assert 'user_id' in response1.json(), 'There is no user id'
        self.auth_sid = response1.cookies.get('auth_sid')
        self.token = response1.headers.get('x-csrf-token')
        self.user_id = response1.json()['user_id']

    def test_positive_auth_check(self):
        # auth_sid, token, user_id = self.get_response()
        response2 = requests.get(
            self.url_auth,
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        assert 'user_id' in response2.json(), 'There is not user id in second response'
        user_id_from_sec_response = response2.json()['user_id']
        assert self.user_id == user_id_from_sec_response, 'User id from login is not equal user id from auth request'

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
        assert 'user_id' in response2.json(), "There is no user id"
        user_id_from_check = response2.json()['user_id']
        assert user_id_from_check == 0, f'User is authorized with condition {condition}'

    ''' def get_response(self): # самописная реализация setup
        response1 = requests.post(self.url_login, data=self.data)

        assert 'auth_sid' in response1.cookies, 'There is no auth cookie'
        assert 'x-csrf-token' in response1.headers, 'There is no x-csrt-token'
        assert 'user_id' in response1.json(), 'There is no user id'
        auth_sid = response1.cookies.get('auth_sid')
        token = response1.headers.get('x-csrf-token')
        user_id = response1.json()['user_id']
        return auth_sid, token, user_id
    '''
