# 1) с помощью pytest необходимо написать тест, который просит ввести в консоли любую фразу короче 15 символов.
# А затем с помощью assert проверяет, что фраза действительно короче 15 символов.

import pytest


class TestSomeSimpleTests:

    @pytest.mark.first
    def test_check_input(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15

