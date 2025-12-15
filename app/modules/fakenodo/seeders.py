from core.seeders.BaseSeeder import BaseSeeder
from app.modules.fakenodo.models import Fakenodo
from app.modules.dataset.models import BaseDataset

class FakenodoSeeder(BaseSeeder):
    priority = 4  # se ejecuta después de AuthSeeder, DataSeeder y MovieSeeder

    def run(self):

        dataset1 = BaseDataset.query.filter_by(id=1).first()
        dataset2 = BaseDataset.query.filter_by(id=2).first()
        dataset3 = BaseDataset.query.filter_by(id=3).first()

        if not all([dataset1, dataset2, dataset3]):
            print("Algunos datasets no existen. Ejecuta primero el MovieSeeder o DataSeeder.")
            return

        to_seed = []

        # Only create Fakenodo records when they don't already exist
        existing1 = Fakenodo.query.filter_by(dataset_id=dataset1.id).first()
        if not existing1:
            to_seed.append(Fakenodo(status="draft", dataset_id=dataset1.id, dataset=dataset1))

        existing2 = Fakenodo.query.filter_by(dataset_id=dataset2.id).first()
        if not existing2:
            to_seed.append(Fakenodo(status="published", dataset_id=dataset2.id, dataset=dataset2))

        existing3 = Fakenodo.query.filter_by(dataset_id=dataset3.id).first()
        if not existing3:
            to_seed.append(Fakenodo(status="draft", dataset_id=dataset3.id, dataset=dataset3))

        if to_seed:
            self.seed(to_seed)