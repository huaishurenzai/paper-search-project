import json

import pytest
from fastapi.testclient import TestClient

import app.storage as storage
from app.main import app

def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "paper search API"}

@pytest.fixture
def client(tmp_path, monkeypatch):
    test_data_file = tmp_path / "papers.json"

    initial_papers = [
        {
            "id": 1,
            "title": "Attention Is All You Need",
            "authors": "Vaswani et al.",
            "year": 2017,
            "keywords": ["Transformer", "attention", "NLP"],
        },
        {
            "id": 2,
            "title": "Segment Anything",
            "authors": "Meta AI",
            "year": 2023,
            "keywords": ["CV", "segmentation", "foundation model"],
        },
    ]

    test_data_file.write_text(
        json.dumps(initial_papers, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    monkeypatch.setattr(storage, "DATA_FILE", test_data_file)

    return TestClient(app)

def test_get_papers(client):
    response = client.get("/papers")

    assert response.status_code == 200

    data = response.json()
    assert data["count"] == 2
    assert len(data["papers"]) == 2
    assert data["papers"][0]["title"] == "Attention Is All You Need"

def test_search_papers_no_result(client):
    response = client.get("/papers/search?keyword=nonexistent")

    assert response.status_code == 200

    data = response.json()
    assert data["count"] == 0
    assert data['results'] == []

def test_get_paper_by_id(client):
    response = client.get("/papers/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Attention Is All You Need"

def test_get_paper_not_found(client):
    response = client.get("/papers/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "paper not found"

def test_create_paper(client):
    new_paper = {
         "title": "Vision-Language Agent for Paper Search",
        "authors": "Li Wei, Wang Hao",
        "year": 2024,
        "keywords": ["agent", "VLM", "paper search"],
    }

    response = client.post("/papers", json=new_paper)

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "paper created"
    assert data["paper"]["id"] == 3
    assert data["paper"]["title"] == new_paper["title"]

    list_response = client.get("/papers")
    assert list_response.json()["count"] == 3

def test_update_paper(client):
    updated_paper = {
        "title": "Updated Paper Title",
        "authors": "Updated Author",
        "year": 2025,
        "keywords": ["updated", "test"],
    }

    response = client.put("/papers/1",json=updated_paper)

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "paper updated"
    assert data["paper"]["id"] == 1
    assert data["paper"]["title"] == "Updated Paper Title"

    get_response = client.get("/papers/1")
    assert get_response.json()["title"] == "Updated Paper Title"

def test_delete_paper(client):
    response = client.delete("/papers/1")

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "paper deleted"
    assert data["paper"]["id"] == 1

    get_response = client.get("/papers/1")
    assert get_response.status_code == 404

    list_response = client.get("/papers")
    assert list_response.json()["count"] == 1

def test_create_paper_missing_title(client):
    invalid_paper = {
        "authors": "Someone",
        "year": 2024,
        "keywords": ["test"],
    }

    response = client.post("/papers", json=invalid_paper)
    assert response.status_code == 422

def test_search_papers(client):
    response = client.get("/papers/search?keyword=transformer")

    assert response.status_code == 200

    data = response.json()
    assert data["count"] == 1
    assert data["results"][0]["title"] == "Attention Is All You Need"

def test_create_paper_invalid_year(client):
    invalid_paper = {
        "title": "Invalid Paper",
        "authors": "Someone",
        "year": 1800,
        "keywords": ["test"],
    }

    response = client.post("/papers",json=invalid_paper)

    assert response.status_code == 422

def test_search_papers_empty_keyword(client):
    response = client.get("/papers/search?keyword=")

    assert response.status_code == 400
    assert response.json()["detail"] == "keyword cannot be empty"