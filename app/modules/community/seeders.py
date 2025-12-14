from app import db
from core.seeders.BaseSeeder import BaseSeeder
from app.modules.community.models import Community


class CommunitySeeder(BaseSeeder):
    priority = 2  # ajusta según vuestro orden

    def run(self):
        if Community.query.count() > 0:
            return

        communities = [
            Community(name="Grupo de Investigación en IA", logo_url="investigacionia.png"),
            Community(name="Comunidad de Ciencia de Datos", logo_url="cienciadatos.png"),
        ]
        db.session.add_all(communities)
        db.session.commit()
