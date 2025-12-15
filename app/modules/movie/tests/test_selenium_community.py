import time
import json
import os
import tempfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.selenium.common import initialize_driver, close_driver


class TestCommunityUpload:

    def setup_method(self, method):
        self.driver = initialize_driver()
        self.host = "http://web:5000"
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        close_driver(self.driver)

    def open(self, path):
        self.driver.get(f"{self.host}{path}")
        time.sleep(1)

    def test_upload_form_shows_community_fields(self):
        self.open("/login")

        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)

        self.open("/moviedataset/upload")

        community_select = self.wait.until(
            EC.presence_of_element_located((By.NAME, "community_id"))
        )
        assert community_select is not None

        new_name = self.driver.find_element(By.NAME, "new_community_name")
        assert new_name is not None

        new_logo = self.driver.find_element(By.NAME, "new_community_logo")
        assert new_logo is not None


class TestCommunitySuite:

    def login(self, email="user1@example.com", password="1234"):
        self.open("/login")

        self.wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)

        assert "/login" not in self.driver.current_url

    def setup_method(self, method):
        self.driver = initialize_driver()
        self.host = "http://web:5000"
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        close_driver(self.driver)

    def open(self, path):
        self.driver.get(f"{self.host}{path}")
        time.sleep(1)

    def test_upload_creates_new_community_draft(self):
        self.login()
        self.open("/moviedataset/upload")

        assert "/moviedataset/upload" in self.driver.current_url

        community_name = f"ComunidadSelenium_{int(time.time())}"

        self.wait.until(EC.presence_of_element_located((By.ID, "title"))).send_keys(
            f"Dataset Selenium {community_name}"
        )
        self.driver.find_element(By.NAME, "desc").send_keys("Dataset creado desde Selenium")
        self.driver.find_element(By.NAME, "tags").send_keys("selenium,test")

        author_name = self.driver.find_element(By.ID, "authors-0-name")
        assert author_name.get_attribute("readonly") is not None
        assert author_name.get_attribute("value")

        self.driver.find_element(By.NAME, "new_community_name").send_keys(community_name)

        tmp_dir = tempfile.mkdtemp()
        json_path = os.path.join(tmp_dir, "movies.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({"movies": [{"title": "A", "year": 2020, "director": "D"}]}, f)

        file_input = self.driver.find_element(By.NAME, "file")
        file_input.send_keys(json_path)

        agree = self.driver.find_element(By.ID, "agree_terms")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", agree)
        time.sleep(0.3)
        if not agree.is_selected():
            agree.click()

        draft_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='action'][value='draft']"))
        )
        draft_btn.click()

        time.sleep(1)

        assert "success=true" in self.driver.current_url
        assert "action=draft" in self.driver.current_url
        assert "dataset_id=" in self.driver.current_url
