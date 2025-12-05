import hashlib
import os

from app.modules.fakenodo.repositories import FakenodoRepository
from app import db
from core.services.BaseService import BaseService
from app.modules.movie.models import MovieDataset, BaseDataset
from app.modules.featuremodel.models import FeatureModel
from app.modules.fakenodo.models import Fakenodo
from app.modules.dataset.services import SizeService
import uuid
import logging

logger = logging.getLogger(__name__)


class FakenodoService(BaseService):
    def __init__(self):
        super().__init__(FakenodoRepository())
    
    def create_fakenodo(self, dataset=BaseDataset):
        try:
            logger.info(f"Creating Fakenodo for dataset ID {dataset.id}...")

            fakenodo = self.repository.create_new_fakenodo(dataset_id=dataset.id)
            deposition_id = fakenodo.id 

            fakenodo_response = {
                "id": fakenodo.id,
                "fakenodo_doi": fakenodo.doi,
                "deposition_id": deposition_id,
                "dataset_metadata": dataset.ds_meta_data.to_dict(),
                "status": fakenodo.status
            }

            return fakenodo_response

        except Exception as error:
            logger.exception("Error creating Fakenodo record.")
            raise Exception(f"Failed to create Fakenodo record: {str(error)}")


    def publish_fakenodo(self, fakenodo_id):
        fakenodo = self.get_by_id(fakenodo_id)
        if not fakenodo:
            raise ValueError(f"Fakenodo with ID {fakenodo_id} not found")

        if fakenodo.status == "published":
            raise ValueError(f"Fakenodo {fakenodo_id} is already published")

        fake_doi = f"10.1234/moviehub.fake.{uuid.uuid4().hex[:8]}"

        fakenodo.status = "published"
        fakenodo.doi = fake_doi

        self.update(fakenodo.id, status=fakenodo.status, doi=fakenodo.doi)

        return fakenodo

    def get_fakenodo(self, fakenodo_id):
        fakenodo = Fakenodo.query.get(fakenodo_id)
        if not fakenodo:
            raise FileNotFoundError("Fakenodo object not found")
        
        change_logs = [
        log.to_dict() for log in fakenodo.dataset.change_logs
    ]
        response = {
            "fakenodo_doi": fakenodo.doi,
            "deposition_id": fakenodo.id,
            "dataset_metadata": fakenodo.dataset.ds_meta_data.to_dict(),
            "status": fakenodo.status,
            "minor_change_logs": change_logs
        }
        return response

    def get_doi_versions(self, fakenodo_id):

        fakenodo = Fakenodo.query.get(fakenodo_id)
        if not fakenodo:
            raise FileNotFoundError("Fakenodo object not found")
        response = {
            "version-list": fakenodo.dataset.versions.__repr__(),
            "current-version": fakenodo.dataset.current_version,
            "doi": fakenodo.doi,
        }
        return response
    
    def checksum(self, fileName):
        try:
            with open(fileName, "rb") as file:
                file_content = file.read()
                res = hashlib.sha256(file_content).hexdigest()
            return res
        except FileNotFoundError:
            raise Exception(f"File {fileName} not found for checksum calculation")
        except Exception as e:
            raise Exception(f"Error calculating checksum for file {fileName}: {str(e)}")
        
        
    def upload_file_to_fakenodo(self, fakenodo_id: int, file_content: bytes, filename: str, dataset_id: int):
        """
        Upload a file to Fakenodo (mock external service).
        
        Args:
            fakenodo_id: ID of the Fakenodo record
            file_content: Binary content of the file
            filename: Name of the file
            dataset_id: ID of the dataset
            
        Returns:
            dict with file info
        """
        # 1️⃣ Validate Fakenodo
        fakenodo = self.get_by_id(fakenodo_id)
        if not fakenodo:
            raise ValueError(f"Fakenodo with ID {fakenodo_id} not found")

        # 2️⃣ Generate file path inside Fakenodo
        fakenodo_folder = os.path.join("datasets", f"fakenodo_{fakenodo_id}", f"dataset_{dataset_id}")
        os.makedirs(fakenodo_folder, exist_ok=True)
        file_path = os.path.join(fakenodo_folder, filename)

        # 3️⃣ Save the file
        with open(file_path, "wb") as f:
            f.write(file_content)

        # 4️⃣ Validate integrity
        checksum = hashlib.md5(file_content).hexdigest()
        with open(file_path, "rb") as f:
            if hashlib.md5(f.read()).hexdigest() != checksum:
                raise Exception(f"Corrupted file detected in Fakenodo copy of '{filename}'")

        # 5️⃣ Update Fakenodo status
        fakenodo.dataset_file_path = fakenodo_folder
        fakenodo.status = "dataset_uploaded"
        self.update(
            fakenodo.id,
            dataset_file_path=fakenodo.dataset_file_path,
            status=fakenodo.status
        )

        # 6️⃣ Return minimal info
        return {
            "fakenodo_id": fakenodo_id,
            "dataset_id": dataset_id,
            "file_path": file_path,
            "checksum": checksum,
            "status": fakenodo.status
        }

        
        



            