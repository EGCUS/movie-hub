import hashlib
import os
from flask import abort
from app import db
from app.modules.dataset.models import Author, DSMetaData
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from app.modules.movie.models import MovieDataset, Movie
import json
from types import SimpleNamespace
from app.modules.dataset.base_dataset import Version
from datetime import datetime
from core.services.BaseService import BaseService
from app.modules.movie.repositories import MovieRepository
from app.modules.dataset.repositories import DSDownloadRecordRepository, DSViewRecordRepository
from app.modules.fakenodo.adapter import FakenodoAdapter


class SnapshotDataset:
    """Dataset reconstruido desde snapshot sin usar SQLAlchemy."""
    def __init__(self, id, movies, metadata):
        self.id = id
        self.movies = movies
        self.ds_meta_data = metadata

class SnapshotMovie:
    """Pelí­cula reconstruida desde snapshot."""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)

class MovieService(BaseService):
    def __init__(self):
        super().__init__(MovieRepository())
        self.dsdownloadrecord_repository = DSDownloadRecordRepository()
        self.dsviewrecord_repostory = DSViewRecordRepository()
        self.fakenodo_adapter = FakenodoAdapter()
    
    def total_dataset_downloads(self) -> int:
        return self.dsdownloadrecord_repository.total_dataset_downloads()

    def total_dataset_views(self) -> int:
        return self.dsviewrecord_repostory.total_dataset_views()
    
    def get_moviedataset(self, dataset_id):
        dataset = MovieDataset.query.get(dataset_id)
        if not dataset:
            abort(404, "Movie dataset not found")
        return dataset
    
    def get_all_moviedatasets(self):
        from app.modules.dataset.models import DSMetaData
        
        return MovieDataset.query.join(DSMetaData).filter(
            DSMetaData.dataset_doi.isnot(None)
        ).order_by(MovieDataset.created_at.desc()).all()
    
    #Se muestra lo publicado 
    def get_moviedataset_by_user(self, user_id):
        from app.modules.dataset.models import DSMetaData
        
        return MovieDataset.query.join(DSMetaData).filter(
            MovieDataset.user_id == user_id,
            DSMetaData.dataset_doi.isnot(None)
        ).order_by(MovieDataset.created_at.desc()).all()
    
    #Ahora mismo no se usa, sirve para mostrar los no publicados
    def get_unsynchronized_datasets_by_user(self, user_id):
        from app.modules.dataset.models import DSMetaData
        
        return MovieDataset.query.join(DSMetaData).filter(
            MovieDataset.user_id == user_id,
            DSMetaData.dataset_doi.is_(None)
        ).order_by(MovieDataset.created_at.desc()).all()
    
    def get_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404, "Movie not found")
        return movie
    
    
    def upload_and_publish_dataset(self, form, current_user, dsmetadata_service):
        """
        Crea y sube un dataset completo con todos sus archivos y películas.
        Retorna el dataset creado y el total de películas procesadas.
        """
        metadata = DSMetaData(
            title=form.title.data,
            description=form.desc.data,
            publication_type=form.convert_publication_type(form.publication_type.data),
            publication_doi=form.publication_doi.data or None,
            tags=form.tags.data or None
        )
        db.session.add(metadata)
        db.session.flush()
        
        for author_data in form.get_authors():
            if author_data['name']:
                author = Author(
                    name=author_data['name'],
                    affiliation=author_data.get('affiliation'),
                    orcid=author_data.get('orcid'),
                    ds_meta_data_id=metadata.id
                )
                db.session.add(author)
        
        movie_dataset = MovieDataset(
            user_id=current_user.id,
            ds_meta_data_id=metadata.id
        )
        db.session.add(movie_dataset)
        db.session.flush()
        
        if not movie_dataset.id:
            raise Exception("Failed to create MovieDataset - ID is NULL")
        
        db.session.commit()
        
        # Fakenodo
        fakenodo_response = self.fakenodo_adapter.create_fakenodo(movie_dataset)
        fakenodo_id = fakenodo_response.get("id")
        deposition_id = fakenodo_response.get("deposition_id")
        dsmetadata_service.update(metadata.id, deposition_id=deposition_id)
        db.session.commit()
        
        # carpeta local
        dataset_folder = f"uploads/user_{current_user.id}/dataset_{movie_dataset.id}"
        os.makedirs(dataset_folder, exist_ok=True)
        
        # Procesar archivos
        files = form.file.data
        if not files or len(files) == 0:
            raise ValueError("No files uploaded")
        
        total_movies = 0
        for file in files:
            if not file or file.filename == '':
                continue
            
            file_content = file.read()
            
            # Validar JSON
            try:
                movie_data = json.loads(file_content)
                if isinstance(movie_data, list):
                    movie_data = {"movies": movie_data}
                elif isinstance(movie_data, dict) and 'movies' not in movie_data:
                    raise ValueError("JSON object must contain a 'movies' key with an array")
                elif not isinstance(movie_data, dict):
                    raise ValueError("JSON must be an array or an object with 'movies' key")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {file.filename}: {str(e)}")
            
            # Guardar localmente
            local_file_path = os.path.join(dataset_folder, file.filename)
            with open(local_file_path, 'wb') as f:
                f.write(file_content)
            
            # Subir a Fakenodo
            self.fakenodo_adapter.upload_file_to_fakenodo(
                fakenodo_id=fakenodo_id,
                file_content=file_content,
                filename=file.filename,
                dataset_id=movie_dataset.id
            )
            
            fm_meta = FMMetaData(
                filename=file.filename,
                title=f"{metadata.title} - {file.filename}",
                description="Movie dataset JSON",
                publication_type=metadata.publication_type,
                tags="movies,json",
                version="1.0"
            )
            db.session.add(fm_meta)
            db.session.flush()
            
            feature_model = FeatureModel(
                data_set_id=movie_dataset.id,
                fm_meta_data_id=fm_meta.id
            )
            db.session.add(feature_model)
            db.session.flush()
            
            file_hash = hashlib.md5(file_content).hexdigest()
            hubfile = Hubfile(
                name=file.filename,
                checksum=file_hash,
                size=len(file_content),
                feature_model_id=feature_model.id
            )
            db.session.add(hubfile)
            
            for movie_dict in movie_data.get('movies', []):
                movie = Movie(
                    movie_dataset_id=movie_dataset.id,
                    title=movie_dict.get('title'),
                    original_title=movie_dict.get('original_title'),
                    year=movie_dict.get('year'),
                    duration=movie_dict.get('duration'),
                    country=movie_dict.get('country'),
                    director=movie_dict.get('director'),
                    production_company=movie_dict.get('production_company'),
                    genre=movie_dict.get('genre'),
                    synopsis=movie_dict.get('synopsis'),
                    imdb_rating=movie_dict.get('imdb_rating'),
                    imdb_votes=movie_dict.get('imdb_votes'),
                    poster_url=movie_dict.get('poster_url'),
                    screenplay=movie_dict.get('screenplay'),
                    cast=movie_dict.get('cast'),
                    awards=movie_dict.get('awards')
                )
                db.session.add(movie)
            
            movies_count = len(movie_data.get('movies', []))
            total_movies += movies_count
        
        # Finalizar
        movie_dataset.update_files_info()
        db.session.commit()
        
        # Crear versión inicial
        self.create_version(movie_dataset)
        
        # Publicar
        dataset_doi = f"10.1234/{metadata.title.lower().replace(' ', '')}"
        dsmetadata_service.update(metadata.id, dataset_doi=dataset_doi)
        self.fakenodo_adapter.publish_fakenodo(fakenodo_id)
        
        return movie_dataset, total_movies
    
    
    #POR HACER
    def create_dataset(self, form, current_user):
        """
        TODO
        añadir self.create_version(dataset) al final para poder crear las versiones
        """
        raise NotImplementedError("Dataset creation not yet implemented")
    
    #Método delete??

###################
# VERSIONING METHODS
###################


    def create_version(self, dataset: MovieDataset):
        """Crea una nueva versión del dataset guardando un snapshot JSON."""

        version_number = str(len(dataset.versions) + 1.0)

        version = Version(
            dataset_id=dataset.id,
            version_number=version_number,
            created_at=datetime.utcnow()
        )
        
        dataset.current_version = version_number

        db.session.add(version)
        db.session.flush()

        version_folder = f"uploads/user_{dataset.user_id}/dataset_{dataset.id}/versions/{version.id}"
        os.makedirs(version_folder, exist_ok=True)

        snapshot = {
            "dataset_id": dataset.id,      
            "metadata": {
                "title": dataset.ds_meta_data.title,
                "description": dataset.ds_meta_data.description,
                "publication_type": dataset.ds_meta_data.publication_type.name if dataset.ds_meta_data.publication_type else None,
                "publication_doi": dataset.ds_meta_data.publication_doi,
                "dataset_doi": dataset.ds_meta_data.dataset_doi,
                "tags": dataset.ds_meta_data.tags.split(",") if dataset.ds_meta_data.tags else []
            },
            "movies": [m.to_dict() for m in dataset.movies]
        }

        snapshot_path = os.path.join(version_folder, "snapshot.json")
        with open(snapshot_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=4)

        version.snapshot_path = snapshot_path

        db.session.commit()
        return version


    def load_dataset_from_version(self, version_id):
        """Carga un dataset reconstruido desde el snapshot de una versión."""

        version = Version.query.get(version_id)
        if not version or not version.snapshot_path:
            raise ValueError("Snapshot not found for that version")

        with open(version.snapshot_path, "r", encoding="utf-8") as f:
            snap = json.load(f)

        metadata = SimpleNamespace(
            title=snap["metadata"].get("title"),
            description=snap["metadata"].get("description"),
            authors=snap["metadata"].get("authors", []),
            publication_type=snap["metadata"].get("publication_type"),
            publication_doi=snap["metadata"].get("publication_doi"),
            dataset_doi=snap["metadata"].get("dataset_doi"),
            tags=snap["metadata"].get("tags", [])
        )

        movies = [SnapshotMovie(m) for m in snap["movies"]]

        return SnapshotDataset(
            id=snap["dataset_id"],   # <-- ya existe
            movies=movies,
            metadata=metadata
        )
    
    def compare_versions(self, v1_dataset, v2_dataset):
        """
        Compara dos datasets cargados desde snapshot.
        Ambos argumentos son SnapshotDataset.
        """

        result = {
            "movies_added": [],
            "movies_removed": [],
            "movies_modified": [],
            "metadata_changed": {},
        }

        # ============================
        # COMPARAR METADATA
        # ============================
        meta1 = vars(v1_dataset.ds_meta_data)
        meta2 = vars(v2_dataset.ds_meta_data)

        for key in meta1.keys() | meta2.keys():
            if meta1.get(key) != meta2.get(key):
                result["metadata_changed"][key] = {
                    "old": meta1.get(key),
                    "new": meta2.get(key),
                }

        # ============================
        # COMPARAR MOVIES
        # ============================

        # Convert to dict by ID
        movies_v1 = {m.id: m for m in v1_dataset.movies}
        movies_v2 = {m.id: m for m in v2_dataset.movies}

        # Añadidos
        for movie_id, m in movies_v2.items():
            if movie_id not in movies_v1:
                result["movies_added"].append(vars(m))

        # Eliminados
        for movie_id, m in movies_v1.items():
            if movie_id not in movies_v2:
                result["movies_removed"].append(vars(m))

        # Modificados
        for movie_id in movies_v1.keys() & movies_v2.keys():
            m1 = vars(movies_v1[movie_id])
            m2 = vars(movies_v2[movie_id])

            diffs = {}
            for key in m1.keys() | m2.keys():
                if m1.get(key) != m2.get(key):
                    diffs[key] = {"old": m1.get(key), "new": m2.get(key)}

            if diffs:
                result["movies_modified"].append({
                    "movie_id": movie_id,
                    "changes": diffs
                })

        return result


    def compare_version_ids(self, version_id_1, version_id_2):
        v1 = self.load_dataset_from_version(version_id_1)
        v2 = self.load_dataset_from_version(version_id_2)

        return self.compare_versions(v1, v2)
    