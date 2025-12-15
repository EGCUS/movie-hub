import hashlib
import io
from types import SimpleNamespace
from unittest.mock import patch, MagicMock
import pytest
from app.modules.fakenodo.services import FakenodoService

""""
def test_checksum_ok(tmp_path):
    #Comprueba que checksum calcula bien el SHA-256 de un archivo
    file = tmp_path / "test.txt"
    file.write_text("hola", encoding="utf-8")

    result = FakenodoService.checksum(str(file))

    expected = hashlib.sha256("hola".encode("utf-8")).hexdigest()
    assert result == expected


def test_checksum_file_not_found():
    #Si el archivo no existe, debe lanzar una excepción con mensaje claro
    with pytest.raises(Exception) as excinfo:
        FakenodoService.checksum("no_existe_123456.txt")

    msg = str(excinfo.value)
    assert "not found" in msg.lower()
"""

# ---------- GET /fakenodo ----------


def test_fakenodo_index_ok(test_client):
    resp = test_client.get("/fakenodo")
    assert resp.status_code == 200


# ---------- POST /fakenodo/create ----------
@patch("app.modules.fakenodo.routes.FakenodoService")
@patch("app.modules.fakenodo.routes.db")
@patch("app.modules.fakenodo.routes.BaseDataset")
def test_create_fakenodo_ok(MockBaseDataset, mock_db, MockFakenodoService,
                            test_client):
    dataset_mock = MagicMock()
    dataset_mock.id = 123
    MockBaseDataset.return_value = dataset_mock

    service_instance = MockFakenodoService.return_value
    service_instance.create_fakenodo.return_value = {
        "id": 10,
        "status": "draft",
    }

    payload = {
        "metadata_id": 1,
        "user_id": 42,
    }

    resp = test_client.post("/fakenodo/create", json=payload)

    assert resp.status_code == 201
    data = resp.get_json()
    assert data["message"] == "MovieDataset successfully created in Fakenodo."
    assert data["dataset_id"] == 123
    assert data["fakenodo_id"] == 10

    MockBaseDataset.assert_called_once()
    service_instance.create_fakenodo.assert_called_once_with(dataset_mock)
    mock_db.session.add.assert_called()
    mock_db.session.commit.assert_called()


def test_upload_dataset_missing_file(test_client):
    resp = test_client.post("/fakenodo/upload/1", data={},
                            content_type="multipart/form-data")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["ok"] is False
    assert "file is required" in data["error"]


# ---------- POST /fakenodo/publish/<id> ----------

@patch("app.modules.fakenodo.routes.FakenodoService")
def test_publish_fakenodo_ok(MockFakenodoService, test_client):
    service_instance = MockFakenodoService.return_value

    fakenodo_obj = MagicMock()
    fakenodo_obj.id = 5
    fakenodo_obj.status = "published"
    fakenodo_obj.doi = "10.1234/moviehub.fake.aaaa1111"

    service_instance.publish_fakenodo.return_value = fakenodo_obj

    resp = test_client.post("/fakenodo/publish/5")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == 5
    assert data["status"] == "published"
    assert data["doi"] == "10.1234/moviehub.fake.aaaa1111"

    service_instance.publish_fakenodo.assert_called_once_with(5)


@patch("app.modules.fakenodo.routes.FakenodoService")
def test_publish_fakenodo_not_found(MockFakenodoService, test_client):
    service_instance = MockFakenodoService.return_value
    service_instance.publish_fakenodo.side_effect = ValueError(
                                    "Fakenodo with ID 99 not found")

    resp = test_client.post("/fakenodo/publish/99")

    assert resp.status_code == 400
    data = resp.get_json()
    assert "not found" in data["error"].lower()


# ---------- GET /fakenodo/<id> ----------

@patch("app.modules.fakenodo.routes.FakenodoService")
def test_get_one_fakenodo_ok(MockFakenodoService, test_client):
    service_instance = MockFakenodoService.return_value
    service_instance.get_fakenodo.return_value = {
        "dataset_metadata": {"title": "Test dataset"},
        "status": "draft",
    }

    resp = test_client.get("/fakenodo/1")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["dataset_metadata"]["title"] == "Test dataset"
    assert data["status"] == "draft"

    service_instance.get_fakenodo.assert_called_once_with(1)


@patch("app.modules.fakenodo.routes.FakenodoService")
def test_get_one_fakenodo_not_found(MockFakenodoService, test_client):
    service_instance = MockFakenodoService.return_value
    service_instance.get_fakenodo.side_effect = FileNotFoundError(
                                            "Fakenodo object not found")

    resp = test_client.get("/fakenodo/123")

    assert resp.status_code == 404
    data = resp.get_json()
    assert "not found" in data["error"].lower()


# ---------- GET /fakenodo/<id>/versions ----------

@patch("app.modules.fakenodo.routes.FakenodoService")
def test_get_doi_versions_ok(MockFakenodoService, test_client):
    service_instance = MockFakenodoService.return_value
    service_instance.get_doi_versions.return_value = {
        "version-list": "Version1, Version2",
        "current-version": "Version2",
        "doi": "10.1234/moviehub.fake.version2",
    }

    resp = test_client.get("/fakenodo/1/versions")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["current-version"] == "Version2"
    assert "Version1" in data["version-list"]

    service_instance.get_doi_versions.assert_called_once_with(1)


# ---------- POST /fakenodo/upload/<id> ----------


@patch("app.modules.fakenodo.routes.FakenodoService")
@patch("app.modules.fakenodo.routes.db")
def test_upload_dataset_ok(mock_db, MockFakenodoService, test_client):
    # Fake del servicio que usa la ruta
    class FakeFakenodoService:
        def upload_file_to_fakenodo(self, **kwargs):
            # Podemos comprobar que la ruta le pasa lo que esperamos
            assert kwargs["fakenodo_id"] == 7
            assert kwargs["dataset_id"] == 1

            # Devolvemos exactamente lo que la ruta espera leer
            return {
                "fakenodo_id": kwargs["fakenodo_id"],
                "dataset_id": kwargs["dataset_id"],
                "file_path": "datasets/fakenodo_7/dataset_1/dataset.csv",
                "checksum": "fakechecksum123",
                "status": "draft",
            }

    # Cuando en la ruta se haga FakenodoService(), devolvemos nuestro fake
    MockFakenodoService.return_value = FakeFakenodoService()

    # Simulamos el formulario enviado desde el cliente
    data = {
        "file": (io.BytesIO(b"dummy content"), "dataset.csv"),
        "dataset_id": "1",
    }

    resp = test_client.post(
        "/fakenodo/upload/7",
        data=data,
        content_type="multipart/form-data",
    )

    assert resp.status_code == 200
    json_data = resp.get_json()

    assert json_data["ok"] is True
    assert json_data["fakenodo_id"] == 7
    assert json_data["dataset_id"] == 1
    assert json_data["status"] == "draft"
    assert "file_path" in json_data
    assert "checksum" in json_data

    mock_db.session.commit.assert_called()
