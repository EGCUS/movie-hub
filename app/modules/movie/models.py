from app import db
from app.modules.dataset.base_dataset import BaseDataset


class MovieDataset(BaseDataset):
    __tablename__ = "movie_dataset"
    
    # Este ID es foreign key a base_dataset
    id = db.Column(db.Integer, db.ForeignKey('base_dataset.id'), primary_key=True)
    
    
    movie_title = db.Column(db.String(255))
    original_title = db.Column(db.String(255))
    year = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer) 
    country = db.Column(db.String(255))
    director = db.Column(db.String(500))
    production_company = db.Column(db.String(500))
    genre = db.Column(db.String(255))
    synopsis = db.Column(db.Text)
    
    # IMDB
    imdb_rating = db.Column(db.Float)
    imdb_votes = db.Column(db.Integer)
    
    poster_url = db.Column(db.String(500))
    poster_local_path = db.Column(db.String(500))
    
    # JSON
    screenplay = db.Column(db.JSON)  
    cast = db.Column(db.JSON)
    awards = db.Column(db.JSON)
    
    __mapper_args__ = {
        "polymorphic_identity": "movie",
    }
    
    def to_dict(self):
        """Convierte el modelo a diccionario para JSON/APIs"""
        return {
            "id": self.id,
            "title": self.ds_meta_data.title if self.ds_meta_data else None,
            "description": self.ds_meta_data.description if self.ds_meta_data else None,
            "tags": self.ds_meta_data.tags if self.ds_meta_data else None,
            "authors": [a.to_dict() for a in self.ds_meta_data.authors
            ] if self.ds_meta_data and self.ds_meta_data.authors else [],
            "movie_title": self.movie_title,
            "original_title": self.original_title,
            "year": self.year,
            "duration": self.duration,
            "country": self.country,
            "director": self.director,
            "screenplay": self.screenplay,
            "cast": self.cast,
            "production_company": self.production_company,
            "genre": self.genre,
            "synopsis": self.synopsis,
            "awards": self.awards,
            "imdb_rating": self.imdb_rating,
            "imdb_votes": self.imdb_votes,
            "poster_url": self.poster_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id,
            "dataset_type": self.dataset_type,
        }