from flask import render_template
from app.modules.movie import movie_bp


@movie_bp.route('/movie', methods=['GET'])
def index():
    return render_template('movie/index.html')
