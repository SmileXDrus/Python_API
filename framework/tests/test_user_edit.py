import time
import allure
import pytest
from framework.test_lib.base_case import BaseCase
from framework.test_lib.assertions import Assertions
from framework.test_lib.my_requests import MyRequests
from framework.tests.tests_data_test import *


@allure.epic("Edit cases")
class TestUserEdit(BaseCase):
    def test_edit_just_created_user_positive(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(URL_USER, data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post(URL_LOGIN, data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"{URL_USER}{user_id}",
            headers={"x-csrf-token": token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # Get
        response4 = MyRequests.get(f"{URL_USER}{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={'auth_sid': auth_sid})
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_as_auth_other_user(self):
        id_user_1, email_user_1, psw_user_1 = self.create_user_with_random_email("auth")
        time.sleep(0.01)
        id_user_2, first_name_user_2, email_user_2, psw_user_2 = self.create_user_with_random_email("firstName")
        new_name = "Changed Name"

        # Login user1
        login_data = {
            'email': email_user_1,
            'password': psw_user_1
        }
        response1 = MyRequests.post(URL_LOGIN, data=login_data)
        auth_sid_user_1 = self.get_cookie(response1, "auth_sid")
        token_user_1 = self.get_header(response1, "x-csrf-token")

        # Edit user2
        response2 = MyRequests.put(
            f"{URL_USER}{id_user_2}",
            headers={"x-csrf-token": token_user_1},
            cookies={'auth_sid': auth_sid_user_1},
            data={'firstName': new_name}
        )
        Assertions.assert_code_status(response2, 200)

        # Login user2
        login_data = {
            'email': email_user_2,
            'password': psw_user_2
        }
        response3 = MyRequests.post(URL_LOGIN, data=login_data)
        auth_sid_user_2 = self.get_cookie(response3, "auth_sid")
        token_user_2 = self.get_header(response3, "x-csrf-token")

        # Get user2
        response4 = MyRequests.get(f"{URL_USER}{id_user_2}",
                                   headers={"x-csrf-token": token_user_2},
                                   cookies={'auth_sid': auth_sid_user_2})
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            first_name_user_2,
            "Wrong name of the user after edit"
        )

        # Get user1
        response5 = MyRequests.get(f"{URL_USER}{id_user_1}",
                                   headers={"x-csrf-token": token_user_1},
                                   cookies={'auth_sid': auth_sid_user_1})
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_value_by_name(
            response5,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # Попытаемся изменить данные пользователя, будучи неавторизованными
    users_data = ['username', 'firstName', 'lastName', 'password', 'email']

    @pytest.mark.parametrize("user_data", users_data)
    def test_edit_user_as_no_auth_user(self, user_data):
        id_user_1, user_name_user_1, first_name_user_1, last_name_user_1, email_user_1, psw_user_1 \
            = self.create_user_with_random_email("all")
        new_name = "Changed Name"

        # Edit user
        response1 = MyRequests.put(
            f"{URL_USER}{id_user_1}",
            data={user_data: new_name}
        )
        Assertions.assert_code_status(response1, 400)

        # Login user1
        login_data = {
            'email': email_user_1,
            'password': psw_user_1
        }
        response2 = MyRequests.post(URL_LOGIN, data=login_data)
        auth_sid_user_1 = self.get_cookie(response2, "auth_sid")
        token_user_1 = self.get_header(response2, "x-csrf-token")

        # Get user
        response3 = MyRequests.get(f"{URL_USER}{id_user_1}",
                                   headers={"x-csrf-token": token_user_1},
                                   cookies={'auth_sid': auth_sid_user_1})
        Assertions.assert_code_status(response3, 200)
        if user_data == 'password':
            Assertions.assert_json_has_not_key(response3, user_data)
        elif user_data == 'email':
            Assertions.assert_json_value_by_name(
                response3,
                user_data,
                email_user_1,
                "Wrong name of the user after edit"
            )
        else:
            Assertions.assert_json_value_by_name(
                response3,
                user_data,
                "learnqa",
                "Wrong name of the user after edit"
            )

    # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем,
    # на новый email без символа @
    def test_edit_incorrect_email_by_auth_user(self):
        id_user_1, email_user_1, psw_user_1 = self.create_user_with_random_email("auth")
        new_email = "changedemail.com"

        # Login user1
        login_data = {
            'email': email_user_1,
            'password': psw_user_1
        }
        response1 = MyRequests.post(URL_LOGIN, data=login_data)
        auth_sid_user_1 = self.get_cookie(response1, "auth_sid")
        token_user_1 = self.get_header(response1, "x-csrf-token")

        # Edit user
        response2 = MyRequests.put(
            f"{URL_USER}{id_user_1}",
            headers={"x-csrf-token": token_user_1},
            cookies={'auth_sid': auth_sid_user_1},
            data={'email': new_email}
        )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content: {response2.content}"

        # Get user
        response3 = MyRequests.get(f"{URL_USER}{id_user_1}",
                                   headers={"x-csrf-token": token_user_1},
                                   cookies={'auth_sid': auth_sid_user_1})
        Assertions.assert_code_status(response3, 200)

        Assertions.assert_json_value_by_name(
            response3,
            "email",
            email_user_1,
            "Wrong name of the user after edit"
        )

    # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем,
    # на очень короткое значение в один символ
    def test_edit_firstname_to_short_str(self):
        id_user_1, firstname_user_1, email_user_1, psw_user_1 = self.create_user_with_random_email("firstName")
        new_firstname = "x"

        # Login user1
        login_data = {
            'email': email_user_1,
            'password': psw_user_1
        }
        response1 = MyRequests.post(URL_LOGIN, data=login_data)
        auth_sid_user_1 = self.get_cookie(response1, "auth_sid")
        token_user_1 = self.get_header(response1, "x-csrf-token")

        # Edit user
        response2 = MyRequests.put(
            f"{URL_USER}{id_user_1}",
            headers={"x-csrf-token": token_user_1},
            cookies={'auth_sid': auth_sid_user_1},
            data={'firstName': new_firstname}
        )
        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_has_key(response2, 'error')

        # Get user
        response3 = MyRequests.get(f"{URL_USER}{id_user_1}",
                                   headers={"x-csrf-token": token_user_1},
                                   cookies={'auth_sid': auth_sid_user_1})
        Assertions.assert_code_status(response3, 200)

        Assertions.assert_json_value_by_name(
            response3,
            "firstName",
            firstname_user_1,
            "Wrong name of the user after edit"
        )

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
