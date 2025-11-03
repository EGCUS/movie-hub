from app.modules.movie.repositories import MovieRepository
from core.services.BaseService import BaseService


class MovieService(BaseService):
    def __init__(self):
        super().__init__(MovieRepository())
