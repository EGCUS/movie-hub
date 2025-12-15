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
            Community(name="Disney Community", logo_url="diseney.jpg"),
            Community(name="80s Shows", logo_url="80s.jpg"),
            Community(name="Sci-Fi Fans", logo_url="fan.jpeg"),
            Community(name="Romantic Films Circle", logo_url="love.jpg"),
            Community(name="Warner Community", logo_url="warner.png"),
            
        ]
        db.session.add_all(communities)
        db.session.commit()
