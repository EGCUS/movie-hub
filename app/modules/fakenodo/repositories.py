from app.modules.fakenodo.models import Fakenodo
from core.repositories.BaseRepository import BaseRepository


class FakenodoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Fakenodo)
        
    def create_new_movie(self, movie_metadata, doi):
        return self.create(movie_metadata=movie_metadata, doi=doi)
