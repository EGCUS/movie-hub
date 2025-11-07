import hashlib

from app.modules.fakenodo.repositories import FakenodoRepository
from core.services.BaseService import BaseService
from app.modules.movie.models import MovieDataset
from app.modules.featuremodel.models import FeatureModel


class FakenodoService(BaseService):
    def __init__(self):
        super().__init__(FakenodoRepository())
    
    def create_fakenodo(self, dataset=MovieDataset):
        #TO-DO: funcion que cree un nuevo dataset
        pass
        
    def upload_dataset(self, fakenodo_id, dataset=MovieDataset, feature_model=FeatureModel):
        #TO-DO: funcion suba un fichero al reposiotrio de datasets
        pass
    
    def publish_fakenodo(self, fakenodo_id):
        #TO-DO: funcion que publique un dataset
        pass
    
    def get_fakenodo(self, fakenodo_id):
        #TO-DO: funcion que obtenga un dataset por su id
        pass
    
    def get_doi_versions(self, fakenodo_id):
        #TO-DO: funcion para listar las versiones de un dataset
        pass
    
    def checksum(fileName):
        try:
            with open(fileName, "rb") as file:
                file_content = file.read()
                res = hashlib.sha256(file_content).hexdigest()
            return res
        except FileNotFoundError:
            raise Exception(f"File {fileName} not found for checksum calculation")
        except Exception as e:
            raise Exception(f"Error calculating checksum for file {fileName}: {str(e)}")
