# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.user_data import create_random_user_data


def test_create_user_data(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/user_data/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_username" in content


def test_read_user_data(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = create_random_user_data(db)
    response = client.get(
        f"{settings.API_V1_STR}/user_data/{data.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data.title
    assert content["description"] == data.description
    assert content["id"] == data.id
    assert content["owner_username"] == data.owner_username
