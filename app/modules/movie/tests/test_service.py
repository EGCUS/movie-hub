import hashlib
import io
import json
import os
import tempfile
from unittest import mock
from unittest.mock import mock_open, patch, MagicMock
import pytest
from flask import url_for


# ========================================
# TESTS PARA get_published_datasets
# ========================================

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
# TESTS PARA get_unsynchronized_datasets_by_user
# ========================================

@patch("app.modules.movie.services.MovieDataset")
def test_get_unsynchronized_datasets_by_user(mock_movie_dataset):
    from app.modules.movie.services import MovieService
    
    mock_dataset = MagicMock()
    mock_dataset.id = 5
    
    mock_query = MagicMock()
    mock_query.join.return_value.filter.return_value.order_by.return_value.all.return_value = [
        mock_dataset
    ]
    mock_movie_dataset.query = mock_query
    
    service = MovieService()
    result = service.get_unsynchronized_datasets_by_user(user_id=10)
    
    assert len(result) == 1
    assert result[0].id == 5


# ========================================
# TESTS PARA upload_and_publish_dataset
# ========================================

@patch("app.modules.movie.services.MovieService.upload_draft_dataset")
def test_upload_and_publish_dataset_success(mock_upload_draft):
    from app.modules.movie.services import MovieService
    
    mock_dataset = MagicMock()
    mock_dataset.id = 1
    
    mock_upload_draft.return_value = (mock_dataset, 10, 123)
    
    service = MovieService()
    
    with patch.object(service.fakenodo_adapter, 'publish_fakenodo') as mock_publish:
        result_dataset, total_movies = service.upload_and_publish_dataset(
            form=MagicMock(),
            current_user=MagicMock(id=1),
            dsmetadata_service=MagicMock()
        )
    
    assert result_dataset.id == 1
    assert total_movies == 10
    mock_publish.assert_called_once_with(123)


@patch("app.modules.movie.services.MovieService.upload_draft_dataset")
def test_upload_and_publish_dataset_fails(mock_upload_draft):
    from app.modules.movie.services import MovieService
    
    mock_upload_draft.side_effect = ValueError("Invalid JSON")
    
    service = MovieService()
    
    with pytest.raises(ValueError, match="Invalid JSON"):
        service.upload_and_publish_dataset(
            form=MagicMock(),
            current_user=MagicMock(id=1),
            dsmetadata_service=MagicMock()
        )


# ========================================
# Tupload_draft_dataset
# ========================================

@patch("app.modules.movie.services.os.makedirs")
@patch("app.modules.movie.services.db.session")
@patch("app.modules.movie.services.MovieService._create_movie_dataset_with_metadata")
@patch("app.modules.movie.services.MovieService._create_movies")
@patch("app.modules.movie.services.MovieService._create_feature_model_and_hubfile")
@patch("app.modules.movie.services.MovieService.create_version")
def test_upload_draft_dataset_success(
    mock_create_version, mock_create_fm, mock_create_movies,
    mock_create_dataset, mock_session, mock_makedirs
):
    from app.modules.movie.services import MovieService
    
    # Mock del dataset
    mock_dataset = MagicMock()
    mock_dataset.id = 1
    mock_dataset.ds_meta_data.title = "Test Dataset"
    mock_dataset.ds_meta_data.id = 100
    mock_create_dataset.return_value = mock_dataset
    
    # Mock de películas creadas
    mock_create_movies.return_value = 5
    
    # Mock del form con archivos
    mock_file = MagicMock()
    mock_file.filename = "movies.json"
    mock_file.read.return_value = json.dumps({
        "movies": [
            {"title": "Movie 1", "year": 2020, "director": "Director 1"}
        ]
    }).encode('utf-8')
    
    mock_form = MagicMock()
    mock_form.file.data = [mock_file]
    
    mock_user = MagicMock()
    mock_user.id = 1
    
    mock_dsmetadata_service = MagicMock()
    
    service = MovieService()
    
    with patch.object(service.fakenodo_adapter, 'create_fakenodo') as mock_fakenodo, \
         patch.object(service.fakenodo_adapter, 'upload_file_to_fakenodo') as mock_upload, \
         patch("builtins.open", mock_open()):
        
        mock_fakenodo.return_value = {
            "id": 999,
            "deposition_id": 888
        }
        
        dataset, total, fakenodo_id = service.upload_draft_dataset(
            form=mock_form,
            current_user=mock_user,
            dsmetadata_service=mock_dsmetadata_service
        )
    
    assert dataset.id == 1
    assert total == 5
    assert fakenodo_id == 999
    mock_create_movies.assert_called_once()
    mock_fakenodo.assert_called_once()


@patch("app.modules.movie.services.os.makedirs")
@patch("app.modules.movie.services.db.session")
@patch("app.modules.movie.services.MovieService._create_movie_dataset_with_metadata")
def test_upload_draft_dataset_invalid_json(mock_create_dataset, mock_session, mock_makedirs):
    from app.modules.movie.services import MovieService
    
    mock_dataset = MagicMock()
    mock_dataset.id = 1
    mock


@patch("app.modules.movie.services.db.session")
@patch("app.modules.movie.services.MovieService._create_movie_dataset_with_metadata")
def test_upload_draft_dataset_no_files(mock_create_dataset, mock_session):
    from app.modules.movie.services import MovieService
    
    mock_dataset = MagicMock()
    mock_dataset.id = 1
    mock_create_dataset.return_value = mock_dataset
    
    mock_form = MagicMock()
    mock_form.file.data = []
    
    service = MovieService()
    
    with pytest.raises(ValueError, match="No files uploaded"):
        service.upload_draft_dataset(
            form=mock_form,
            current_user=MagicMock(id=1),
            dsmetadata_service=MagicMock()
        )
    
    mock_session.rollback.assert_called_once()


# ========================================
# create_movie_dataset_with_metadata
# ========================================

@patch("app.modules.movie.services.db.session")
@patch("app.modules.movie.services.DSMetaData")
@patch("app.modules.movie.services.Author")
@patch("app.modules.movie.services.MovieDataset")
def test_create_movie_dataset_with_metadata(mock_movie_dataset, mock_author, mock_metadata, mock_session):
    from app.modules.movie.services import MovieService
    
    mock_form = MagicMock()
    mock_form.title.data = "Test Title"
    mock_form.desc.data = "Test Description"
    mock_form.publication_type.data = "journal_article"
    mock_form.publication_doi.data = "10.1234/test"
    mock_form.tags.data = "test,mock"
    mock_form.convert_publication_type.return_value = MagicMock()
    mock_form.get_authors.return_value = [
        {"name": "Author 1", "affiliation": "Uni 1", "orcid": "0000-0001"}
    ]
    
    mock_user = MagicMock()
    mock_user.id = 5
    
    mock_metadata_instance = MagicMock()
    mock_metadata_instance.id = 100
    mock_metadata.return_value = mock_metadata_instance
    
    mock_dataset_instance = MagicMock()
    mock_dataset_instance.id = 200
    mock_movie_dataset.return_value = mock_dataset_instance
    
    service = MovieService()
    result = service._create_movie_dataset_with_metadata(mock_form, mock_user)
    
    assert result.id == 200
    mock_session.add.assert_called()
    mock_session.flush.assert_called()


@patch("app.modules.movie.services.db.session")
@patch("app.modules.movie.services.DSMetaData")
@patch("app.modules.movie.services.MovieDataset")
def test_create_movie_dataset_with_metadata_no_id(mock_movie_dataset, mock_metadata, mock_session):
    from app.modules.movie.services import MovieService
    
    mock_form = MagicMock()
    mock_form.title.data = "Test"
    mock_form.desc.data = "Desc"
    mock_form.publication_type.data = "journal_article"
    mock_form.publication_doi.data = None
    mock_form.tags.data = None
    mock_form.convert_publication_type.return_value = MagicMock()
    mock_form.get_authors.return_value = []
    
    mock_metadata_instance = MagicMock()
    mock_metadata_instance.id = 100
    mock_metadata.return_value = mock_metadata_instance
    
    mock_dataset_instance = MagicMock()
    mock_dataset_instance.id = None  # Simula fallo
    mock_movie_dataset.return_value = mock_dataset_instance
    
    service = MovieService()
    
    with pytest.raises(Exception, match="Failed to create MovieDataset"):
        service._create_movie_dataset_with_metadata(mock_form, MagicMock(id=1))


# ========================================
# TESTS PARA _create_movies
# ========================================

@patch("app.modules.movie.services.db.session")
@patch("app.modules.movie.services.Movie")
def test_create_movies(mock_movie_class, mock_session):
    from app.modules.movie.services import MovieService
    
    movie_data = {
        "movies": [
            {
                "title": "Movie 1",
                "year": 2020,
                "director": "Director 1",
                "genre": "Action"
            },
            {
                "title": "Movie 2",
                "year": 2021,
                "director": "Director 2",
                "genre": "Drama"
            }
        ]
    }
    
    service = MovieService()
    count = service._create_movies(movie_data, dataset_id=10)
    
    assert count == 2
    assert mock_session.add.call_count == 2


@patch("app.modules.movie.services.db.session")
def test_create_movies_empty_list(mock_session):
    from app.modules.movie.services import MovieService
    
    movie_data = {"movies": []}
    
    service = MovieService()
    count = service._create_movies(movie_data, dataset_id=10)
    
    assert count == 0
    mock_session.add.assert_not_called()


# ========================================
# TESTS PARA _create_feature_model_and_hubfile
# ========================================

@patch("app.modules.movie.services.db.session")
@patch("app.modules.movie.services.FMMetaData")
@patch("app.modules.movie.services.FeatureModel")
@patch("app.modules.movie.services.Hubfile")
def test_create_feature_model_and_hubfile(mock_hubfile, mock_fm, mock_fm_meta, mock_session):
    from app.modules.movie.services import MovieService
    
    mock_dataset = MagicMock()
    mock_dataset.id = 1
    mock_dataset.ds_meta_data.title = "Dataset Title"
    mock_dataset.ds_meta_data.publication_type = MagicMock()
    
    file_content = b"test content"
    
    mock_fm_meta_instance = MagicMock()
    mock_fm_meta_instance.id = 100
    mock_fm_meta.return_value = mock_fm_meta_instance
    
    mock_fm_instance = MagicMock()
    mock_fm_instance.id = 200
    mock_fm.return_value = mock_fm_instance
    
    service = MovieService()
    service._create_feature_model_and_hubfile(
        filename="test.json",
        file_content=file_content,
        movie_dataset=mock_dataset
    )
    
    mock_session.add.assert_called()
    mock_session.flush.assert_called()
    
    # Verificar que se calculó el checksum
    expected_checksum = hashlib.md5(file_content).hexdigest()
    mock_hubfile.assert_called_once()
    call_kwargs = mock_hubfile.call_args[1]
    assert call_kwargs['checksum'] == expected_checksum
    assert call_kwargs['size'] == len(file_content)


# ========================================
# TESTS PARA generate_logical_id
# ========================================

def test_generate_logical_id():
    from app.modules.movie.services import MovieService
    
    data = {
        "title": "The Matrix",
        "year": 1999,
        "director": "Wachowski"
    }
    
    service = MovieService()
    logical_id = service.generate_logical_id(data)
    
    expected_base = "The Matrix|1999|Wachowski"
    expected_id = hashlib.sha1(expected_base.encode("utf-8")).hexdigest()
    
    assert logical_id == expected_id
    assert len(logical_id) == 40  # SHA1 tiene 40 caracteres en hex


def test_generate_logical_id_same_data_same_id():
    from app.modules.movie.services import MovieService
    
    data = {
        "title": "Inception",
        "year": 2010,
        "director": "Nolan"
    }
    
    service = MovieService()
    id1 = service.generate_logical_id(data)
    id2 = service.generate_logical_id(data)
    
    assert id1 == id2