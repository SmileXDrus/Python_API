import requests
import pytest


class TestFirstAPI:
    names = [
        ('First_name'),
        ('Second_name'),
        ('')
    ]

    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        data = {'name': name}

        response = requests.get(url, params=data)
        assert response.status_code == 200, 'Status is not 200'

        response_dict = response.json()
        assert 'answer' in response_dict, "There is no field 'answer' in the response"
        if len(name) == 0:
            expected_response_text = 'Hello, someone'
        else:
            expected_response_text = f'Hello, {name}'
        actual_response_text = response_dict['answer']
        assert actual_response_text == expected_response_text, 'Actual text is not equal expected'


''' Запуск: 
python -m  pytest test_examples.py -k "test_name"

:param
-s          == show print statements in console
-x          == остановка после первого упавшего теста 
--maxfail=2 == остановка после первых двух упавших тестов
-k "name"   == запуск удовлетв условию наименования
-m slow     == запуск с меткой slow
-x --pdb    == вызывает отладчик при первом падении и завершает тестовую сессию
'''
