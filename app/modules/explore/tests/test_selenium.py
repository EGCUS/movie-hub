import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.selenium.common import initialize_driver, close_driver


class TestExploreFilters:

    def setup_method(self, method):
        self.driver = initialize_driver()
        self.host = "http://web:5000"
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        close_driver(self.driver)

    def open(self, path):
        self.driver.get(f"{self.host}{path}")
        time.sleep(1)

    def test_explore_filter_by_text(self):
        self.open("/explore")

        # Esperar a que carguen resultados (ajusta selector si hace falta)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card")))

        initial_results = self.driver.find_elements(By.CSS_SELECTOR, ".card")
        assert len(initial_results) > 0

        # Si tu filtro usa el input de arriba del navbar:
        search_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "search-query"))
        )
        search_input.clear()
        search_input.send_keys("Sci")
        search_input.submit()

        time.sleep(2)

        filtered_results = self.driver.find_elements(By.CSS_SELECTOR, ".card")
        assert len(filtered_results) > 0
        assert len(filtered_results) <= len(initial_results)
