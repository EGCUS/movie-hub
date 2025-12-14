from app import db


class Community(db.Model):
    __tablename__ = "community"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    logo_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Community {self.id} {self.name}>"
