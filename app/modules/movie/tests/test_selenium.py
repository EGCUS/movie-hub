import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.selenium.common import initialize_driver, close_driver


class TestDefaultSuite:

    def setup_method(self, method):
        self.driver = initialize_driver()
        self.host = "http://web:5000"
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        close_driver(self.driver)

    def open(self, path):
        self.driver.get(f"{self.host}{path}")
        time.sleep(1)

    # --------------------------------------------------------
    # TEST 1 — comprobar listado accesible
    # --------------------------------------------------------
    def test_explore_datasets_home(self):
        self.open("/moviedataset/list")

        assert ("Movie" in self.driver.page_source 
                or "movies" in self.driver.page_source.lower())

    # --------------------------------------------------------
    # TEST 2 — abrir dataset Sci-Fi
    # --------------------------------------------------------
    def test_open_scifi_dataset(self):
        self.open("/moviedataset/list")

        dataset_link = self.wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Sci-Fi"))
        )
        dataset_link.click()

        assert "Sci-Fi" in self.driver.page_source

    # --------------------------------------------------------
    # TEST 4 — abrir selector de versiones
    # --------------------------------------------------------
    def test_open_versions_selector(self):
        self.open("/moviedataset/list")

        link = self.wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Sci-Fi"))
        )
        link.click()

        versions_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a[href*='/versions']")
            )
        )
        versions_btn.click()

        assert "/versions" in self.driver.current_url

    # --------------------------------------------------------
    # TEST 5 — comparar sin selección (alert JS)
    # --------------------------------------------------------
    def test_compare_without_selection(self):
        self.open("/moviedataset/list")

        link = self.wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Sci-Fi"))
        )
        link.click()

        versions_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/versions']"))
        )
        versions_btn.click()

        compare_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "compareBtn"))
        )
        compare_btn.click()

        # Capturar alerta real
        alert = self.driver.switch_to.alert
        assert "select" in alert.text.lower()
        alert.accept()

    def test_view_movie_collection(self):
      self.open("/moviedataset/list")

      link = self.wait.until(
          EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Sci-Fi"))
      )
      link.click()

      # Carrusel debería existir
      carousel = self.wait.until(
          EC.presence_of_element_located((By.ID, "carouselTrack"))
      )

      movies = self.driver.find_elements(By.CSS_SELECTOR, ".carousel-item")
      assert len(movies) >= 1, "No movie items found in the carousel"

      # Comprobar que el título de la primera película aparece en detalles
      title_el = self.driver.find_element(By.ID, "movieTitle")
      assert len(title_el.text.strip()) > 0

    def test_download_dataset_button(self):
      self.open("/moviedataset/list")

      link = self.wait.until(
          EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Sci-Fi"))
      )
      link.click()

      dl_btn = self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-success"))
      )
      current = self.driver.current_url
      dl_btn.click()
      time.sleep(1)

      # La URL NO cambia, porque se está descargando un ZIP
      assert self.driver.current_url == current

    
    def test_open_file_preview(self):
      self.open("/moviedataset/list")

      link = self.wait.until(
          EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Sci-Fi"))
      )
      link.click()

      view_btn = self.wait.until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-outline-secondary"))
      )

      # Scroll para que sea clicable
      self.driver.execute_script("arguments[0].scrollIntoView(true);", view_btn)
      time.sleep(0.5)

      self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-outline-secondary")))
      view_btn.click()

      modal = self.wait.until(
          EC.visibility_of_element_located((By.ID, "fileContent"))
      )

      assert len(modal.text.strip()) > 0

    
    def test_login_wrong_password(self):
      self.open("/login")

      self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
      self.driver.find_element(By.ID, "password").send_keys("wrongpass")
      self.driver.find_element(By.ID, "submit").click()
      time.sleep(1)

      # Si falla, NO redirige → sigue en /login
      assert "/login" in self.driver.current_url

