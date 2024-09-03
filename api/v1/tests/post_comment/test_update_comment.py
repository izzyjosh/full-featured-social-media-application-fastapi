import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)


import pytest
from main import app
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

client = TestClient(app)

endpoint = "api/v1/posts/ac3d6659-8f67-4a67-b690-9f77fab7e6e3/comments/dd0030f4-2370-4bdf-8d20-00b52f167fb3"


def test_update_comment_success(
    mock_db_session: Session, access_token, current_user, mock_update_comment
):

    response = client.patch(
        endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        json={"comment": "Test update comment"},
    )

    assert response.status_code == 200
    assert response.json()["status_code"] == 200
    assert response.json()["message"] == "Comment updated successfully"
    assert response.json()["data"] == {
        "id": "02bb30ec-c793-463f-a2ea-d83edd157738",
        "comment": "This is a very nice post",
        "created_at": "2024-08-22T23:59:25.816336+01:00",
        "updated_at": "2024-08-23T11:59:25.816336+01:00",
        "post_id": "ac3d6659-8f67-4a67-b690-9f77fab7e6e3",
        "user": {
            "id": "02bb30ec-c793-463f-a2ea-d83edd156628",
            "username": "izzyjosh",
            "profile_picture": {
                "id": "02bb30ec-c793-463f-a2ea-d83edd159938",
                "image": "user/profile_picture.img",
            },
        },
    }


def test_update_comment_post_not_found(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_update_comment_post_not_found_side_effect,
):

    response = client.patch(
        endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        json={"comment": "Test update comment"},
    )

    data = response.json()
    assert response.status_code == 404
    assert data["status_code"] == 404
    assert data["message"] == "Post not found"


def test_update_comment_no_content(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_update_comment_no_content_side_effect,
):

    response = client.patch(
        endpoint, headers={"Authorization": f"Bearer {access_token}"}, json={}
    )

    assert response.status_code == 400
    assert response.json()["status_code"] == 400
    assert response.json()["message"] == "Please provide comment content"


def test_unauthenticated_user(mock_db_session: Session):

    response = client.patch(endpoint, json={})

    assert response.status_code == 401
