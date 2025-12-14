from unittest.mock import patch, MagicMock


@patch("app.modules.community.routes.Community")
def test_api_list_communities_returns_json(mock_community, test_client):
    mock_c1 = MagicMock()
    mock_c1.id = 1
    mock_c1.name = "IA"
    mock_c1.logo_url = "ia.png"

    mock_community.query.order_by().all.return_value = [mock_c1]

    response = test_client.get("/api/communities")

    assert response.status_code == 200
    assert b"IA" in response.data
