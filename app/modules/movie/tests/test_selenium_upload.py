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

    def scroll_and_click(self, by, value, use_js_click=True):
        """
        Helper method para encontrar elemento, hacer scroll y click de forma segura.
        Siempre busca el elemento fresco para evitar StaleElementReference.
        """
        element = self.wait.until(EC.presence_of_element_located((by, value)))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.8)
        
        if use_js_click:
            self.driver.execute_script("arguments[0].click();", element)
        else:
            element.click()
        
        return element

    def safe_send_keys(self, by, value, text, clear_first=True):
        """
        Método mejorado que hace scroll al elemento antes de interactuar
        """
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        
        # Hacer scroll al elemento antes de interactuar
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.5)
        
        if clear_first:
            element.clear()
        element.send_keys(text)


    # --------------------------------------------------------
    # TEST NUEVO - Upload como Draft + Upload y Publish directo
    # --------------------------------------------------------
    def test_upload_draft_and_publish_plus_direct_publish(self):
        """
        Test completo que hace:
        1. Login
        2. Upload dataset como DRAFT
        3. Publicar el draft desde "My datasets"
        4. Upload otro dataset con PUBLISH directo
        5. Editar metadata dos veces
        6. Verificar changelog
        """
        # ======================================================
        # PARTE 1: LOGIN
        # ======================================================
        self.open("/login")
        self.safe_send_keys(By.ID, "email", "user1@example.com", clear_first=False)
        self.safe_send_keys(By.ID, "password", "1234", clear_first=False)
        self.scroll_and_click(By.ID, "submit")
        time.sleep(1)
        
        # ======================================================
        # save draft
        # ======================================================
        self.scroll_and_click(By.LINK_TEXT, "Upload dataset")
        
        self.safe_send_keys(By.ID, "title", "Ciencias y Naturaleza", clear_first=False)
        self.safe_send_keys(By.ID, "desc", "Dataset de prueba", clear_first=False)
        self.safe_send_keys(By.ID, "publication_doi", "10.1234/example15", clear_first=False)
        self.safe_send_keys(By.ID, "tags", "movie", clear_first=False)
        self.safe_send_keys(By.ID, "authors-0-orcid", "0000-0000-0000", clear_first=False)
        
        file_input = self.driver.find_element(By.ID, "fileInput")
        file_input.send_keys(self.test_json_file)
        
        self.scroll_and_click(By.ID, "agree_terms")
        self.scroll_and_click(By.ID, "draft_btn")
        time.sleep(2)
        
        # ======================================================
        # publish draft
        # ======================================================
        self.scroll_and_click(By.LINK_TEXT, "My datasets")
        time.sleep(1)
        manage_btn = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//tr[.//a[contains(text(), 'Ciencias y Naturaleza')]]" +
                "//a[contains(@href, '/manage')]"
            ))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", manage_btn)
        time.sleep(0.8)
        self.driver.execute_script("arguments[0].click();", manage_btn)
        time.sleep(1)
        
        # Publicar el draft
        self.scroll_and_click(By.ID, "publishBtn")
        time.sleep(3)
        
        # ======================================================
        # Upload and publish
        # ======================================================
        self.scroll_and_click(By.LINK_TEXT, "Upload dataset")
        
        self.safe_send_keys(By.ID, "title", "Prueba Upload y Publish", clear_first=False)
        self.safe_send_keys(By.ID, "desc", "Upload y Publish directo", clear_first=False)
        self.safe_send_keys(By.ID, "publication_doi", "10.1234/example25", clear_first=False)
        self.safe_send_keys(By.ID, "tags", "cinema", clear_first=False)
        self.safe_send_keys(By.ID, "authors-0-orcid", "0000-0000-0000", clear_first=False)
        
        file_input = self.driver.find_element(By.ID, "fileInput")
        file_input.send_keys(self.test_json_file)
        
        self.scroll_and_click(By.ID, "agree_terms")
        self.scroll_and_click(By.ID, "publish_btn")
        time.sleep(2)
        
        self.scroll_and_click(By.LINK_TEXT, "My datasets")
        time.sleep(1)
        
        # Verificar que los dos datasets están presentes
        page_source = self.driver.page_source
        assert "Ciencias y Naturaleza" in page_source, "Draft dataset not found in My datasets"
        assert "Prueba Upload y Publish" in page_source, "Published dataset not found in My datasets"
        
        # ======================================================
        # editar metadatos
        # ======================================================
        # Click en el dataset "Prueba Upload y Publish"
        self.scroll_and_click(By.LINK_TEXT, "🎬 Prueba Upload y Publish")
        time.sleep(1)
        
        self.scroll_and_click(By.LINK_TEXT, "Edit Metadata")
        time.sleep(1)
        
        # Cambiar título
        self.safe_send_keys(By.ID, "title", "Esto es una prueba para editar el título")
        self.scroll_and_click(By.ID, "add-author")
        time.sleep(0.5)
        
        self.safe_send_keys(By.NAME, "authors-1-name", "Carmona Reina, Alejandro", clear_first=False)
        self.safe_send_keys(By.NAME, "authors-1-affiliation", "Universidad de Sevilla", clear_first=False)
        self.safe_send_keys(By.ID, "edit_comment", "Edición 1", clear_first=False)
        
        self.scroll_and_click(By.ID, "add-author")
        time.sleep(0.5)
        
        self.safe_send_keys(By.NAME, "authors-2-name", "Román, Darío", clear_first=False)
        self.safe_send_keys(By.NAME, "authors-2-affiliation", "Universidad de Sevilla", clear_first=False)
        
        # Guardar cambios
        self.scroll_and_click(By.CSS_SELECTOR, ".btn-primary")
        time.sleep(1)
        
        # ======================================================
        # ver cambios
        # ======================================================
        self.scroll_and_click(By.LINK_TEXT, "Edit Metadata")
        time.sleep(1)
        
        # Buscar link de changelog dinámicamente (puede cambiar el ID del dataset)
        changelog_link = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/changelog')]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", changelog_link)
        time.sleep(0.8)
        self.driver.execute_script("arguments[0].click();", changelog_link)
        time.sleep(1)
        
        # Volver al dataset
        self.scroll_and_click(By.LINK_TEXT, "Back to Dataset")
        time.sleep(1)
        
        # ======================================================
        # editar metadatos de nuevo (ver si se borran autores)
        # ======================================================
        self.scroll_and_click(By.LINK_TEXT, "Edit Metadata")
        time.sleep(1)
        
        # Modificar nombre del segundo autor
        self.safe_send_keys(By.ID, "authors-1-name", "Carmona Reina, Pepe")
        self.safe_send_keys(By.ID, "edit_comment", "Ahora verifico que se editan y borran bien los autores")
        
        # Cambiar tags
        self.safe_send_keys(By.ID, "tags", "cinema, disney")
        
        delete_author_btn = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//div[contains(@class, 'card')][3]//button[contains(@class, 'btn-danger')] | " +
                "//div[contains(@class, 'card')][3]//path"
            ))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", delete_author_btn)
        time.sleep(0.8)
        self.driver.execute_script("arguments[0].click();", delete_author_btn)
        time.sleep(0.5)
        
        # Guardar cambios
        self.scroll_and_click(By.CSS_SELECTOR, ".btn-primary")
        time.sleep(1)
        
        # ======================================================
        # changelog final
        # ======================================================
        self.scroll_and_click(By.LINK_TEXT, "Edit Metadata")
        time.sleep(1)
        
        changelog_link = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//a[contains(text(), 'View Full Changelog') or contains(@href, '/changelog')]"
            ))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", changelog_link)
        time.sleep(0.8)
        self.driver.execute_script("arguments[0].click();", changelog_link)
        time.sleep(1)
        
        # Verificar que hay entradas en el changelog
        page_source = self.driver.page_source
        assert "Edición 1" in page_source, "Primera edición no encontrada en changelog"
        assert "Ahora verifico que se editan y borran bien los autores" in page_source, "Segunda edición no encontrada en changelog"
        
        print("Test completado exitosamente")