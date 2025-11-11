from core.blueprints.base_blueprint import BaseBlueprint

movie_bp = BaseBlueprint('movie', __name__, template_folder='templates')

from app.modules.movie.models import MovieDataset
