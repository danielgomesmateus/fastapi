import os

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from app.api.property import controllers as property_controller
from app.api.core import controllers as core_controller
from app.api.client import controllers as client_controller
from app.api.proposal import controllers as proposal_controller

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DB_URL"))

app.include_router(core_controller.router, tags=["Início"])
app.include_router(client_controller.router, prefix="/client", tags=["Cliente"])
app.include_router(property_controller.router_real_estate, prefix="/real-estate", tags=["Imobiliária"])
app.include_router(property_controller.router_property, prefix="/property", tags=["Imóveis"])
app.include_router(proposal_controller.router_proposal, prefix="/proposal", tags=["Propostas"])
