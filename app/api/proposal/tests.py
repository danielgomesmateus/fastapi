import os

from fastapi.testclient import TestClient
from fastapi import status
from fastapi_sqlalchemy import DBSessionMiddleware

from app.main import app

client = TestClient(app)


class TestProposal:
    @classmethod
    def setup_class(cls):
        app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DB_TEST_URL"))

    @classmethod
    def teardown_class(cls):
        app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DB_URL"))

    def test_get_proposals(self):
        response = client.get("/proposal/")

        assert response.status_code == status.HTTP_200_OK

    def test_get_proposal_by_id_if_client_not_found(self):
        id_client = 0
        response = client.get("/proposal/{}".format(id_client))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Proposal not found"}

    def test_create_when_payload_is_valid(self):
        payload = dict(client_id=1, property_id=1)

        response = client.post(
            "/proposal/",
            json=payload
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('id')

    def test_create_when_payload_is_invalid(self):
        payload = dict(client_id=1)

        response = client.post(
            "/proposal/",
            json=payload
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_when_client_or_property_is_not_found(self):
        payload = dict(client_id=0, property_id=0)

        response = client.post(
            "/proposal/",
            json=payload
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Client or Property not found"}

    def test_delete_if_proposal_not_found(self):
        id_client = 0

        response = client.delete(
            "/proposal/{}".format(id_client)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Proposal not found"}


