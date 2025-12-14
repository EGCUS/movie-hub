from io import BytesIO
import json
from locust import HttpUser, TaskSet, task, between
from core.environment.host import get_host_for_locust_testing
from core.locust.common import fake, get_csrf_token
from bs4 import BeautifulSoup
import random


def get_csrf_token(response):
    """Extrae el token CSRF de la respuesta HTML"""
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_input = soup.find("input", {"name": "csrf_token"})
    return csrf_input["value"] if csrf_input else None


class MovieDatasetBehavior(TaskSet):

    def on_start(self):
        self.login()
        self.last_dataset_id = None
        self.version_ids = []
        self.my_uploaded_datasets = []  # Guardar IDs de datasets que YO subí
        self.my_draft_datasets = []  # Solo los drafts que puedo publicar

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
    # HELPER: Generar JSON de películas
    # --------------------------------------------------
    
    def _generate_movie_json(self, num_movies=5):
        """Genera JSON de películas de prueba"""
        movies = []
        for i in range(num_movies):
            movies.append({
                "title": f"Test Movie {i}",
                "original_title": f"Test Movie Original {i}",
                "year": random.randint(2000, 2024),
                "duration": random.randint(80, 180),
                "country": "USA",
                "director": f"Director {i}",
                "production_company": "Test Productions",
                "genre": random.choice(["Action", "Drama", "Comedy", "Sci-Fi"]),
                "synopsis": f"Synopsis for test movie {i}",
                "imdb_rating": round(random.uniform(5.0, 9.5), 1),
                "imdb_votes": random.randint(1000, 100000),
                "poster_url": f"http://example.com/poster{i}.jpg",
                "screenplay": f"Writer {i}",
                "cast": f"Actor {i}, Actress {i}",
                "awards": f"{random.randint(0, 5)} awards"
            })
        return {"movies": movies}

    # --------------------------------------------------
    # UPLOAD & PUBLISH
    # --------------------------------------------------

    @task(3)
    def upload_dataset_as_draft(self):
        """POST /moviedataset/upload con action=draft"""
        response = self.client.get("/moviedataset/upload")
        if response.status_code != 200:
            print(f"Upload page failed: {response.status_code}")
            return
        
        csrf_token = get_csrf_token(response)
        if not csrf_token:
            print("CSRF token not found")
            return
        
        movie_data = self._generate_movie_json(num_movies=5)
        
        files = {
            'file': ('test_movies.json', 
                    BytesIO(json.dumps(movie_data).encode('utf-8')), 
                    'application/json')
        }
        
        data = {
            'title': f'Test Dataset {random.randint(1000, 9999)}',
            'desc': 'Dataset de prueba para Locust',
            'publication_type': 'none',
            'tags': 'test,locust,movies',
            'authors-0-name': 'Test Author',
            'authors-0-affiliation': 'Test University',
            'authors-0-orcid': '',
            'action': 'draft',
            'csrf_token': csrf_token
        }
        
        response = self.client.post(
            "/moviedataset/upload",
            data=data,
            files=files,
            name="/moviedataset/upload [DRAFT]"
        )
        
        if response.status_code in [200, 302]:
            if 'dataset_id=' in response.url:
                self.last_dataset_id = response.url.split('dataset_id=')[1].split('&')[0]
                self.my_uploaded_datasets.append(self.last_dataset_id)
                self.my_draft_datasets.append(self.last_dataset_id)  # Es un draft
                print(f"✓ Draft uploaded - Dataset ID: {self.last_dataset_id}")
            else:
                print(f"✗ Upload success but no dataset_id in URL: {response.url}")
        else:
            print(f"Upload draft failed: {response.status_code}")

    @task(5)
    def upload_and_publish_directly(self):
        """POST /moviedataset/upload con action=publish"""
        response = self.client.get("/moviedataset/upload")
        if response.status_code != 200:
            print(f"Upload page failed: {response.status_code}")
            return
        
        csrf_token = get_csrf_token(response)
        if not csrf_token:
            print("CSRF token not found")
            return
        
        movie_data = self._generate_movie_json(num_movies=3)
        
        files = {
            'file': ('quick_publish.json', 
                    BytesIO(json.dumps(movie_data).encode('utf-8')), 
                    'application/json')
        }
        
        data = {
            'title': f'Quick Publish {random.randint(1000, 9999)}',
            'desc': 'Dataset publicado directamente',
            'publication_type': 'none',
            'tags': 'test,quick',
            'authors-0-name': 'Quick Author',
            'action': 'publish',
            'csrf_token': csrf_token
        }
        
        response = self.client.post(
            "/moviedataset/upload",
            data=data,
            files=files,
            name="/moviedataset/upload [PUBLISH]"
        )
        
        if response.status_code in [200, 302]:
            if 'dataset_id=' in response.url:
                self.last_dataset_id = response.url.split('dataset_id=')[1].split('&')[0]
                self.my_uploaded_datasets.append(self.last_dataset_id)  # Guardar mi dataset
                print(f"✓ Published directly - Dataset ID: {self.last_dataset_id}")
            else:
                print(f"✗ Publish success but no dataset_id in URL: {response.url}")
        else:
            print(f"Upload and publish failed: {response.status_code}")

    @task(2)
    def publish_existing_draft(self):
        """POST /moviedataset/<id>/publish"""
        # Solo intentar publicar si tengo drafts disponibles
        if not self.my_draft_datasets:
            return
        
        # Elegir un draft aleatorio de mis drafts
        dataset_id = random.choice(self.my_draft_datasets)
        
        # Verificar que sea un ID válido (número)
        if not str(dataset_id).isdigit():
            return
        
        # Es una API JSON, no necesita CSRF
        response = self.client.post(
            f"/moviedataset/{dataset_id}/publish",
            headers={"Content-Type": "application/json"},
            name="/moviedataset/<id>/publish"
        )
        
        if response.status_code == 200:
            print(f"✓ Draft {dataset_id} published successfully")
            # Remover de la lista de drafts porque ya está publicado
            self.my_draft_datasets.remove(dataset_id)
        elif response.status_code == 400:
            # Ya está publicado o error de validación
            # Remover de la lista de drafts
            if dataset_id in self.my_draft_datasets:
                self.my_draft_datasets.remove(dataset_id)
        else:
            print(f"Publish draft failed: {response.status_code} - Dataset ID: {dataset_id}")

    @task(1)
    def upload_multiple_files(self):
        """POST /moviedataset/upload con múltiples archivos"""
        response = self.client.get("/moviedataset/upload")
        if response.status_code != 200:
            return
        
        csrf_token = get_csrf_token(response)
        if not csrf_token:
            return
        
        files = []
        for i in range(3):
            movie_data = {
                "movies": [
                    {
                        "title": f"Bulk Movie {j}",
                        "year": 2020 + j,
                        "duration": 90 + (j * 10),
                        "director": f"Director {j}",
                        "country": "Spain",
                        "genre": "Drama"
                    }
                    for j in range(i + 1, i + 4)
                ]
            }
            
            files.append((
                'file',
                (f'bulk_movies_{i}.json',
                 BytesIO(json.dumps(movie_data).encode('utf-8')),
                 'application/json')
            ))
        
        data = {
            'title': f'Bulk Dataset {random.randint(1000, 9999)}',
            'desc': 'Dataset con múltiples archivos',
            'publication_type': 'none',
            'tags': 'test,bulk',
            'authors-0-name': 'Bulk Author',
            'action': 'draft',
            'csrf_token': csrf_token
        }
        
        response = self.client.post(
            "/moviedataset/upload",
            data=data,
            files=files,
            name="/moviedataset/upload [BULK]"
        )
        
        if response.status_code not in [200, 302]:
            print(f"Bulk upload failed: {response.status_code}")

    @task(1)
    def upload_large_dataset(self):
        """POST /moviedataset/upload con dataset grande (50 películas)"""
        response = self.client.get("/moviedataset/upload")
        if response.status_code != 200:
            return
        
        csrf_token = get_csrf_token(response)
        if not csrf_token:
            return
        
        movie_data = {
            "movies": [
                {
                    "title": f"Large Movie {i}",
                    "original_title": f"Original {i}",
                    "year": random.randint(1990, 2024),
                    "duration": random.randint(80, 180),
                    "country": random.choice(["USA", "UK", "Spain", "France"]),
                    "director": f"Director {i}",
                    "production_company": "Big Productions",
                    "genre": random.choice(["Action", "Drama", "Comedy", "Thriller"]),
                    "synopsis": f"Long synopsis for movie {i} " * 10,
                    "imdb_rating": round(random.uniform(5.0, 9.5), 1),
                    "imdb_votes": random.randint(1000, 500000),
                    "screenplay": f"Writer {i}",
                    "cast": ", ".join([f"Actor {j}" for j in range(5)])
                }
                for i in range(50)
            ]
        }
        
        files = {
            'file': ('large_dataset.json',
                    BytesIO(json.dumps(movie_data).encode('utf-8')),
                    'application/json')
        }
        
        data = {
            'title': f'Large Dataset {random.randint(1000, 9999)}',
            'desc': 'Dataset grande para stress test',
            'publication_type': 'none',
            'tags': 'test,stress,large',
            'authors-0-name': 'Stress Tester',
            'action': 'draft',
            'csrf_token': csrf_token
        }
        
        response = self.client.post(
            "/moviedataset/upload",
            data=data,
            files=files,
            name="/moviedataset/upload [LARGE]",
            timeout=60
        )
        
        if response.status_code not in [200, 302]:
            print(f"Large upload failed: {response.status_code}")

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
