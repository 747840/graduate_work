import allure
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.driver.get(url)
        self.driver.maximize_window()

    def _wait_for_elements(self, by, value, multiple=False, timeout=1):
        if multiple:
            return (WebDriverWait(self.driver, timeout).until
                    (EC.visibility_of_all_elements_located((by, value))))
        else:
            return (WebDriverWait(self.driver, timeout).
                    until(EC.visibility_of_element_located((by, value))))

    @allure.step("Поиск контента по фразе: {phrase}")
    def search_content_by_keyword(self, phrase):
        """Этот метод метод вводит фразу в поисковое поле
         и нажимает на кнопку Поиск."""
        self._wait_for_elements(By.CSS_SELECTOR,
                                "input[name=kp_query]").send_keys(phrase)
        self.driver.find_element(By.CSS_SELECTOR,
                                 "button[type=submit]").click()

    @allure.step("Получаем список найденных элементов")
    def _get_element_texts(self, css_selector):
        """Этод метод возвращает список найденных элементов"""
        elements = self._wait_for_elements(By.CSS_SELECTOR,
                                           css_selector, multiple=True)
        return [element.text for element in elements]

    @allure.step("Получаем названия фильмов")
    def get_movie_titles(self):
        """Этот метод проверяет что в списке есть фильм, который мы ищем"""
        return self._get_element_texts("[data-type='film']")

    @allure.step("Получаем имя персоны")
    def get_person_titles(self):
        """Этот метод проверяет что в списке есть персона, которую мы ищем"""
        return self._get_element_texts("[data-type='person']")

    @allure.step("Получаем количество результатов поиска")
    def get_search_results_count(self):
        """Этот метод определяет колличество найденных элементов"""
        results_text = self._wait_for_elements(By.CSS_SELECTOR,
                                               ".search_results_topText").text
        match = re.search(r'результаты:\s*(\d+)', results_text)
        if match:
            return int(match.group(1))
        else:
            return 0
