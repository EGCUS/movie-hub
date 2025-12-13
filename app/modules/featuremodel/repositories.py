from sqlalchemy import func

from app.modules.dataset.base_dataset import BaseDataset
from app.modules.fakenodo.models import Fakenodo
from app.modules.featuremodel.models import FeatureModel, FMMetaData
from core.repositories.BaseRepository import BaseRepository


class FeatureModelRepository(BaseRepository):
    def __init__(self):
        super().__init__(FeatureModel)

    def count_feature_models(self) -> int:
        count = self.model.query.join(
            BaseDataset, self.model.data_set_id == BaseDataset.id
        ).join(
            Fakenodo, BaseDataset.id == Fakenodo.dataset_id
        ).filter(
            BaseDataset.dataset_type == "movie",
            Fakenodo.status == "published"
        ).count()
        
        return count
        


class FMMetaDataRepository(BaseRepository):
    def __init__(self):
        super().__init__(FMMetaData)
