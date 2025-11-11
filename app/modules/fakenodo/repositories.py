from app.modules.fakenodo.models import Fakenodo
from core.repositories.BaseRepository import BaseRepository
from app import db

class FakenodoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Fakenodo)
        
    def create_new_fakenodo(self, dataset_id, status="draft"):
        fakenodo = Fakenodo(dataset_id=dataset_id, status=status)
        db.session.add(fakenodo)
        db.session.commit()
        return fakenodo