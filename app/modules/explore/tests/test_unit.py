import json
from unittest.mock import patch, MagicMock


def test_explore_get_renders_page(test_client):
    res = test_client.get("/explore")
    assert res.status_code == 200
    assert b"Explore" in res.data


@patch("app.modules.explore.routes.Community")
def test_explore_communities_returns_empty_list(mock_community, test_client):
    mock_community.query.order_by().all.return_value = []

    res = test_client.get("/explore/communities")
    assert res.status_code == 200
    assert res.get_json() == []


@patch("app.modules.explore.routes.Community")
def test_explore_communities_returns_json(mock_community, test_client):
    c1 = MagicMock()
    c1.id = 1
    c1.name = "Grupo IA"
    c1.logo_url = "investigacionia.png"

    mock_community.query.order_by().all.return_value = [c1]

    res = test_client.get("/explore/communities")
    assert res.status_code == 200

    data = res.get_json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Grupo IA"
    assert "logo_url" in data[0]


@patch("app.modules.explore.routes.ExploreService")
def test_explore_post_calls_filter_with_community_id(mock_service, test_client):
    ds = MagicMock()
    ds.id = 10
    ds.to_dict.return_value = {"id": 10, "title": "Dataset X"}

    mock_service.return_value.filter.return_value = [ds]

    payload = {
        "csrf_token": "dummy",
        "query": "ia",
        "publication_type": "any",
        "sorting": "newest",
        "community_id": 1
    }

    res = test_client.post(
        "/explore",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert data[0]["id"] == 10

    mock_service.return_value.filter.assert_called_once()
    called_kwargs = mock_service.return_value.filter.call_args.kwargs
    assert called_kwargs.get("community_id") == 1


@patch("app.modules.explore.routes.ExploreService")
def test_explore_post_includes_dataset_url(mock_service, test_client):
    ds = MagicMock()
    ds.id = 10
    ds.to_dict.return_value = {"id": 10, "title": "Dataset X"}

    mock_service.return_value.filter.return_value = [ds]

    payload = {
        "csrf_token": "dummy",
        "query": "",
        "publication_type": "any",
        "sorting": "newest",
    }

    res = test_client.post("/explore", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 200
    data = res.get_json()

    assert "url" in data[0]
    assert f"/moviedataset/{ds.id}" in data[0]["url"]

