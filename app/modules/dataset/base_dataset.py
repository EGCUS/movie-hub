from enum import Enum
from app import db
from datetime import datetime
from sqlalchemy import Enum as SQLAlchemyEnum
from flask import request
from sqlalchemy.ext.declarative import declared_attr


class PublicationType(Enum):
    NONE = "none"
    ANNOTATION_COLLECTION = "annotationcollection"
    BOOK = "book"
    BOOK_SECTION = "section"
    CONFERENCE_PAPER = "conferencepaper"
    DATA_MANAGEMENT_PLAN = "datamanagementplan"
    JOURNAL_ARTICLE = "article"
    PATENT = "patent"
    PREPRINT = "preprint"
    PROJECT_DELIVERABLE = "deliverable"
    PROJECT_MILESTONE = "milestone"
    PROPOSAL = "proposal"
    REPORT = "report"
    SOFTWARE_DOCUMENTATION = "softwaredocumentation"
    TAXONOMIC_TREATMENT = "taxonomictreatment"
    TECHNICAL_NOTE = "technicalnote"
    THESIS = "thesis"
    WORKING_PAPER = "workingpaper"
    OTHER = "other"


class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey("base_dataset.id"), nullable=False)
    version_number = db.Column(db.String(20), nullable=False)  # por ejemplo "1.0", "1.1", "2.0"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    dataset = db.relationship("BaseDataset", back_populates="versions")

    def __repr__(self):
        return f"<Version {self.version_number} of dataset {self.dataset_id}>"


class BaseDataset(db.Model):
    
    __tablename__ = "base_dataset"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    current_version = db.Column(db.String(20), default="1.0")
    dataset_type = db.Column(db.String(120), nullable=False)

    ds_meta_data_id = db.Column(db.Integer, db.ForeignKey("ds_meta_data.id"), nullable=False)

    # @declared_attr
    # def ds_meta_data(cls):
    #     return db.relationship("DSMetaData", backref=db.backref("dataset", uselist=False))

    # @declared_attr
    # def versions(cls):
    #     return db.relationship("Version", back_populates="dataset", cascade="all, delete-orphan")

    # @declared_attr
    # def feature_models(cls):
    #     return db.relationship("FeatureModel", backref="dataset", lazy=True, cascade="all, delete")
    ds_meta_data = db.relationship("DSMetaData", backref=db.backref("dataset", uselist=False))

    versions = db.relationship("Version", back_populates="dataset", cascade="all, delete-orphan")
    feature_models = db.relationship("FeatureModel", backref="dataset", lazy=True, cascade="all, delete")

    __mapper_args__ = {
        "polymorphic_on": dataset_type,
        "polymorphic_identity": "base",
    }

    # Métodos genéricos que dependen de la metadata
    def name(self):
        return self.ds_meta_data.title

    def get_clean_publication_type(self):
        return self.ds_meta_data.publication_type.name.replace("_", " ").title()

    def files(self):
        return [file for fm in self.feature_models for file in fm.files]

    def get_files_count(self):
        return sum(len(fm.files) for fm in self.feature_models)

    def get_file_total_size(self):
        return sum(file.size for fm in self.feature_models for file in fm.files)

    def get_file_total_size_for_human(self):
        from app.modules.dataset.services import SizeService
        return SizeService().get_human_readable_size(self.get_file_total_size())

    def get_doi(self):
        from app.modules.dataset.services import DataSetService
        return DataSetService().get_dataset_doi(self)


# class BaseDataset(db.Model):
    
#     __abstract__ = True #No se crea tabla en la BD para esta clase
#                         #(realmente no hace falta, cada sub-clase tiene la suya)
    
#     id = db.Column(db.Integer, primary_key=True)
#     deposition_id = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     dataset_type = db.Column(db.String(120), nullable=False)
#     current_version = db.Column(db.String(20), default="1.0") # PARA LA VERSION ACTUAL
#     versions = db.relationship("Version", back_populates="dataset", cascade="all, delete-orphan")
#     publication_type = db.Column(SQLAlchemyEnum(PublicationType), nullable=False)
#     publication_doi = db.Column(db.String(120))
#     dataset_doi = db.Column(db.String(120))
#     tags = db.Column(db.String(120))
#     authors = db.relationship("Author", backref="dataset", lazy=True, cascade="all, delete")
#     feature_models = db.relationship("FeatureModel", backref="data_set", lazy=True, cascade="all, delete")

    
#     __mapper_args__ = { #Esto define el tipo de dataset, cada uno debe definir su identity, para UVLDataet puede ser "uvl"
#         "polymorphic_on": dataset_type,
#         "polymorphic_identity": "base",
#     }
    
#     def name(self):
#         return self.id
    
#     def files(self): #?? Hay que probar si funciona con featureModel
#         return [file for fm in self.feature_models for file in fm.files]
    
#     def get_clean_publication_type(self):
#         return self.publication_type.name.replace("_", " ").title()
    
#     def get_files_count(self): #?? Lo mismo que files
#         return sum(len(fm.files) for fm in self.feature_models)
    
#     def get_file_total_size(self): #?? Lo mismo que files
#         return sum(file.size for fm in self.feature_models for file in fm.files)
    
#     def get_file_total_size_for_human(self):
#         from app.modules.dataset.services import SizeService

#         return SizeService().get_human_readable_size(self.get_file_total_size())
    
#     def get_doi(self):
#         from app.modules.dataset.services import DataSetService

#         return DataSetService().get_dataset_doi(self)
    
#     # Método para agregar nueva versión
#     def add_version(self, version_number):
#         new_version_number = str(float(version_number) + 1.0)
#         new_version = Version(dataset=self, version_number=new_version_number)
#         db.session.add(new_version)
#         self.current_version = version_number  # actualizar versión actual
#         db.session.commit()
#         return new_version

#     def get_versions(self):
#         # Devuelve todas las versiones ordenadas por fecha de más antigua a más nueva
#         return sorted(self.versions, key=lambda v: v.created_at, reverse=True)
    
    
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
        
#     def __repr__(self):
#         return f"BaseDataset<id={self.id} type={self.dataset_type}>"
    
#     def to_dict(self):
#         raise NotImplementedError("Each dataset type should define its own to_dict method")