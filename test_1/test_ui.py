import pytest
import allure
from graduate_work.page.main_page import MainPage
from selenium import webdriver
from graduate_work.config import main_url


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver):
    driver.get(main_url)
    return MainPage(driver, main_url)


@allure.feature("Поиск")
@allure.story("UI")
@allure.title("Поиск фильмов по названию")
@allure.suite("Позитивный тест")
@pytest.mark.parametrize("film_title",
                         ["Асса", "Пи", "Красный шелк"])
def test_search_films_by_title_positive(main_page, film_title):
    with allure.step(f"Поиск фильмов по названию"
                     f" {film_title}"):
        main_page.search_content_by_keyword(film_title)
    with allure.step("Количество результатов больше 0"):
        assert main_page.get_search_results_count() > 0
    with allure.step("Название фильма содержится в результатах"):
        assert film_title in main_page.get_movie_titles()


@allure.feature("Поиск")
@allure.story("UI")
@allure.title("Поиск фильмов по названию")
@allure.suite("Негативный тест")
@pytest.mark.parametrize("film_title",
                         ["☺", "мульбурга", "   "])
def test_search_films_by_title_negative(main_page, film_title):
    with allure.step(f"Поиск фильмов по названию"
                     f" {film_title}"):
        main_page.search_content_by_keyword(film_title)
    with allure.step("Количество результатов 0"):
        assert main_page.get_search_results_count() == 0


@allure.feature("Поиск")
@allure.story("UI")
@allure.title("Поиск персоны по имени")
@allure.suite("Позитивный тест")
@pytest.mark.parametrize("person_title",
                         ["Андрей И", "Евгений Миронов", "Том Круз"])
def test_search_person_by_title_positive(main_page, person_title):
    with allure.step(f"Поиск персоны по имени"
                     f" {person_title}"):
        main_page.search_content_by_keyword(person_title)
    with allure.step("Количество результатов больше 0"):
        assert main_page.get_search_results_count() > 0
    with allure.step("Имя персона содержится в результатах"):
        assert person_title in main_page.get_person_titles()


@allure.feature("Поиск")
@allure.story("UI")
@allure.title("Поиск персоны по имени")
@allure.suite("Негативный тест")
@pytest.mark.parametrize("person_title",
                         ["☺", "    ", "мульбурга"])
def test_search_person_by_title_negative(main_page, person_title):
    with allure.step(f"Поиск персоны по имени"
                     f" {person_title}"):
        main_page.search_content_by_keyword(person_title)
    with allure.step("Количество результатов 0"):
        assert main_page.get_search_results_count() == 0
