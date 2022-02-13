# 1) с помощью pytest необходимо написать тест, который просит ввести в консоли любую фразу короче 15 символов.
# А затем с помощью assert проверяет, что фраза действительно короче 15 символов.

import pytest
import requests


class TestSomeSimpleTests:

    @pytest.mark.first
    def test_check_input(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15

    @pytest.mark.second
    def test_check_cookie(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
        if response.cookies.values() is not None:
            print("first way: ", response.cookies.values()[0])
            dict_1 = response.cookies.get_dict()
            print(dict_1)
            if 'HomeWork' in dict_1:
                print("second way", dict_1["HomeWork"])
            assert dict_1["HomeWork"] == 'hw_value'

