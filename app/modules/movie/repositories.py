from app.modules.movie.models import Movie
from core.repositories.BaseRepository import BaseRepository


class MovieRepository(BaseRepository):
    def __init__(self):
        super().__init__(Movie)
