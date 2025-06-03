import requests
import allure
from graduate_work.config import api_url, my_headers


def check_search_movie(movie_title):
    """Этот метод выполняем GET-запрос к API с использованием названия фильма,
    проверяет, что запрос выполнен успешно, текст ответа содержит название
    фильма, ответ не пустой"""
    with allure.step("Отправляем запрос"):
        resp = requests.get(api_url + movie_title, headers=my_headers)
    with allure.step("Получаем ответ"):
        response_text = resp.text
    with allure.step("Проверяем статус-код"):
        assert resp.status_code == 200
    with allure.step("Проверяем, что название фильма "
                     "содержится в теле ответа"):
        assert movie_title in response_text
    with allure.step("Проверяем что длина ответа больше 0"):
        assert len(response_text) > 0


@allure.feature("Поиск фильма")
@allure.story("API")
@allure.title("Получение информации о фильме по названию на кириллице.")
@allure.suite("Позитивный тест")
def test_search_movie_title_in_cyrillic():
    check_search_movie("Красный шелк")


@allure.feature("Поиск фильма")
@allure.story("API")
@allure.title("Получение информации о фильме по названию на латинице.")
@allure.suite("Позитивный тест")
def test_search_movie_title_in_latin():
    check_search_movie("Red Silk")


@allure.feature("Поиск фильма")
@allure.story("API")
@allure.title("Получение информации о фильме по названию с цифрами.")
@allure.suite("Позитивный тест")
def test_search_movie_title_with_numbers():
    check_search_movie("Брат 2")


@allure.feature("Поиск фильма")
@allure.story("API")
@allure.title("Поиск фильма с невалидным токеном.")
@allure.suite("Негативный тест")
def test_search_movie_with_an_invalid_token():
    with allure.step("Отправляем запрос"):
        resp = requests.get(api_url+'Красный шелк',
                            headers={"X-API-KEY": "94XTKXG-1YMMA3D-M4P40E6"})
    with allure.step("Получаем ответ"):
        response_text = resp.text
    with allure.step("Проверяем статус-код"):
        assert resp.status_code == 401
    with allure.step("Проверяем, что в теле ответа"
                     " есть предупреждение об ошибке"):
        assert "Переданный токен некорректен!" in resp.text
    with allure.step("Проверяем что длина ответа больше 0"):
        assert len(response_text) > 0


@allure.feature("Поиск фильма")
@allure.story("API")
@allure.title("Поиск фильма без токена.")
@allure.suite("Негативный тест")
def test_search_movie_without_a_token():
    with allure.step("Отправляем запрос"):
        resp = requests.get(api_url+'Красный шелк')
    with allure.step("Получаем ответ"):
        response_text = resp.text
    with allure.step("Проверяем статус-код"):
        assert resp.status_code == 401
    with allure.step("Проверяем, что в теле ответа есть"
                     " предупреждение об ошибке"):
        assert "В запросе не указан токен!" in resp.text
    with allure.step("Проверяем что длина ответа больше 0"):
        assert len(response_text) > 0


def test_search_movie_method_put():
    resp = requests.put(api_url+'Красный шелк', headers=my_headers)
    with allure.step("Получаем ответ"):
        response_text = resp.text
    with allure.step("Проверяем статус-код"):
        assert resp.status_code == 404
    with allure.step("Проверяем, что в теле ответа есть"
                     " предупреждение об ошибке"):
        assert "Not Found" in resp.text
    with allure.step("Проверяем что длина ответа больше 0"):
        assert len(response_text) > 0
