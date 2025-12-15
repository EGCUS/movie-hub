import os
import json
import shutil
import hashlib
from datetime import datetime, timezone
from dotenv import load_dotenv

from app import db
from app.modules.auth.models import User
from app.modules.movie.models import MovieDataset, Movie
from app.modules.dataset.models import DSMetaData, PublicationType, Author
from app.modules.fakenodo.models import Fakenodo
from app.modules.featuremodel.models import FeatureModel, FMMetaData
from app.modules.hubfile.models import Hubfile
from core.seeders.BaseSeeder import BaseSeeder
from app.modules.community.models import Community


from app.modules.movie.services import MovieService
movie_service = MovieService()


class MovieSeeder(BaseSeeder):
    priority = 3

    def run(self):

        if MovieDataset.query.join(MovieDataset.ds_meta_data).filter(DSMetaData.dataset_doi.isnot(None)).count() > 0:
            return

        # ==============================
        # PREPARACIÓN
        # ==============================
        user1 = User.query.filter_by(email="user1@example.com").first()
        user2 = User.query.filter_by(email="user2@example.com").first()

        if not user1 or not user2:
            raise Exception("Users not found. Please seed users first.")

        load_dotenv()
        working_dir = os.getenv("WORKING_DIR", "")
        src_folder = os.path.join(
            working_dir, "app", "modules", "movie", "json_examples"
        )

        ai = Community.query.filter_by(name="Grupo de Investigación en IA").first()
        ds = Community.query.filter_by(name="Comunidad de Ciencia de Datos").first()

        if not ai or not ds:
            raise Exception(
                "Communities not found. Seed CommunitySeeder before MovieSeeder."
            )
        # ==============================
        #  DATASET 1 — SCI-FI
        # ==============================

        def generate_logical_id(data: dict) -> str:
            base = f"{data.get('title')}|{data.get('year')}|{data.get('director')}"
            return hashlib.sha1(base.encode("utf-8")).hexdigest()

        # ==========================================================
        # DATASET 1 — SCI-FI (CON VERSIONADO COMPLETO)
        # ==========================================================
        scifi_meta = DSMetaData(
            title="Sci-Fi Masterpieces Collection",
            description="Essential science fiction films that pushed the boundaries of cinema",
            publication_type=PublicationType.OTHER,
            tags="movies, sci-fi, classics, space",
            dataset_doi="10.1234/scify-2024"
        )
        db.session.add(scifi_meta)
        db.session.flush()

        db.session.add(
            Author(
                name="Sci-Fi Film Institute",
                affiliation="Future Cinema Foundation",
                ds_meta_data_id=scifi_meta.id
            )
        )

        scifi_dataset = MovieDataset(
            ds_meta_data_id=scifi_meta.id,
            user_id=user1.id,
            dataset_type="movie",
            created_at=datetime.now(timezone.utc),
            community_id=ai.id
        )
        db.session.add(scifi_dataset)
        db.session.flush()

        # Películas Sci-Fi
        with open(os.path.join(src_folder, "movies1.json"), "r", encoding="utf-8") as f:
            scifi_movies_data = json.load(f)

        for data in scifi_movies_data:
            logical_id = data.get("logical_id") or generate_logical_id(data)
            db.session.add(
                Movie(
                    movie_dataset_id=scifi_dataset.id,
                    logical_id=logical_id,
                    **{k: v for k, v in data.items() if k != "logical_id"}
                )
            )

        db.session.commit()

        # Carpeta dataset
        scifi_folder = os.path.join(
            working_dir,
            "uploads",
            f"user_{scifi_dataset.user_id}",
            f"dataset_{scifi_dataset.id}"
        )
        os.makedirs(scifi_folder, exist_ok=True)

        # Archivo inicial
        src_file = os.path.join(src_folder, "movies1.json")
        dest_file = os.path.join(scifi_folder, "movies1.json")
        shutil.copy(src_file, dest_file)

        with open(dest_file, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        fm_meta = FMMetaData(
            filename="movies1.json",
            title="Sci-Fi Movies File",
            description="Initial Sci-Fi dataset file",
            publication_type=PublicationType.OTHER,
            tags="movies,json",
            version="1.0"
        )
        db.session.add(fm_meta)
        db.session.flush()

        feature_model = FeatureModel(
            data_set_id=scifi_dataset.id,
            fm_meta_data_id=fm_meta.id
        )
        db.session.add(feature_model)
        db.session.flush()

        db.session.add(
            Hubfile(
                name="movies1.json",
                checksum=file_hash,
                size=os.path.getsize(dest_file),
                feature_model_id=feature_model.id
            )
        )

        db.session.commit()

        # Crear registro en Fakenodo para que el dataset pertenezca y tenga estado
        # (por defecto lo marcamos como 'published' dado que le asignamos dataset_doi)
        scifi_fakenodo = Fakenodo(
            status="published",
            dataset_id=scifi_dataset.id,
            dataset_file_path=scifi_folder,
            doi=scifi_meta.dataset_doi
        )
        db.session.add(scifi_fakenodo)
        db.session.commit()

# ==============================
# VERSIONES SCI-FI
# ==============================

        # -------- V1 --------
        movie_service.create_version(scifi_dataset)

        # -------- V2 --------
        # 1️⃣ Modificar una película existente
        movie_to_modify = Movie.query.filter_by(
            movie_dataset_id=scifi_dataset.id
        ).first()

        movie_to_modify.director = "Ridley Scott (Edited)"
        movie_to_modify.synopsis = "Updated synopsis in version 2"

        # 2️⃣ Añadir una película nueva
        new_movie = Movie(
            movie_dataset_id=scifi_dataset.id,
            logical_id=generate_logical_id({
                "title": "Blade Runner 2049",
                "year": 2017,
                "director": "Denis Villeneuve"
            }),
            title="Blade Runner 2049",
            year=2017,
            director="Denis Villeneuve",
            genre="Sci-Fi",
            imdb_rating=8.0
        )
        db.session.add(new_movie)

        # 3️⃣ Modificar archivo movies1.json
        with open(dest_file, "r", encoding="utf-8") as f:
            content = json.load(f)

        content.append({
            "title": "Blade Runner 2049",
            "year": 2017,
            "director": "Denis Villeneuve"
        })

        with open(dest_file, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)

        hubfile = Hubfile.query.filter_by(name="movies1.json").first()
        hubfile.checksum = hashlib.md5(
            json.dumps(content, sort_keys=True).encode("utf-8")
        ).hexdigest()
        hubfile.size = os.path.getsize(dest_file)

        db.session.commit()
        movie_service.create_version(scifi_dataset)

        # -------- V3 --------
        # 4️⃣ Eliminar una película
        movie_to_delete = Movie.query.filter_by(
            movie_dataset_id=scifi_dataset.id,
            title="Blade Runner 2049"
        ).first()

        if movie_to_delete:
            db.session.delete(movie_to_delete)

        # 5️⃣ Añadir archivo nuevo
        extra_movies = [
            {"title": "Solaris", "year": 1972, "director": "Andrei Tarkovsky"}
        ]

        extra_file = os.path.join(scifi_folder, "extra_movies.json")
        with open(extra_file, "w", encoding="utf-8") as f:
            json.dump(extra_movies, f, indent=4)

        file_hash = hashlib.md5(
            json.dumps(extra_movies, sort_keys=True).encode("utf-8")
        ).hexdigest()

        fm_meta = FMMetaData(
            filename="extra_movies.json",
            title="Sci-Fi Extra Movies",
            description="Added in version 3",
            publication_type=PublicationType.OTHER,
            tags="movies,json",
            version="1.0"
        )
        db.session.add(fm_meta)
        db.session.flush()

        feature_model = FeatureModel(
            data_set_id=scifi_dataset.id,
            fm_meta_data_id=fm_meta.id
        )
        db.session.add(feature_model)
        db.session.flush()

        db.session.add(
            Hubfile(
                name="extra_movies.json",
                checksum=file_hash,
                size=os.path.getsize(extra_file),
                feature_model_id=feature_model.id
            )
        )

        db.session.commit()
        movie_service.create_version(scifi_dataset)

        # -------- V4 --------
        # 6️⃣ Eliminar archivo movies1.json
        if os.path.exists(dest_file):
            os.remove(dest_file)

        Hubfile.query.filter_by(name="movies1.json").delete()
        db.session.commit()

        movie_service.create_version(scifi_dataset)


        # ==========================================================
        # DATASET 2 — CLASSIC CINEMA (SIMPLE, SIN VERSIONADO LOCO)
        # ==========================================================
        classic_meta = DSMetaData(
            title="Classic Cinema Collection",
            description="Timeless classic movies from the golden age of cinema",
            publication_type=PublicationType.OTHER,
            tags="movies, classic, cinema",
            dataset_doi="10.1234/classic-cinema-2024"
        )
        db.session.add(classic_meta)
        db.session.flush()

        db.session.add(
            Author(
                name="Classic Film Archive",
                affiliation="International Film Preservation Society",
                ds_meta_data_id=classic_meta.id
            )
        )

        classic_dataset = MovieDataset(
            ds_meta_data_id=classic_meta.id,
            user_id=user2.id,
            dataset_type="movie",
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(classic_dataset)
        db.session.flush()

        with open(os.path.join(src_folder, "movies2.json"), "r", encoding="utf-8") as f:
            classic_movies = json.load(f)

        for data in classic_movies:
            logical_id = data.get("logical_id") or generate_logical_id(data)
            db.session.add(
                Movie(
                    movie_dataset_id=classic_dataset.id,
                    logical_id=logical_id,
                    **{k: v for k, v in data.items() if k != "logical_id"}
                )
            )

        db.session.commit()

        # Carpeta classic
        classic_folder = os.path.join(
            working_dir,
            "uploads",
            f"user_{classic_dataset.user_id}",
            f"dataset_{classic_dataset.id}"
        )
        os.makedirs(classic_folder, exist_ok=True)

        src_file = os.path.join(src_folder, "movies2.json")
        dest_file = os.path.join(classic_folder, "movies2.json")
        shutil.copy(src_file, dest_file)

        with open(dest_file, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        fm_meta = FMMetaData(
            filename="movies2.json",
            title="Classic Movies File",
            description="Classic cinema dataset file",
            publication_type=PublicationType.OTHER,
            tags="movies,json",
            version="1.0"
        )
        db.session.add(fm_meta)
        db.session.flush()

        feature_model = FeatureModel(
            data_set_id=classic_dataset.id,
            fm_meta_data_id=fm_meta.id
        )
        db.session.add(feature_model)
        db.session.flush()

        db.session.add(
            Hubfile(
                name="movies2.json",
                checksum=file_hash,
                size=os.path.getsize(dest_file),
                feature_model_id=feature_model.id
            )
        )

        db.session.commit()

        # Versión única (V1)
        # Crear registro en Fakenodo para el dataset clásico como DRAFT
        classic_fakenodo = Fakenodo(
            status="draft",
            dataset_id=classic_dataset.id,
            dataset_file_path=classic_folder,
            doi=classic_meta.dataset_doi
        )
        db.session.add(classic_fakenodo)
        db.session.commit()

        movie_service.create_version(classic_dataset)

        # ==========================================================
        # DATASET 3 — DOCUMENTARIES (PEQUEÑO, PARA TEST/SEEDS)
        # ==========================================================
        doc_meta = DSMetaData(
            title="Documentary Highlights",
            description="A small curated set of notable documentaries",
            publication_type=PublicationType.OTHER,
            tags="movies,documentary,non-fiction",
            dataset_doi="10.1234/documentary-2025",
        )
        db.session.add(doc_meta)
        db.session.flush()

        db.session.add(
            Author(
                name="Documentary Collective",
                affiliation="Docs Org",
                ds_meta_data_id=doc_meta.id
            )
        )

        doc_dataset = MovieDataset(
            ds_meta_data_id=doc_meta.id,
            user_id=user2.id,
            dataset_type="movie",
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(doc_dataset)
        db.session.flush()

        # Añadir una película de ejemplo
        db.session.add(
            Movie(
                movie_dataset_id=doc_dataset.id,
                logical_id=generate_logical_id({"title": "Planet Earth", "year": 2006, "director": "Alastair Fothergill"}),
                title="Planet Earth",
                year=2006,
                director="Alastair Fothergill",
                genre="Documentary",
            )
        )

        db.session.commit()

        # Crear carpeta uploads vacía para el dataset3 (no necesitamos archivos)
        doc_folder = os.path.join(
            working_dir,
            "uploads",
            f"user_{doc_dataset.user_id}",
            f"dataset_{doc_dataset.id}"
        )
        os.makedirs(doc_folder, exist_ok=True)

        # Crear carpeta uploads vacía para el dataset3 (no necesitamos archivos)
        doc_folder = os.path.join(
            working_dir,
            "uploads",
            f"user_{doc_dataset.user_id}",
            f"dataset_{doc_dataset.id}"
        )
        os.makedirs(doc_folder, exist_ok=True)

        # Publicar este dataset creando un registro Fakenodo (status=published)
        doc_fakenodo = Fakenodo(
            status="published",
            dataset_id=doc_dataset.id,
            dataset_file_path=doc_folder,
            doi=doc_meta.dataset_doi
        )
        db.session.add(doc_fakenodo)
        db.session.commit()

        movie_service.create_version(doc_dataset)
        
        # ==========================================================
        # DATASET 3 — DOCUMENTARIES (PEQUEÑO, PARA TEST/SEEDS)
        # ==========================================================
        doc_meta = DSMetaData(
            title="Documentary Highlights",
            description="A small curated set of notable documentaries",
            publication_type=PublicationType.OTHER,
            tags="movies,documentary,non-fiction",
            dataset_doi="10.1234/documentary-2025",
        )
        db.session.add(doc_meta)
        db.session.flush()

        db.session.add(
            Author(
                name="Documentary Collective",
                affiliation="Docs Org",
                orcid="0000-0000-0000-0001",
                ds_meta_data_id=doc_meta.id
            )
        )

        doc_dataset = MovieDataset(
            ds_meta_data_id=doc_meta.id,
            user_id=user1.id,
            dataset_type="movie",
            created_at=datetime.now(timezone.utc),
            community_id=ds.id
        )
        db.session.add(doc_dataset)
        db.session.flush()

        with open(os.path.join(src_folder, "movies3.json"), "r", encoding="utf-8") as f:
            doc_movies_data = json.load(f)

        for data in doc_movies_data:
            logical_id = data.get("logical_id") or generate_logical_id(data)
            db.session.add(
                Movie(
                    movie_dataset_id=doc_dataset.id,
                    logical_id=logical_id,
                    **{k: v for k, v in data.items() if k != "logical_id"}
                )
            )

        db.session.commit()

        # Crear carpeta uploads para el dataset3
        doc_folder = os.path.join(
            working_dir,
            "uploads",
            f"user_{doc_dataset.user_id}",
            f"dataset_{doc_dataset.id}"
        )
        os.makedirs(doc_folder, exist_ok=True)

        src_file = os.path.join(src_folder, "movies3.json")
        dest_file = os.path.join(doc_folder, "movies3.json")
        shutil.copy(src_file, dest_file)

        with open(dest_file, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        fm_meta_doc = FMMetaData(
            filename="movies3.json",
            title="Documentary Movies File",
            description="Documentary dataset file",
            publication_type=PublicationType.OTHER,
            tags="movies,json",
            version="1.0"
        )
        db.session.add(fm_meta_doc)
        db.session.flush()

        feature_model_doc = FeatureModel(
            data_set_id=doc_dataset.id,
            fm_meta_data_id=fm_meta_doc.id
        )
        db.session.add(feature_model_doc)
        db.session.flush()

        db.session.add(
            Hubfile(
                name="movies3.json",
                checksum=file_hash,
                size=os.path.getsize(dest_file),
                feature_model_id=feature_model_doc.id
            )
        )

        db.session.commit()

        # Publicar este dataset creando un registro Fakenodo (status=published)
        doc_fakenodo = Fakenodo(
            status="published",
            dataset_id=doc_dataset.id,
            dataset_file_path=doc_folder,
            doi=doc_meta.dataset_doi
        )
        db.session.add(doc_fakenodo)
        db.session.commit()

        movie_service.create_version(doc_dataset)

        # EDICIONES 

        movie_service.edit_metadata(
            dataset=doc_dataset,
            new_title="Documentary Masterpieces",
            new_description="Updated: A comprehensive collection of award-winning documentaries",
            new_tags="movies,documentary,awards,masterpieces",
            user_id=user1.id,
            comment="Changed title and added more descriptive tags"
        )

        new_authors_with_second = [
            {
                'name': 'Documentary Collective',
                'affiliation': 'Docs Org',
                'orcid': '0000-0000-0000-0001'
            },
            {
                'name': 'Film Archive Team', 
                'affiliation': 'Global Documentary Institute',
                'orcid': '0000-0000-0000-0002'
            }
        ]

        movie_service.edit_authors(
            dataset=doc_dataset,
            new_authors=new_authors_with_second,
            user_id=user1.id,
            comment="Added second author to the team"
        )

        movie_service.edit_community(
            dataset=doc_dataset,
            new_community_id=ai.id,
            user_id=user1.id,
            comment="Moved to AI research community"
        )
        
        new_authors_updated = [
            {
                'name': 'Documentary Collective',
                'affiliation': 'International Documentary Foundation',  # 👈 Cambiado
                'orcid': '0000-0000-0000-0099'  # 👈 Cambiado
            },
            {
                'name': 'Film Archive Team',
                'affiliation': 'Global Documentary Institute',
                'orcid': '0000-0000-0000-0002'
            }
        ]

        movie_service.edit_authors(
            dataset=doc_dataset,
            new_authors=new_authors_updated,
            user_id=user1.id,
            comment="Updated main author affiliation and ORCID"
        )

        db.session.commit()

