import requests
from framework.test_lib.base_case import BaseCase
from framework.test_lib.assertions import Assertions
from framework.tests.tests_data_test import *


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        response1 = requests.post(URL_USER, data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post(URL_LOGIN, data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_name = "Changed Name"

        response3 = requests.put(
            f"{URL_USER}/{user_id}",
            headers={"x-csrf-token": token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # Get

        response4 = requests.get(f"{URL_USER}/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={'auth_sid': auth_sid})
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )


