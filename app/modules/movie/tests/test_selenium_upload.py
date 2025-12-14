import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.selenium.common import initialize_driver, close_driver


class TestDefaultSuite:

    def setup_method(self, method):
        self.driver = initialize_driver()
        self.host = os.getenv("SELENIUM_HOST", "http://localhost:5000")
        self.wait = WebDriverWait(self.driver, 10)

        current_dir = os.path.dirname(os.path.abspath(__file__))  # app/modules/movie/tests
        movie_module_dir = os.path.dirname(current_dir)  # app/modules/movie
        self.test_json_file = os.path.join(movie_module_dir, "json_examples", "movies5.json")

    
    def teardown_method(self, method):
        close_driver(self.driver)

    def open(self, path):
        self.driver.get(f"{self.host}{path}")
        time.sleep(1)

  

         # --------------------------------------------------------
    # TEST NUEVO - Upload como Draft + Upload y Publish directo
    # --------------------------------------------------------
    def test_upload_draft_and_publish_plus_direct_publish(self):
        """
        Test completo que hace:
        1. Login
        2. Upload dataset como DRAFT
        3. Upload otro dataset con PUBLISH directo
        4. Verificar que ambos están en "My datasets"
        """
        # Login
        self.open("/login")
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        
        # Ir a Upload dataset
        upload_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Upload dataset"))
        )
        upload_link.click()
        
        # === PARTE 1: Upload como DRAFT ===
        self.driver.find_element(By.ID, "title").send_keys("Ciencias y Naturaleza")
        self.driver.find_element(By.ID, "desc").send_keys("Dataset de prueba")
        self.driver.find_element(By.ID, "publication_doi").send_keys("10.1234/example15")
        self.driver.find_element(By.ID, "tags").send_keys("movie")
        self.driver.find_element(By.ID, "authors-0-orcid").send_keys("0000-0000-0000-0000")
        
        # Subir archivo
        file_input = self.driver.find_element(By.ID, "fileInput")
        file_input.send_keys(self.test_json_file)
        
        # Scroll al checkbox y hacer click
        agree_checkbox = self.driver.find_element(By.ID, "agree_terms")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", agree_checkbox)
        time.sleep(0.5)
        agree_checkbox.click()
        
        # Click en botón DRAFT
        draft_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "draft_btn"))
        )
        draft_btn.click()
        time.sleep(2)
        
        # Ir a "My datasets"
        my_datasets_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "My datasets"))
        )
        my_datasets_link.click()
        time.sleep(1)
        
        # Click en el botón "Manage" del primer draft
        manage_btns = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/manage']")
        if manage_btns:
            manage_btns[0].click()
        
        time.sleep(1)
        
        # Ahora estamos en la página de manage del draft
        # Click en el botón "publishBtn" (igual que en el código Selenium IDE)
        publish_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "publishBtn"))
        )
        publish_btn.click()
        time.sleep(3)  # Esperar a que se publique
        
        # === PARTE 2: Upload y Publish DIRECTO ===
        upload_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Upload dataset"))
        )
        upload_link.click()
        
        self.driver.find_element(By.ID, "title").send_keys("Prueba Upload y Publish")
        self.driver.find_element(By.ID, "desc").send_keys("Upload y Publish directo")
        self.driver.find_element(By.ID, "publication_doi").send_keys("10.1234/example25")
        self.driver.find_element(By.ID, "tags").send_keys("cinema")
        self.driver.find_element(By.ID, "authors-0-orcid").send_keys("0000-0000-0000")
        
        # Subir archivo
        file_input = self.driver.find_element(By.ID, "fileInput")
        file_input.send_keys(self.test_json_file)
        
        # Scroll al checkbox y hacer click
        agree_checkbox = self.driver.find_element(By.ID, "agree_terms")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", agree_checkbox)
        time.sleep(0.5)
        agree_checkbox.click()
        
        # Click en botón PUBLISH directo
        publish_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "publish_btn"))
        )
        publish_btn.click()
        time.sleep(2)
        
        # === VERIFICACIÓN: Ir a "My datasets" ===
        my_datasets_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "My datasets"))
        )
        my_datasets_link.click()
        time.sleep(1)
        
        # Verificar que los dos datasets están presentes
        page_source = self.driver.page_source
        assert "Ciencias y Naturaleza" in page_source, "Draft dataset not found in My datasets"
        assert "Prueba Upload y Publish" in page_source, "Published dataset not found in My datasets"
