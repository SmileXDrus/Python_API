import allure
import pytest
from framework.test_lib.assertions import Assertions
from framework.test_lib.base_case import BaseCase, get_random_string
from framework.test_lib.my_requests import MyRequests
from framework.tests.tests_data_test import *


@allure.epic("Register cases")
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

    # Проверка без @
    def test_create_user_with_bad_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post(URL_USER, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content: {response.content}"

    exclude_params = ['password', 'username', 'firstName', 'lastName', 'email']

    # Отсутствие любого параметра не дает зарегистрировать пользователя
    @pytest.mark.parametrize('exclude_param', exclude_params)
    def test_create_user_success(self, exclude_param):
        data = self.prepare_registration_data()
        del data[exclude_param]
        response = MyRequests.post(URL_USER, data=data)
        Assertions.assert_code_status(response, 400)
        # Assertions.assert_json_has_not_key(response, exclude_param)
        assert response.content.decode("utf-8") == f"The following required params are missed: {exclude_param}", \
            f"Unexpected response content: {response.content}"

    # Создание пользователя с очень коротким именем в один символ
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = 'x'
        response = MyRequests.post(URL_USER, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"Unexpected response content: {response.content}"

    #  Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['username'] = get_random_string(251)
        response = MyRequests.post(URL_USER, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f"Unexpected response content: {response.content}"
