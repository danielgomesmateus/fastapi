from fastapi import APIRouter, HTTPException, status
from fastapi_sqlalchemy import db

from typing import List

from app.api.client.models import Client as ModelClient
from app.api.client.schemas import ClientCreate as SchemaClientCreate
from app.api.client.schemas import Client as SchemaClients


router = APIRouter()


@router.get("/", response_model=List[SchemaClients], status_code=status.HTTP_200_OK)
def get_clients():
    clients = db.session.query(ModelClient).offset(0).limit(20).all()
    return clients


@router.get("/{id_client}", response_model=SchemaClients, status_code=status.HTTP_200_OK)
def get_client_by_id(id_client: int):
    client = db.session.query(ModelClient).filter(ModelClient.id == id_client).first()

    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client


@router.post("/", response_model=SchemaClients, status_code=status.HTTP_201_CREATED)
def create(client: SchemaClientCreate):
    create_client = ModelClient(name=client.name, last_name=client.last_name, email=client.email)

    db.session.add(create_client)
    db.session.commit()
    db.session.refresh(create_client)
    return create_client


@router.put("/{id_client}", response_model=SchemaClients, status_code=status.HTTP_200_OK)
def update(id_client: int, client: SchemaClientCreate):
    update_client = db.session.query(ModelClient).filter(ModelClient.id == id_client).first()

    if update_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    db.session.query(ModelClient).filter(ModelClient.id == id_client).update(client)
    db.session.commit()
    db.session.refresh(update_client)
    return update_client


@router.delete("/{id_client}", response_model=SchemaClients, status_code=status.HTTP_200_OK)
def delete(id_client: int):
    delete_client = db.session.query(ModelClient).filter(ModelClient.id == id_client).first()

    if delete_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    db.session.delete(delete_client)
    db.session.commit()
