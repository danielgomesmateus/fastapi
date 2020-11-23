from fastapi import APIRouter, HTTPException, status
from fastapi_sqlalchemy import db

from typing import List

from app.api.proposal.models import Proposal as ModelProposal
from app.api.proposal.schemas import ProposalCreate as SchemaProposalcreate
from app.api.proposal.schemas import Proposal as SchemaProposals

from app.api.property.models import Property as ModelProperty
from app.api.client.models import Client as ModelClient


router = APIRouter()


@router.get("/", response_model=List[SchemaProposals], status_code=status.HTTP_200_OK)
def get_proposals():
    proposals = db.session.query(ModelProposal).all()
    return proposals


@router.get("/{id_proposal}", response_model=SchemaProposals, status_code=status.HTTP_200_OK)
def get_proposal_by_id(id_proposal: int):
    proposal = db.session.query(ModelProposal).filter(ModelProposal.id == id_proposal).first()

    if proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")
    return proposal


@router.post("/", response_model=SchemaProposals, status_code=status.HTTP_201_CREATED)
def create(proposal: SchemaProposalcreate):
    if get_client_and_property_by_id(proposal) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client or Property not found")

    create_proposal = ModelProposal(client_id=proposal.client_id, property_id=proposal.property_id)

    db.session.add(create_proposal)
    db.session.commit()
    db.session.refresh(create_proposal)
    return create_proposal


@router.put("/{id_proposal}", response_model=SchemaProposals, status_code=status.HTTP_200_OK)
def update(id_proposal: int, proposal: SchemaProposalcreate):
    update_proposal = db.session.query(ModelProposal).filter(ModelProposal.id == id_proposal).first()

    if get_client_and_property_by_id(proposal) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client or Property not found")

    if update_proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")

    db.session.query(ModelProposal).filter(ModelProposal.id == id_proposal).update(proposal)
    db.session.commit()
    db.session.refresh(update_proposal)
    return update_proposal


@router.delete("/{id_proposal}", response_model=SchemaProposals, status_code=status.HTTP_200_OK)
def delete(id_proposal: int):
    delete_proposal = db.session.query(ModelProposal).filter(ModelProposal.id == id_proposal).first()

    if delete_proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")

    db.session.delete(delete_proposal)
    db.session.commit()


def get_client_and_property_by_id(proposal):
    client = db.session.query(ModelClient).filter(ModelClient.id == proposal.client_id).first()
    _property = db.session.query(ModelProperty).filter(ModelProperty.id == proposal.property_id).first()

    return client and _property
