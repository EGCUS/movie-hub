from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, MultipleFileField
from wtforms import FieldList, FormField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length
from app.modules.dataset.models import PublicationType

class AuthorForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    affiliation = StringField("Affiliation")
    orcid = StringField("ORCID")
    
    class Meta:
        csrf = False
    
    def get_author(self):
        return {
            "name": self.name.data,
            "affiliation": self.affiliation.data,
            "orcid": self.orcid.data,
        }

class MovieForm(FlaskForm):
    # Dataset metadata
    title = StringField("Dataset Title", validators=[DataRequired()])
    desc = TextAreaField("Description", validators=[DataRequired()])
    publication_type = SelectField(
        "Publication type",
        choices=[(pt.value, pt.name.replace("_", " ").title()) for pt in PublicationType],
        validators=[DataRequired()],
        default=PublicationType.OTHER.value
    )
    publication_doi = StringField("Publication DOI", validators=[Optional()])
    tags = StringField("Tags (separated by commas)", validators=[Optional()])
    
    authors = FieldList(FormField(AuthorForm))
    
    # File upload
    file = MultipleFileField(
            "Movie Dataset Files", 
            validators=[
                FileRequired(message="Please select at least one file"),
                FileAllowed(['json'], 'Only JSON files are allowed!')
            ]
        )
    
    submit = SubmitField("Upload Dataset")
    
    def get_dsmetadata(self):
        publication_type_converted = self.convert_publication_type(self.publication_type.data)
        return {
            "title": self.title.data,
            "description": self.desc.data,
            "publication_type": publication_type_converted,
            "publication_doi": self.publication_doi.data,
            "tags": self.tags.data,
        }
    
    def convert_publication_type(self, value):
        for pt in PublicationType:
            if pt.value == value:
                return pt
        return PublicationType.NONE
    
    def get_authors(self):
        return [author.get_author() for author in self.authors]
    
