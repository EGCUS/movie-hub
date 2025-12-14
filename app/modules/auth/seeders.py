from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from core.seeders.BaseSeeder import BaseSeeder


class AuthSeeder(BaseSeeder):
    priority = 1  # Higher priority

    def run(self):
        # Datos seed
        users_data = [
            ("user1@example.com", "1234", ("John", "Doe")),
            ("user2@example.com", "1234", ("Jane", "Doe")),
        ]

        seeded_users = []

        # 1) Crear usuarios SOLO si no existen
        for email, password, _name in users_data:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                seeded_users.append(existing_user)
            else:
                new_user = User(email=email, password=password)
                seeded_users.extend(self.seed([new_user]))  # self.seed devuelve lista

        # 2) Crear perfiles SOLO si no existen
        for user, (_email, _password, (name, surname)) in zip(seeded_users, users_data):
            existing_profile = UserProfile.query.filter_by(user_id=user.id).first()
            if existing_profile:
                continue

            profile_data = {
                "user_id": user.id,
                "orcid": "",
                "affiliation": "Some University",
                "name": name,
                "surname": surname,
            }
            self.seed([UserProfile(**profile_data)])
