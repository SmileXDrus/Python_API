import time

from framework.test_lib.assertions import Assertions
from framework.test_lib.base_case import BaseCase
from framework.test_lib.my_requests import MyRequests
from framework.tests.tests_data_test import *


class TestUserDelete(BaseCase):
    # попытка удалить пользователя по ID 2
    def test_delete_protected_user(self):
        # Login_protected_user
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post(URL_LOGIN, data=data)
        Assertions.assert_code_status(response1, 200)
        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id = self.get_json_value(response1, 'user_id')

        # Try delete
        response2 = MyRequests.delete(
            f"{URL_USER}{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content: {response2.content}"

        # GET: check is all right
        response3 = MyRequests.get(
            f"{URL_USER}{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response3, expected_fields)

    # Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить,
    # затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.
    def test_delete_created_user(self):
        id_user_1, email_user_1, psw_user_1 = self.create_user_with_random_email("auth")

        # LOGIN
        login_data = {
            'email': email_user_1,
            'password': psw_user_1
        }
        response1 = MyRequests.post(URL_LOGIN, data=login_data)
        auth_sid_user_1 = self.get_cookie(response1, "auth_sid")
        token_user_1 = self.get_header(response1, "x-csrf-token")

        # Delete
        response2 = MyRequests.delete(
            f"{URL_USER}{id_user_1}",
            headers={'x-csrf-token': token_user_1},
            cookies={'auth_sid': auth_sid_user_1}
        )
        Assertions.assert_code_status(response2, 200)

        # GET check deleted user_id
        response3 = MyRequests.get(f"{URL_USER}{id_user_1}")
        Assertions.assert_code_status(response3, 404)
        assert response3.text == 'User not found'

    # Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_user_as_other_user(self):
        id_user_1, email_user_1, psw_user_1 = self.create_user_with_random_email("auth")
        time.sleep(0.01)
        id_user_2 = self.create_user_with_random_email()

        # LOGIN
        login_data = {
            'email': email_user_1,
            'password': psw_user_1
        }
        response1 = MyRequests.post(URL_LOGIN, data=login_data)
        auth_sid_user_1 = self.get_cookie(response1, "auth_sid")
        token_user_1 = self.get_header(response1, "x-csrf-token")

        # Delete
        response2 = MyRequests.delete(
            f"{URL_USER}{id_user_2}",
            headers={'x-csrf-token': token_user_1},
            cookies={'auth_sid': auth_sid_user_1}
        )
        Assertions.assert_code_status(response2, 200)

        # GET check tried delete user_id
        response3 = MyRequests.get(f"{URL_USER}{id_user_2}")
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, 'username')

        # GET check auth (1) user_id
        response4 = MyRequests.get(f"{URL_USER}{id_user_1}")
        Assertions.assert_code_status(response4, 404)
        assert response4.text == 'User not found'


