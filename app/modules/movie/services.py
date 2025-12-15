import hashlib
import os
import json
import difflib
from flask import abort

from app import db
from app.modules.dataset.models import Author, DSMetaData
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from app.modules.movie.models import DatasetChangeLog, MovieDataset, Movie
from app.modules.dataset.base_dataset import Version
from datetime import datetime
from core.services.BaseService import BaseService
from app.modules.movie.repositories import MovieRepository
from app.modules.dataset.repositories import DSDownloadRecordRepository, DSViewRecordRepository
from app.modules.fakenodo.adapter import FakenodoAdapter
from app.modules.fakenodo.models import Fakenodo


class SnapshotDataset:
    """Dataset reconstruido desde snapshot sin usar SQLAlchemy."""
    def __init__(self, id, movies, metadata, files, version_id):
        self.id = id
        self.movies = movies
        self.ds_meta_data = metadata or {}
        self.files = files or []
        self.version_id = version_id


class SnapshotMovie:
    """Película reconstruida desde snapshot."""
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
        
    
    def get_published_datasets(self, limit=None):
        """Obtiene solo los datasets publicados en Fakenodo"""
        from app.modules.fakenodo.models import Fakenodo
        
        return MovieDataset.query.join(Fakenodo).filter(
            Fakenodo.status == "published"
        ).order_by(MovieDataset.created_at.desc())
            
        
    #MUESTRO LO PUBLICADO EN FAKENODO
    def get_moviedataset_by_user(self, user_id):
        """Obtiene datasets publicados en Fakenodo del usuario"""
        from app.modules.fakenodo.models import Fakenodo
        
        # Datasets que tienen un Fakenodo con status "published"
        return MovieDataset.query.join(Fakenodo).filter(
            MovieDataset.user_id == user_id,
            Fakenodo.status == "published"
        ).order_by(MovieDataset.created_at.desc()).all()
        
        
    def get_unsynchronized_datasets_by_user(self, user_id):
        """Obtiene datasets NO publicados (drafts) del usuario"""
        
        # Datasets que tienen un Fakenodo pero NO está published
        return MovieDataset.query.join(Fakenodo).filter(
            MovieDataset.user_id == user_id,
            Fakenodo.status != "published"
        ).order_by(MovieDataset.created_at.desc()).all()
        
        
    def get_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404, "Movie not found")
        return movie
    
    
    
    def upload_and_publish_dataset(self, form, current_user, dsmetadata_service):
        """
        Crea y sube un dataset completo con todos sus archivos y películas,
        y luego lo publica en Fakenodo.
        Retorna el dataset creado y el total de películas procesadas.
        """
        movie_dataset, total_movies, fakenodo_id = self.upload_draft_dataset(form, current_user, dsmetadata_service)

        self.fakenodo_adapter.publish_fakenodo(fakenodo_id)

        return movie_dataset, total_movies
    
    
    def upload_draft_dataset(self, form, current_user, dsmetadata_service):
    
        try:
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
            
            # Fakenodo
            fakenodo_response = self.fakenodo_adapter.create_fakenodo(movie_dataset)
            fakenodo_id = fakenodo_response.get("id")
            deposition_id = fakenodo_response.get("deposition_id")
            dsmetadata_service.update(metadata.id, deposition_id=deposition_id)
            
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
            
            # Crear versión inicial
            self.create_version(movie_dataset)
            
            dataset_doi = f"10.1234/{metadata.title.lower().replace(' ', '')}{metadata.id}"
            dsmetadata_service.update(metadata.id, dataset_doi=dataset_doi)
            
            db.session.commit()
            
            return movie_dataset, total_movies, fakenodo_id
            
        except Exception as e:
            db.session.rollback()
        
        try:
            dataset_folder = f"uploads/user_{current_user.id}/dataset_{movie_dataset.id if 'movie_dataset' in locals() else 'unknown'}"
            if os.path.exists(dataset_folder):
                import shutil
                shutil.rmtree(dataset_folder)
        except:
            pass
        
        raise e
    
    
    #POR HACER
    def create_dataset(self, form, current_user):
        raise NotImplementedError("Dataset creation not yet implemented")

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
            "movies": [m.to_dict() for m in dataset.movies],
            # ✅ files congelados por versión
            "files": [
                {
                    "name": f.name,
                    "checksum": f.checksum,
                    "size": f.size
                }
                for fm in dataset.feature_models
                for f in Hubfile.query.filter_by(feature_model_id=fm.id).all()
            ]
        }

        snapshot_path = os.path.join(version_folder, "snapshot.json")
        with open(snapshot_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=4)

        version.snapshot_path = snapshot_path

        db.session.commit()
        return version

    def load_dataset_from_version(self, version_id):
        version = Version.query.get(version_id)

        if not version:
            raise ValueError(f"Version {version_id} does not exist")
        if not version.snapshot_path:
            raise ValueError(f"Version {version_id} has no snapshot")
        if not os.path.exists(version.snapshot_path):
            raise ValueError(f"Snapshot file missing for version {version_id}")

        with open(version.snapshot_path, "r", encoding="utf-8") as f:
            snap = json.load(f)

        return SnapshotDataset(
            id=snap["dataset_id"],
            movies=[SnapshotMovie(m) for m in snap.get("movies", [])],
            metadata=snap.get("metadata", {}),
            files=snap.get("files", []),
            version_id=version.id
        )

    ###################
    # MAIN COMPARE
    ###################

    def compare_versions(self, v1_dataset, v2_dataset):
        result = {
            "files": {},
            "metadata_changed": {},
            "movies_added": [],
            "movies_removed": [],
            "movies_modified": [],
        }

        # METADATA
        m1 = v1_dataset.ds_meta_data or {}
        m2 = v2_dataset.ds_meta_data or {}

        for key in m1.keys() | m2.keys():
            if m1.get(key) != m2.get(key):
                result["metadata_changed"][key] = {"old": m1.get(key), "new": m2.get(key)}

        # MOVIES (logical_id)
        def norm(v):
            if isinstance(v, list):
                return sorted(v)
            if isinstance(v, dict):
                return dict(sorted(v.items()))
            return v

        FIELDS = [
            "title", "original_title", "year", "duration", "country",
            "director", "production_company", "genre", "synopsis",
            "imdb_rating", "imdb_votes", "poster_url",
            "screenplay", "cast", "awards"
        ]

        v1 = {m.logical_id: m for m in v1_dataset.movies}
        v2 = {m.logical_id: m for m in v2_dataset.movies}

        for lid in (v2.keys() - v1.keys()):
            movie = v2[lid]
            result["movies_added"].append({
                "logical_id": lid,
                "title": movie.title
            })

        for lid in (v1.keys() - v2.keys()):
            movie = v1[lid]
            result["movies_removed"].append({
                "logical_id": lid,
                "title": movie.title
            })

        for lid in v1.keys() & v2.keys():
            diffs = {}
            for f in FIELDS:
                if norm(getattr(v1[lid], f, None)) != norm(getattr(v2[lid], f, None)):
                    diffs[f] = {
                        "old": getattr(v1[lid], f, None),
                        "new": getattr(v2[lid], f, None),
                    }
            if diffs:
                result["movies_modified"].append({
                    "logical_id": lid,
                    "title": v2[lid].title, 
                    "changes": diffs
                })

        # ✅ FILES (desde snapshot, NO BD)
        result["files"] = self.compare_files_between_versions(v1_dataset, v2_dataset)

        return result

    def compare_version_ids(self, v1_id, v2_id):
        return self.compare_versions(
            self.load_dataset_from_version(v1_id),
            self.load_dataset_from_version(v2_id)
        )

    ###################
    # FILE COMPARISON (snapshot-based)
    ###################

    def compare_files_between_versions(self, v1_dataset: SnapshotDataset, v2_dataset: SnapshotDataset):
        files_v1 = {f["name"]: f for f in (v1_dataset.files or [])}
        files_v2 = {f["name"]: f for f in (v2_dataset.files or [])}

        added = []
        removed = []
        modified = []

        for name, f in files_v2.items():
            if name not in files_v1:
                added.append(f)

        for name, f in files_v1.items():
            if name not in files_v2:
                removed.append(f)

        for name in files_v1.keys() & files_v2.keys():
            if files_v1[name].get("checksum") != files_v2[name].get("checksum"):
                modified.append({
                    "name": name,
                    "old": files_v1[name],
                    "new": files_v2[name],
                })

        return {
            "files_added": added,
            "files_removed": removed,
            "files_modified": modified,
        }

    ###################
    # TEXT DIFF (READY)
    ###################

    def diff_text_files(self, path1, path2):
        with open(path1, "r", encoding="utf-8") as f1, \
             open(path2, "r", encoding="utf-8") as f2:
            return list(difflib.unified_diff(
                f1.readlines(),
                f2.readlines(),
                fromfile="version_1",
                tofile="version_2"
            ))
