from locust import HttpUser, TaskSet, task, between
from core.environment.host import get_host_for_locust_testing
from core.locust.common import fake, get_csrf_token
from bs4 import BeautifulSoup
import random


class MovieDatasetBehavior(TaskSet):

    def on_start(self):
        self.login()
        self.last_dataset_id = None
        self.version_ids = []

    def login(self):
        """Simula login con token CSRF"""
        response = self.client.get("/login")
        if response.status_code != 200:
            print(f"Login page failed: {response.status_code}")
            return

        csrf_token = get_csrf_token(response)

        response = self.client.post(
            "/login",
            data={
                "email": "user1@example.com",
                "password": "1234",
                "csrf_token": csrf_token
            },
            allow_redirects=True
        )

        if response.status_code != 200:
            print(f"Login failed: {response.status_code}")

    # --------------------------------------------------
    # DATASETS
    # --------------------------------------------------

    @task(3)
    def list_all_datasets(self):
        """GET /moviedataset/list"""
        response = self.client.get("/moviedataset/list")

        if response.status_code != 200:
            print(f"List datasets failed: {response.status_code}")
            return

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            for link in links:
                href = link["href"]
                # Queremos solo: /moviedataset/<id>
                if href.startswith("/moviedataset/") and href.count("/") == 2:
                    self.last_dataset_id = href.rstrip("/").split("/")[-1]
                    break

        except Exception:
            self.last_dataset_id = None

    @task(2)
    def list_my_datasets(self):
        """GET /moviedataset/my-datasets"""
        response = self.client.get("/moviedataset/my-datasets")
        if response.status_code != 200:
            print(f"My datasets failed: {response.status_code}")

    @task(1)
    def view_dataset_detail(self):
        """GET /moviedataset/<id>"""
        if not self.last_dataset_id:
            return

        response = self.client.get(
            f"/moviedataset/{self.last_dataset_id}"
        )

        if response.status_code != 200:
            print(f"View dataset failed: {response.status_code}")

    @task(1)
    def download_dataset(self):
        """GET /moviedataset/<id>/download"""
        if not self.last_dataset_id:
            self.list_all_datasets()
            if not self.last_dataset_id:
                return

        response = self.client.get(
            f"/moviedataset/{self.last_dataset_id}/download"
        )

        if response.status_code != 200:
            print(f"Download dataset failed: {response.status_code}")

    # --------------------------------------------------
    # VERSIONES
    # --------------------------------------------------

    @task(1)
    def view_dataset_versions(self):
        """GET /moviedataset/<id>/versions"""
        if not self.last_dataset_id:
            return

        response = self.client.get(
            f"/moviedataset/{self.last_dataset_id}/versions"
        )

        if response.status_code != 200:
            print(f"View versions failed: {response.status_code}")
            return

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            version_ids = set()

            for link in links:
                href = link["href"]
                # Ejemplo real:
                # /moviedataset/version/160/compare/162/view
                if "/moviedataset/version/" in href and "/compare/" in href:
                    try:
                        parts = href.split("/")
                        v1 = int(parts[3])
                        v2 = int(parts[5])
                        version_ids.add(v1)
                        version_ids.add(v2)
                    except (IndexError, ValueError):
                        pass

            self.version_ids = list(version_ids)

        except Exception:
            self.version_ids = []


    # --------------------------------------------------
    # COMPARACIÓN DE VERSIONES (ISSUE CORE)
    # --------------------------------------------------

    @task(2)
    def compare_versions_json(self):
        if len(self.version_ids) < 2:
            return

        v1, v2 = random.sample(self.version_ids, 2)

        response = self.client.get(
            f"/moviedataset/version/{v1}/compare/{v2}"
        )

        if response.status_code != 200:
            print(f"Compare versions JSON failed: {response.status_code}")


    @task(1)
    def compare_versions_view(self):
        """GET /moviedataset/version/<v1>/compare/<v2>/view"""
        if len(self.version_ids) < 2:
            return

        v1, v2 = random.sample(self.version_ids, 2)

        response = self.client.get(
            f"/moviedataset/version/{v1}/compare/{v2}/view"
        )

        if response.status_code != 200:
            print(f"Compare versions VIEW failed: {response.status_code}")


class MovieDatasetUser(HttpUser):
    tasks = [MovieDatasetBehavior]
    wait_time = between(2, 5)
    host = get_host_for_locust_testing()
