import requests
# Надо написать скрипт, который делает следующее:
# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
# 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
# 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее.
# И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.

url_1 = "https://playground.learnqa.ru/ajax/api/compare_query_type"
method_list = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', '']


def first_ex(url):
    print('\n', "Start first_ex")
    response = requests.get(url)
    print(response.text)


def second_ex(url):
    print('\n', "Start second_ex")
    response = requests.patch(url)
    print(response.text)


def third_ex(url):
    print('\n',"Start third_ex")
    response = requests.get(url, params={"method": method_list[0]})
    print(response.text)
    response = requests.post(url, data={"method": method_list[1]})
    print(response.text)
    response = requests.put(url, data={"method": method_list[2]})
    print(response.text)
    response = requests.delete(url, data={"method": method_list[3]})
    print(response.text)


def fourth_ex(url):
    print('\n', "Start fourth_ex")
    for i in range(len(method_list)):
        method = method_list[i]
        print(i, ' with method:', method)
        response = requests.get(url, params={"method": method})
        if method != "GET" and response.text == '{"success":"!"}':
            print(f"Response GET with params {method} has wrong answer {response.text}")
        if method == "GET" and response.text != '{"success":"!"}':
            print(f"Response GET with params {method} has wrong answer {response.text}")

        response = requests.post(url, data={"method": method})
        if method != "POST" and response.text == '{"success":"!"}':
            print(f"Response POST with params {method} has wrong answer {response.text}")
        if method == "POST" and response.text != '{"success":"!"}':
            print(f"Response POST with params {method} has wrong answer {response.text}")

        response = requests.delete(url, data={"method": method})
        if method != "DELETE" and response.text == '{"success":"!"}':
            print(f"Response DELETE with params {method} has wrong answer {response.text}")
        if method == "DELETE" and response.text != '{"success":"!"}':
            print(f"Response DELETE with params {method} has wrong answer {response.text}")

        response = requests.put(url, data={"method": method})
        if method != "PUT" and response.text == '{"success":"!"}':
            print(f"Response PUT with params {method} has wrong answer {response.text}")
        if method == "PUT" and response.text != '{"success":"!"}':
            print(f"Response PUT with params {method} has wrong answer {response.text}")

        response = requests.patch(url, data={"method": method})
        if response.text != 'Wrong HTTP method':
            print(f"Response PATCH with params {method} has wrong answer {response.text}")


first_ex(url_1)
second_ex(url_1)
third_ex(url_1)
fourth_ex(url_1)
