# collect-only # https://habr.com/ru/post/269759/

import pytest
import requests
import data_test


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
        (data_test.USER_AGENT_5, data_test.Expected_values_5)]

    @pytest.mark.ex13
    @pytest.mark.parametrize("params_t", params)
    def test_check_header(self, params_t):
        (user_agent_t, expected_res_t) = params_t
        with_user_agent = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": user_agent_t}
        )
        dict_1 = with_user_agent.json()
        assert dict_1['platform'] == expected_res_t['platform'], f"For {user_agent_t}, correct platform expected: " \
                                                                 f"{expected_res_t['platform']} "
        assert dict_1['browser'] == expected_res_t['browser'], f"For {user_agent_t}, correct browser expected: " \
                                                               f"{expected_res_t['browser']}"
        assert dict_1['device'] == expected_res_t['device'], f"For {user_agent_t}, correct device expected: " \
                                                             f"{expected_res_t['device']}"
