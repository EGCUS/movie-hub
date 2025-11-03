from app import db
from datetime import datetime

class BaseDataset(db.Model):
    
    __abstract__ = True #No se crea tabla en la BD para esta clase
                        #(realmente no hace falta, cada sub-clase tiene la suya)
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dataset_type = db.Column(db.String(120), nullable=False)
    
    __mapper_args__ = { #Esto define el tipo de dataset, cada uno debe definir su identity, para UVLDataet puede ser "uvl"
        "polymorphic_on": dataset_type,
        "polymorphic_identity": "base",
    }
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return f"BaseDataset<id={self.id} type={self.dataset_type}>"
    
    def to_dict(self):
        raise NotImplementedError("Each dataset type should define its own to_dict method")
