import os

from fastapi.testclient import TestClient
from fastapi import status
from fastapi_sqlalchemy import DBSessionMiddleware

from app.main import app

client = TestClient(app)


class TestRealEstate:
    @classmethod
    def setup_class(cls):
        app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DB_TEST_URL"))

    @classmethod
    def teardown_class(cls):
        app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DB_URL"))

    def test_get_real_estate(self):
        response = client.get("/real-estate/")

        assert response.status_code == status.HTTP_200_OK

    def test_get_real_estate_by_id_if_real_estate_not_found(self):
        id_client = 0
        response = client.get("/real-estate/{}".format(id_client))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Real Estate not found"}

    def test_create_when_payload_is_valid(self):
        payload = dict(name="Real Corretora", address="Av. Afonso Pena")

        response = client.post(
            "/real-estate/",
            json=payload
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('id')

    def test_create_when_payload_is_invalid(self):
        payload = dict(name="Real Corretora")

        response = client.post(
            "/real-estate/",
            json=payload
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_if_real_estate_not_found(self):
        id_client = 0

        response = client.delete(
            "/real-estate/{}".format(id_client)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Real Estate not found"}


class TestProperty:
    @classmethod
    def setup_class(cls):
        app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DB_TEST_URL"))

    @classmethod
    def teardown_class(cls):
        app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DB_URL"))

    def test_get_properties(self):
        response = client.get("/property/")

        assert response.status_code == status.HTTP_200_OK

    def test_get_property_by_id_if_property_not_found(self):
        id_client = 0
        response = client.get("/property/{}".format(id_client))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Property not found"}

    def test_create_when_payload_is_valid(self):
        payload = dict(
            name="Nome do imóvel", address="Endereco do imóvel", description="Descrição do imóvel",
            characteristics="Informações do imóvel", property_type="Tipo do imóvel",
            goal="Objetivo do imóvel", real_estate_id=1
        )

        response = client.post(
            "/property/",
            json=payload
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('id')

    def test_create_when_real_estate_is_not_found(self):
        payload = dict(
            name="Nome do imóvel", address="Endereco do imóvel", description="Descrição do imóvel",
            characteristics="Informações do imóvel", property_type="Tipo do imóvel",
            goal="Objetivo do imóvel", real_estate_id=0
        )

        response = client.post(
            "/property/",
            json=payload
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Real Estate not found"}

    def test_create_when_payload_is_invalid(self):
        payload = dict(name="Casa nova", address="Av. Afonso Pena", description="Casa nova para alugar")

        response = client.post(
            "/property/",
            json=payload
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_if_property_not_found(self):
        id_client = 0

        response = client.delete(
            "/property/{}".format(id_client)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Property not found"}
