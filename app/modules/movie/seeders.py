from datetime import datetime, timezone
from app.modules.auth.models import User
from app.modules.movie.models import MovieDataset
from core.seeders.BaseSeeder import BaseSeeder


class MovieSeeder(BaseSeeder):
    priority = 3  # se ejecuta después del AuthSeeder y DataSetSeeder

    def run(self):
        user1 = User.query.filter_by(email="user1@example.com").first()
        user2 = User.query.filter_by(email="user2@example.com").first()

        if not user1 or not user2:
            raise Exception("Users not found. Please seed users first.")

        data = [
            MovieDataset(
                title="Inception",
                original_title="Inception",
                year=2010,
                duration=148,
                country="USA",
                director="Christopher Nolan",
                production_company="Syncopy / Warner Bros.",
                genre="scifi",
                synopsis="A skilled thief who steals secrets through dream-sharing technology is given a chance to erase his criminal record.",
                imdb_rating=8.8,
                imdb_votes=2300000,
                poster_url="https://m.media-amazon.com/images/I/51v5ZpFyaFL._AC_.jpg",
                cast=["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
                awards=["Oscar for Best Cinematography", "Oscar for Best Sound Editing"],
                screenplay={"writer": "Christopher Nolan"},
                user_id=user1.id,
                dataset_type="movie", 
                created_at=datetime.now(timezone.utc)
            ),
            MovieDataset(
                title="The Godfather",
                original_title="Il Padrino",
                year=1972,
                duration=175,
                country="USA",
                director="Francis Ford Coppola",
                production_company="Paramount Pictures",
                genre="drama",
                synopsis="The aging patriarch of an organized crime dynasty transfers control of his empire to his reluctant son.",
                imdb_rating=9.2,
                imdb_votes=1900000,
                poster_url="https://m.media-amazon.com/images/I/71xZCwTtH-L._AC_SY679_.jpg",
                cast=["Marlon Brando", "Al Pacino", "James Caan"],
                awards=["Oscar for Best Picture", "Oscar for Best Actor"],
                screenplay={"writer": "Mario Puzo & Francis Ford Coppola"},
                user_id=user2.id,
                dataset_type="movie",  
                created_at=datetime.now(timezone.utc)
            )
        ]

        self.seed(data)
