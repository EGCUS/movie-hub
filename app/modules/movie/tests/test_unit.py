import hashlib
import io
import json
import os
import tempfile
from unittest.mock import mock_open, patch, MagicMock
import pytest
from flask import url_for

# ---------- GET /moviedataset ----------
def test_index_redirects_to_list(test_client):
    response = test_client.get("/moviedataset")
    assert response.status_code == 302
    assert "/moviedataset/list" in response.location


# ---------- GET /moviedataset/list ----------
@patch("app.modules.movie.routes.movie_service.get_all_moviedatasets")
def test_list_datasets(mock_get_all, test_client):
    # Crear mock de dataset con estructura completa
    mock_dataset = MagicMock()
    mock_dataset.id = 1
    mock_dataset.ds_meta_data.title = "Test Dataset"
    mock_dataset.ds_meta_data.description = "Test Description"
    
    mock_get_all.return_value = [mock_dataset]
    
    response = test_client.get("/moviedataset/list")
    assert response.status_code == 200
    mock_get_all.assert_called_once()
    assert b"Test Dataset" in response.data


# ---------- GET /moviedataset/my-datasets ----------
@patch("app.modules.movie.routes.movie_service.get_moviedataset_by_user")
def test_my_datasets_requires_login(mock_get_by_user, test_client):
    # Crear mock de dataset
    mock_dataset = MagicMock()
    mock_dataset.id = 1
    mock_dataset.ds_meta_data.title = "User Dataset"
    mock_dataset.ds_meta_data.description = "User Description"
    
    mock_get_by_user.return_value = [mock_dataset]
    
    # Simular usuario autenticado usando Flask-Login
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.is_active = True
        mock_user.is_anonymous = False
        mock_user.id = 1
        mock_current_user.return_value = mock_user
        
        response = test_client.get("/moviedataset/my-datasets")
        
    assert response.status_code == 200
    assert b"User Dataset" in response.data
    mock_get_by_user.assert_called_once_with(1)


# ---------- GET /moviedataset/<id> ----------
from unittest.mock import patch, MagicMock

@patch("app.modules.movie.routes.ds_view_record_service.create_cookie")
@patch("app.modules.movie.routes.movie_service.get_moviedataset")
def test_view_dataset(mock_get_dataset, mock_create_cookie, test_client):
    # Mock del dataset
    mock_dataset = MagicMock()
    mock_dataset.id = 123
    mock_dataset.ds_meta_data.title = "Mock Dataset"
    mock_dataset.ds_meta_data.description = "Mock Description"
    mock_dataset.ds_meta_data.tags = "test, mock"
    mock_dataset.movies = []

    mock_get_dataset.return_value = mock_dataset

    # Mock de create_cookie para que no intente modificar BD
    mock_create_cookie.return_value = "fake-cookie-value"

    response = test_client.get("/moviedataset/123")

    # --- Asserts ---
    assert response.status_code == 200
    assert b"Mock Dataset" in response.data

    mock_get_dataset.assert_called_once_with(123)
    mock_create_cookie.assert_called_once_with(dataset=mock_dataset)

    # También podemos validar que la cookie se setea:
    assert response.headers.get("Set-Cookie") is not None
    assert "view_cookie=fake-cookie-value" in response.headers.get("Set-Cookie")



# ---------- GET /movie/<id> ----------
@patch("app.modules.movie.routes.movie_service.get_movie")
def test_view_movie(mock_get_movie, test_client):
    # Crear mock completo de la película
    mock_movie = MagicMock()
    mock_movie.id = 42
    mock_movie.title = "Mock Movie"
    mock_movie.year = 2024
    mock_movie.director = "Test Director"
    
    # Mock del dataset relacionado
    mock_dataset = MagicMock()
    mock_dataset.id = 1
    mock_dataset.ds_meta_data.title = "Dataset 1"
    
    mock_movie.dataset = mock_dataset
    mock_get_movie.return_value = mock_movie

    response = test_client.get("/movie/42")
    assert response.status_code == 200
    assert b"Mock Movie" in response.data
    mock_get_movie.assert_called_once_with(42)


# ---------- GET /moviedataset/<id>/download ----------
@patch("app.modules.movie.routes.movie_service.get_moviedataset")
@patch("app.modules.movie.routes.DSDownloadRecordService")
@patch("app.modules.movie.routes.DSDownloadRecord")
def test_download_dataset_creates_zip(mock_record_model, mock_record_service, mock_get_dataset, test_client, tmp_path):
    # --- Mock dataset ---
    dataset_mock = MagicMock()
    dataset_mock.id = 5
    dataset_mock.user_id = 99
    mock_get_dataset.return_value = dataset_mock

    # --- Crear carpeta y archivo en tmp_path ---
    folder = tmp_path / "uploads" / "user_99" / "dataset_5"
    folder.mkdir(parents=True)
    (folder / "test.txt").write_text("contenido")

    # --- Mock de query para que no toque base de datos ---
    mock_record_model.query.filter_by.return_value.first.return_value = None

    # --- Mock os.path.exists + os.walk ---
    with patch("app.modules.movie.routes.os.path.exists", return_value=True), \
         patch("app.modules.movie.routes.os.walk") as mockwalk:
        
        mockwalk.return_value = [(str(folder), [], ["test.txt"])]

        response: Response = test_client.get("/moviedataset/5/download")

    # ---- Assertions ----
    assert response.status_code == 200
    assert response.mimetype == "application/zip"

    # Se llamó al servicio para obtener el dataset
    mock_get_dataset.assert_called_once_with(5)

    # Se debería haber intentado crear un record porque no existía antes
    mock_record_service.return_value.create.assert_called_once()

    # Aseguramos que el zip se haya enviado
    content_disp = response.headers.get("Content-Disposition")
    assert "attachment" in content_disp
    assert "movie_dataset_5.zip" in content_disp



def test_download_dataset_not_found(test_client):
    with patch("app.modules.movie.routes.movie_service.get_moviedataset") as mock_get, \
         patch("app.modules.movie.routes.os.path.exists", return_value=False):
        mock_get.return_value = MagicMock(id=1, user_id=1)
        response = test_client.get("/moviedataset/1/download")
        assert response.status_code == 404

# ---------- GET /moviedataset/<id>/versions ----------
@patch("app.modules.movie.routes.movie_service.get_moviedataset")
def test_compare_versions_page_renders(mock_get_dataset, test_client):
    from datetime import datetime, timedelta

    mock_dataset = MagicMock()
    mock_dataset.id = 10
    mock_dataset.ds_meta_data.title = "Dataset test"

    mock_dataset.versions = [
        MagicMock(id=1, version_number="1", created_at=datetime.utcnow()),
        MagicMock(id=2, version_number="2", created_at=datetime.utcnow() - timedelta(minutes=1)),
    ]

    mock_get_dataset.return_value = mock_dataset

    response = test_client.get("/moviedataset/10/versions")
    assert response.status_code == 200
    assert b"Select two versions to compare" in response.data

# ---------- compare_version_ids ----------
@patch("app.modules.movie.services.MovieService.load_dataset_from_version")
def test_compare_version_ids_detects_changes(mock_load):
    from app.modules.movie.services import MovieService

    class FakeMovie:
        def __init__(self, logical_id, title):
            self.logical_id = logical_id
            self.title = title

    mock_v1 = MagicMock()
    mock_v1.ds_meta_data = {"title": "Title A"}
    mock_v1.movies = [FakeMovie(1, "Movie A")]

    mock_v2 = MagicMock()
    mock_v2.ds_meta_data = {"title": "Title B"}
    mock_v2.movies = [
        FakeMovie(1, "Movie A"),
        FakeMovie(2, "Movie Added")
    ]

    mock_load.side_effect = [mock_v1, mock_v2]

    svc = MovieService()
    diff = svc.compare_version_ids(1, 2)

    assert "title" in diff["metadata_changed"]
    assert diff["movies_added"][0]["logical_id"] == 2
    
    
@patch("app.modules.movie.services.MovieDataset")
def test_get_published_datasets(mock_movie_dataset):
    from app.modules.movie.services import MovieService
    
    # Mock de datasets publicados
    mock_dataset1 = MagicMock()
    mock_dataset1.id = 1
    
    mock_dataset2 = MagicMock()
    mock_dataset2.id = 2
    
    mock_query = MagicMock()
    mock_query.join.return_value.filter.return_value.order_by.return_value = [
        mock_dataset1, mock_dataset2
    ]
    mock_movie_dataset.query = mock_query
    
    service = MovieService()
    result = service.get_published_datasets()
    
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


# ========================================
# GET /moviedataset/my-datasets
# ========================================

@patch("app.modules.movie.routes.movie_service.get_unsynchronized_datasets_by_user")
@patch("app.modules.movie.routes.movie_service.get_moviedataset_by_user")
def test_my_datasets_shows_both_types(mock_get_published, mock_get_drafts, test_client):
    """Test que muestra datasets publicados y drafts del usuario"""
    
    mock_published = MagicMock()
    mock_published.id = 1
    mock_published.ds_meta_data.title = "Published Dataset"
    
    mock_draft = MagicMock()
    mock_draft.id = 2
    mock_draft.ds_meta_data.title = "Draft Dataset"
    
    mock_get_published.return_value = [mock_published]
    mock_get_drafts.return_value = [mock_draft]
    
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_current_user.return_value = mock_user
        
        response = test_client.get("/moviedataset/my-datasets")
    
    assert response.status_code == 200
    assert b"Published Dataset" in response.data
    assert b"Draft Dataset" in response.data
    mock_get_published.assert_called_once_with(1)
    mock_get_drafts.assert_called_once_with(1)


# ========================================
# POST /moviedataset/<id>/publish
# ========================================

@patch("app.modules.fakenodo.models.Fakenodo")
@patch("app.modules.movie.routes.fakenodo_adapter.publish_fakenodo")
@patch("app.modules.movie.routes.movie_service.get_moviedataset")
def test_publish_dataset_success(mock_get_dataset, mock_publish, mock_fakenodo_model, test_client):
    """Test publicar un dataset draft exitosamente"""
    
    mock_dataset = MagicMock()
    mock_dataset.id = 5
    mock_dataset.user_id = 1
    mock_get_dataset.return_value = mock_dataset
    
    mock_fakenodo = MagicMock()
    mock_fakenodo.id = 100
    mock_fakenodo.doi = "10.1234/test"
    mock_fakenodo.status = "published"
    
    mock_publish.return_value = mock_fakenodo
    mock_fakenodo_model.query.filter_by.return_value.first.return_value = mock_fakenodo
    
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_current_user.return_value = mock_user
        
        response = test_client.post("/moviedataset/5/publish")
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Dataset published successfully"
    assert data["doi"] == "10.1234/test"
    assert data["status"] == "published"
    mock_publish.assert_called_once_with(100)


@patch("app.modules.movie.routes.movie_service.get_moviedataset")
def test_publish_dataset_forbidden(mock_get_dataset, test_client):
    """Test que no se puede publicar dataset de otro usuario"""
    
    mock_dataset = MagicMock()
    mock_dataset.id = 5
    mock_dataset.user_id = 999  # Otro usuario
    mock_get_dataset.return_value = mock_dataset
    
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_current_user.return_value = mock_user
        
        response = test_client.post("/moviedataset/5/publish")
    
    assert response.status_code == 403
    data = json.loads(response.data)
    assert "permission" in data["error"]


@patch("app.modules.fakenodo.models.Fakenodo")
@patch("app.modules.movie.routes.movie_service.get_moviedataset")
def test_publish_dataset_no_fakenodo(mock_get_dataset, mock_fakenodo_model, test_client):
    """Test error cuando no existe registro de Fakenodo"""
    
    mock_dataset = MagicMock()
    mock_dataset.id = 5
    mock_dataset.user_id = 1
    mock_get_dataset.return_value = mock_dataset
    
    mock_fakenodo_model.query.filter_by.return_value.first.return_value = None
    
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_current_user.return_value = mock_user
        
        response = test_client.post("/moviedataset/5/publish")
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "Fakenodo record not found" in data["error"]


# ========================================
# GET /moviedataset/<id>/manage
# ========================================

@patch("app.modules.movie.routes.movie_service.get_moviedataset")
def test_manage_dataset_success(mock_get_dataset, test_client):
    """Test acceder a gestión de dataset propio"""
    
    mock_dataset = MagicMock()
    mock_dataset.id = 10
    mock_dataset.user_id = 1
    mock_dataset.ds_meta_data.title = "My Dataset"
    mock_get_dataset.return_value = mock_dataset
    
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_current_user.return_value = mock_user
        
        response = test_client.get("/moviedataset/10/manage")
    
    assert response.status_code == 200
    assert b"My Dataset" in response.data


@patch("app.modules.movie.routes.movie_service.get_moviedataset")
def test_manage_dataset_forbidden(mock_get_dataset, test_client):
    """Test que no se puede gestionar dataset de otro usuario"""
    
    mock_dataset = MagicMock()
    mock_dataset.id = 10
    mock_dataset.user_id = 999
    mock_get_dataset.return_value = mock_dataset
    
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_current_user.return_value = mock_user
        
        response = test_client.get("/moviedataset/10/manage")
    
    assert response.status_code == 403


# ========================================
# POST /moviedataset/upload (DRAFT)
# ========================================

@patch("app.modules.movie.routes.dsmetadata_service")
@patch("app.modules.movie.routes.movie_service.upload_draft_dataset")
def test_upload_dataset_as_draft(mock_upload_draft, mock_dsmetadata, test_client):
    """Test subir dataset como draft"""
    
    mock_dataset = MagicMock()
    mock_dataset.id = 20
    mock_upload_draft.return_value = (mock_dataset, 10, 123)
    
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_user.profile.name = "John"
        mock_user.profile.surname = "Doe"
        mock_user.profile.affiliation = "University"
        mock_user.profile.orcid = ""
        mock_current_user.return_value = mock_user
        
        # Simular datos del formulario
        data = {
            'action': 'draft',
            'title': 'Test Dataset',
            'desc': 'Test Description',
            'publication_type': 'none',
            'publication_doi': '',
            'tags': 'test',
            'authors-0-name': 'Doe, John',
            'authors-0-affiliation': 'University',
            'authors-0-orcid': '',
            'file': (io.BytesIO(json.dumps({"movies": [{"title": "Test", "year": 2020, "director": "Director"}]}).encode()), 'movies.json')
        }
        
        response = test_client.post(
            "/moviedataset/upload",
            data=data,
            content_type='multipart/form-data',
            follow_redirects=False
        )
    
    assert response.status_code == 302  # Redirect
    assert "dataset_id=20" in response.location
    assert "action=draft" in response.location


# ========================================
# POST /moviedataset/upload (PUBLISH)
# ========================================

@patch("app.modules.movie.routes.dsmetadata_service")
@patch("app.modules.movie.routes.movie_service.upload_and_publish_dataset")
def test_upload_dataset_and_publish(mock_upload_publish, mock_dsmetadata, test_client):
    """Test subir dataset y publicar directamente"""
    
    mock_dataset = MagicMock()
    mock_dataset.id = 25
    mock_upload_publish.return_value = (mock_dataset, 15)
    
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_user.profile.name = "Jane"
        mock_user.profile.surname = "Smith"
        mock_user.profile.affiliation = "MIT"
        mock_user.profile.orcid = ""
        mock_current_user.return_value = mock_user
        
        data = {
            'action': 'publish',
            'title': 'Published Dataset',
            'desc': 'Published Description',
            'publication_type': 'none',
            'publication_doi': '',
            'tags': 'published',
            'authors-0-name': 'Smith, Jane',
            'authors-0-affiliation': 'MIT',
            'authors-0-orcid': '',
            'file': (io.BytesIO(json.dumps({"movies": [{"title": "Movie", "year": 2021, "director": "Dir"}]}).encode()), 'movies.json')
        }
        
        response = test_client.post(
            "/moviedataset/upload",
            data=data,
            content_type='multipart/form-data',
            follow_redirects=False
        )
    
    assert response.status_code == 302
    assert "dataset_id=25" in response.location
    assert "action=publish" in response.location


@patch("app.modules.movie.routes.movie_service.upload_draft_dataset")
def test_upload_dataset_validation_error(mock_upload_draft, test_client):
    """Test error de validación al subir dataset"""
    
    mock_upload_draft.side_effect = ValueError("Invalid JSON format")
    
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_user.profile.name = "Test"
        mock_user.profile.surname = "User"
        mock_user.profile.affiliation = ""
        mock_user.profile.orcid = ""
        mock_current_user.return_value = mock_user
        
        data = {
            'action': 'draft',
            'title': 'Bad Dataset',
            'desc': 'Bad',
            'publication_type': 'dataset',
            'authors-0-name': 'User, Test'
        }
        
        data['file'] = (io.BytesIO(b"bad json {{"), 'bad.json')
        
        response = test_client.post(
            "/moviedataset/upload",
            data=data,
            content_type='multipart/form-data'
        )
    
    assert response.status_code == 200  # Vuelve al formulario
    # La página debería mostrar el error


# ========================================
# GET /moviedataset/upload
# ========================================

def test_upload_dataset_get_form(test_client):
    """Test mostrar formulario de upload"""
    
    with patch("flask_login.utils._get_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_user.profile.name = "John"
        mock_user.profile.surname = "Doe"
        mock_user.profile.affiliation = "University"
        mock_user.profile.orcid = ""
        mock_current_user.return_value = mock_user
        
        response = test_client.get("/moviedataset/upload")
    
    assert response.status_code == 200
    assert b"Upload" in response.data or b"upload" in response.data



