from core.seeders.BaseSeeder import BaseSeeder
from app.modules.auth.models import User
from app.modules.fakenodo.models import Fakenodo
from datetime import datetime

class FakenodoSeeder(BaseSeeder):
    priority = 4 # se ejecuta despues de AuthSeeder, DataSeeder y MovieSeeder
    
    def run(self):
        
        user1 = User.query.filter_by(email="user1@example.com").first()
        user2 = User.query.filter_by(email="user2@example.com").first()
        
        data = [

            Fakenodo(
                movie_metadata={
                    "id": 1,
                    "title": "The Fake Awakens",
                    "original_title": "The Fake Awakens",
                    "year": 2024,
                    "duration": 128,
                    "country": "USA",
                    "director": "Jane Doe",
                    "screenplay": {"writer": "John Scriptman"},
                    "cast": ["Actor One", "Actress Two", "Sidekick Three"],
                    "production_company": "Fake Studios",
                    "genre": "action, sci-Fi",
                    "synopsis": "En un futuro lleno de APIs falsas, una desarrolladora lucha para mantener vivo el código.",
                    "awards": ["Best Fake Plot 2024"],
                    "imdb_rating": 7.8,
                    "imdb_votes": 15342,
                    "poster_url": "https://example.com/fakeawakens.jpg",
                    "poster_local_path": "/static/posters/fakeawakens.jpg",
                    "created_at": datetime.utcnow().isoformat(),
                    "user_id": user1.id,
                    "dataset_type": "movie"
                },
                status="draft",
                doi="fakenodo.doi.1"
            ),

            Fakenodo(
                movie_metadata={
                    "id": 2,
                    "title": "API Reloaded",
                    "original_title": "API Reloaded",
                    "year": 2023,
                    "duration": 115,
                    "country": "Spain",
                    "director": "Carlos Postman",
                    "screenplay": {"writer": "Laura Bytes"},
                    "cast": ["Actor Byte", "Actress JSON", "Villain SQL"],
                    "production_company": "DataFrame Pictures",
                    "genre": "thriller, techno",
                    "synopsis": "Una hacker intenta derribar un servidor donde las APIs cobran vida propia.",
                    "awards": [],
                    "imdb_rating": 6.9,
                    "imdb_votes": 9102,
                    "poster_url": "https://example.com/apireloaded.jpg",
                    "poster_local_path": "/static/posters/apireloaded.jpg",
                    "created_at": datetime.utcnow().isoformat(),
                    "user_id": user2.id,
                    "dataset_type": "movie"
                },
                status="published",
                doi="fakenodo.doi.2"
            ),

            Fakenodo(
                movie_metadata={
                    "id": 3,
                    "title": "Commit of the Dead",
                    "original_title": "Commit of the Dead",
                    "year": 2022,
                    "duration": 101,
                    "country": "UK",
                    "director": "George Merge",
                    "screenplay": {"writer": "Alice Branch"},
                    "cast": ["Coder One", "Zombie Pull Request", "Git Reaper"],
                    "production_company": "Master Repo Films",
                    "genre": "horror, comedy",
                    "synopsis": "Un commit maldito libera un ejército de zombies que comen cerebros… y repositorios.",
                    "awards": ["Best Bug Fix 2023"],
                    "imdb_rating": 7.2,
                    "imdb_votes": 5530,
                    "poster_url": "https://example.com/commitdead.jpg",
                    "poster_local_path": "/static/posters/commitdead.jpg",
                    "created_at": datetime.utcnow().isoformat(),
                    "user_id": user2.id,
                    "dataset_type": "movie"
                },
                status="draft",
                doi="fakenodo.doi.3"
            ),

        ]

        self.seed(data)
