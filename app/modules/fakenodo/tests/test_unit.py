import hashlib
import pytest
from app.modules.fakenodo.services import FakenodoService


def test_checksum_ok(tmp_path):
    """Comprueba que checksum calcula bien el SHA-256 de un archivo."""
    file = tmp_path / "test.txt"
    file.write_text("hola", encoding="utf-8")

    result = FakenodoService.checksum(str(file))

    expected = hashlib.sha256("hola".encode("utf-8")).hexdigest()
    assert result == expected


def test_checksum_file_not_found():
    """Si el archivo no existe, debe lanzar una excepción con mensaje claro."""
    with pytest.raises(Exception) as excinfo:
        FakenodoService.checksum("no_existe_123456.txt")

    msg = str(excinfo.value)
    assert "not found" in msg.lower()
