import os

from fastapi.testclient import TestClient
from fastapi import status
from fastapi_sqlalchemy import DBSessionMiddleware

from app.main import app

client = TestClient(app)


class TestClient:
    @classmethod
    def setup_class(cls):
        app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DB_TEST_URL"))

    @classmethod
    def teardown_class(cls):
        app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DB_URL"))

    def test_get_clients(self):
        response = client.get("/client/")

        assert response.status_code == status.HTTP_200_OK


    def test_get_client_by_id_if_client_not_found(self):
        id_client = 0
        response = client.get("/client/{}".format(id_client))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Client not found"}


    def test_create_when_payload_is_valid(self):
        payload = dict(name="Luiza", last_name="Almeida", email="luiza.almeida@resale.com.br")

        response = client.post(
            "/client/",
            json=payload
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('id')


    def test_create_when_payload_is_invalid(self):
        payload = dict(name="Marcos", last_name="Silva")

        response = client.post(
            "/client/",
            json=payload
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


    def test_delete_if_client_not_found(self):
        id_client = 0

        response = client.delete(
            "/client/{}".format(id_client)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Client not found"}
