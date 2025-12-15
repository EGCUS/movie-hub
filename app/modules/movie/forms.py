import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, MultipleFileField
from jsonschema import ValidationError
from wtforms import FieldList, FormField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, ValidationError as WTFormsValidationError
from app.modules.community.models import Community
from app.modules.dataset.models import PublicationType


def validate_author_name(form, field):
    if any(char.isdigit() for char in field.data):
        raise WTFormsValidationError("El nombre del autor no puede contener números")
    if field.data.count(',') > 1:
        raise WTFormsValidationError("El nombre solo puede contener una coma como máximo")


def validate_orcid(form, field):
    if not field.data or field.data.strip() == '':
        return
    
    if field.data.strip() == '0000-0000-0000-0000':
        return
    
    orcid_pattern = r'^\d{4}-\d{4}-\d{4}-\d{4}$'
    if not re.match(orcid_pattern, field.data.strip()):
        raise WTFormsValidationError("El ORCID debe tener el formato XXXX-XXXX-XXXX-XXXX con dígitos")


class AuthorForm(FlaskForm):
    name = StringField(
        "Name", 
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            validate_author_name
        ],
        description="Formato: Apellido(s), Nombre"
    )
    affiliation = StringField("Affiliation", validators=[Optional()])
    orcid = StringField(
        "ORCID", 
        validators=[Optional(), validate_orcid],
        description="Formato: XXXX-XXXX-XXXX-XXXX"
    )

    def get_author(self):
        """Procesa y retorna los datos del autor normalizados"""
        try:
            name = self.format_author_name(self.name.data)
        except ValueError as e:
            raise ValidationError(str(e))
        
        orcid_value = self.orcid.data.strip() if self.orcid.data else ''
        if not orcid_value or orcid_value == '':
            orcid_value = '0000-0000-0000-0000'

        return {
            "name": name,
            "affiliation": self.affiliation.data.strip() if self.affiliation.data else None,
            "orcid": orcid_value,
        }

    def format_author_name(self, name: str) -> str:
        name = name.strip()

        # Caso 1: Ya tiene formato "Apellido, Nombre"
        if ',' in name :
            parts = [p.strip() for p in name.split(',', 1)]

            # Validar que tenga ambas partes (apellido Y nombre)
            if len(parts) != 2 or not parts[0] or not parts[1]:
                raise ValueError("Debe incluir al menos nombre y apellido en formato 'Apellido, Nombre'")

            last_name = parts[0].title()
            first_names = ' '.join(p.title() for p in parts[1].split())
            return f"{last_name}, {first_names}"

        # Caso 2: Sin coma - convertir "Nombre Apellido" → "Apellido, Nombre"
        if not ',' in name:
            parts = name.split()

            if len(parts) < 2:
                raise ValueError("Debe incluir al menos nombre y apellido")

            last_name = parts[-1].title()
            first_names = ' '.join(p.title() for p in parts[:-1])
            return f"{last_name}, {first_names}"
        else:
            raise ValueError("Formato de nombre inválido")

    class Meta:
        csrf = False


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

    tags = StringField("Tags (separated by commas)", validators=[DataRequired()])

    # Community (existing or new)
    community_id = SelectField(
        "Community",
        choices=[],
        coerce=int,
        validators=[Optional()],
        validate_choice=False,
        default=0
    )

    new_community_name = StringField(
        "New Community Name",
        validators=[Optional(), Length(max=120)]
    )

    new_community_logo = FileField(
        "New Community Logo",
        validators=[Optional(), FileAllowed(['png', 'jpg', 'jpeg', 'svg'], 'Only image files are allowed!')]
    )

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

    def get_selected_community_id(self):
        cid = self.community_id.data
        if cid in (None, 0):
            return None
        return cid

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


class MovieEditMetadataForm(FlaskForm):
    """Form for minor metadata edits (no new DOI)"""
    title = StringField("Title", validators=[DataRequired(), Length(max=120)])
    desc = TextAreaField("Description", validators=[DataRequired()])
    tags = StringField("Tags (separated by commas)", validators=[DataRequired()]) #Al menos incluir una tag
    authors = FieldList(FormField(AuthorForm), min_entries=1)
    
    community_id = SelectField(
        "Community",
        coerce=int,
        validators=[Optional()]
    )

    edit_comment = TextAreaField(
        "Edit Comment",
        validators=[Optional(), Length(max=500)],
        description="Optional: Describe what you changed"
    )

    submit = SubmitField("Save Changes")
    
    def __init__(self, *args, **kwargs):
        """Constructor que carga las comunidades automáticamente"""
        super(MovieEditMetadataForm, self).__init__(*args, **kwargs)
        communities = Community.query.order_by(Community.name.asc()).all()
        self.community_id.choices = [(0, "-- No Community --")] + [(c.id, c.name) for c in communities]

    
    def get_authors(self):
        return [author.get_author() for author in self.authors]
