import os
import shutil
from datetime import datetime, timezone
from dotenv import load_dotenv

from app import db
from app.modules.auth.models import User
from app.modules.dataset.models import Author, DataSet, DSMetaData, DSMetrics, PublicationType
from app.modules.featuremodel.models import FeatureModel, FMMetaData
from app.modules.hubfile.models import Hubfile
from core.seeders.BaseSeeder import BaseSeeder


class DataSetSeeder(BaseSeeder):

    priority = 2

    def run(self):
        # 🔹 Recuperar usuarios existentes
        user1 = User.query.filter_by(email="user1@example.com").first()
        user2 = User.query.filter_by(email="user2@example.com").first()
        if not user1 or not user2:
            raise Exception("Users not found. Please seed users first.")

        # 🔹 Crear métricas
        ds_metrics = DSMetrics(number_of_models="5", number_of_features="50")
        db.session.add(ds_metrics)
        db.session.flush()  # para obtener el ID

        # 🔹 Crear metadatos de datasets
        ds_meta_data_list = []
        for i in range(4):
            ds_meta = DSMetaData(
                deposition_id=i + 1,
                title=f"Sample dataset {i + 1}",
                description=f"Description for dataset {i + 1}",
                publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
                publication_doi=f"10.1234/dataset{i + 1}",
                dataset_doi=f"10.1234/dataset{i + 1}",
                tags="tag1, tag2",
                ds_metrics_id=ds_metrics.id,
            )
            ds_meta_data_list.append(ds_meta)
        db.session.add_all(ds_meta_data_list)
        db.session.flush()

        # 🔹 Crear autores de datasets
        authors = []
        for i, ds_meta in enumerate(ds_meta_data_list):
            author = Author(
                name=f"Author {i + 1}",
                affiliation=f"Affiliation {i + 1}",
                orcid=f"0000-0000-0000-000{i}",
                ds_meta_data_id=ds_meta.id,
            )
            authors.append(author)
        db.session.add_all(authors)
        db.session.flush()

        # 🔹 Crear datasets (heredan de BaseDataset)
        datasets = []
        for i, ds_meta in enumerate(ds_meta_data_list):
            dataset = DataSet(
                user_id=user1.id,
                ds_meta_data_id=ds_meta.id,
                created_at=datetime.now(timezone.utc),
                dataset_type="uvl",
            )
            datasets.append(dataset)
        db.session.add_all(datasets)
        db.session.flush()

        # 🔹 Crear metadatos de FeatureModels
        fm_meta_data_list = []
        for i in range(12):
            fm_meta = FMMetaData(
                uvl_filename=f"file{i + 1}.uvl",
                title=f"Feature Model {i + 1}",
                description=f"Description for feature model {i + 1}",
                publication_type=PublicationType.SOFTWARE_DOCUMENTATION,
                publication_doi=f"10.1234/fm{i + 1}",
                tags="tag1, tag2",
                uvl_version="1.0",
            )
            fm_meta_data_list.append(fm_meta)
        db.session.add_all(fm_meta_data_list)
        db.session.flush()

        # 🔹 Crear autores de FeatureModels
        fm_authors = []
        for i, fm_meta in enumerate(fm_meta_data_list):
            fm_author = Author(
                name=f"Author {i + 5}",
                affiliation=f"Affiliation {i + 5}",
                orcid=f"0000-0000-0000-000{i + 5}",
                fm_meta_data_id=fm_meta.id,
            )
            fm_authors.append(fm_author)
        db.session.add_all(fm_authors)
