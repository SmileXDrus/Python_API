# collect-only # https://habr.com/ru/post/269759/
import json

import pytest
import requests
from requests import Response

from pytests import data_test


class TestSomeSimpleTests:

    @pytest.mark.ex10
    def test_check_input(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15

    @pytest.mark.ex11
    def test_check_cookie(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
        if response.cookies.values() is not None:
            print("first way: ", response.cookies.values()[0])
            dict_1 = response.cookies.get_dict()
            print(dict_1)
            if 'HomeWork' in dict_1:
                print("second way", dict_1["HomeWork"])
            assert dict_1["HomeWork"] == 'hw_value'

    @pytest.mark.ex12
    def test_check_header(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_header')
        items = response.headers.items()
        if items is not None:
            answer = response.headers.get('x-secret-homework-header')  # first way
            for key, value in items:  # second way
                if 'x-secret-homework-header' in key:
                    print(value)
                    assert answer == value, "It is not required header "
            print(answer)
            assert answer == 'Some secret value', "It is not required header"

    params = [
        (data_test.USER_AGENT_1, data_test.Expected_values_1),
        (data_test.USER_AGENT_2, data_test.Expected_values_2),
        (data_test.USER_AGENT_3, data_test.Expected_values_3),
        (data_test.USER_AGENT_4, data_test.Expected_values_4),
        (data_test.USER_AGENT_5, data_test.Expected_values_5)
    ]
    args = [
        'platform',
        'browser',
        'device'
    ]

    @pytest.mark.ex13
    @pytest.mark.parametrize("arg", args)
    @pytest.mark.parametrize("params_t", params)
    def test_check_header(self, params_t, arg):
        (user_agent_t, expected_res_t) = params_t
        with_user_agent = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": user_agent_t}
        )

        self.assert_json_value_by_name(
            user_agent_t,
            with_user_agent,
            arg,
            expected_res_t[arg]
        )
        self.assert_json_value_by_name(
            user_agent_t,
            with_user_agent,
            arg,
            expected_res_t[arg]
        )
        self.assert_json_value_by_name(
            user_agent_t,
            with_user_agent,
            arg,
            expected_res_t[arg]
        )

    @staticmethod
    def assert_json_value_by_name(user_agent_t, response: Response, name, expected_value):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        assert name in response_as_dict, f'Cannot find key {name}'
        assert response_as_dict[name] == expected_value, f"For {user_agent_t}, " \
                                                         f"browser expected: {expected_value}, " \
                                                         f"but actual is {response_as_dict[name]} " \
