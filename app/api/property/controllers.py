from fastapi import APIRouter, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi_sqlalchemy import db

from typing import List

from app.api.property.models import Property as ModelProperty
from app.api.property.schemas import PropertyCreate as SchemaPropertyCreate
from app.api.property.schemas import Property as SchemaProperties

from app.api.property.models import RealEstate as ModelRealEstate
from app.api.property.schemas import RealEstateCreate as SchemaRealEstateCreate
from app.api.property.schemas import RealEstate as SchemaRealEstate


router_property = InferringRouter()
router_real_estate = InferringRouter()


@cbv(router_property)
class Property:
    @router_property.get("/", response_model=List[SchemaProperties], status_code=status.HTTP_200_OK)
    def get_properties(self):
        properties = db.session.query(ModelProperty).all()
        return properties


    @router_property.get("/{id_property}", response_model=SchemaProperties, status_code=status.HTTP_200_OK)
    def get_property_by_id(self, id_property: int):
        property = db.session.query(ModelProperty).filter(ModelProperty.id == id_property).first()

        if property is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
        return property


    @router_property.post("/", response_model=SchemaProperties, status_code=status.HTTP_201_CREATED)
    def create(self, property: SchemaPropertyCreate):
        if self.get_real_estate_by_id(property) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Real Estate not found")

        create_client = ModelProperty(
            name=property.name, address=property.address, description=property.description,
            characteristics=property.characteristics, property_type=property.property_type,
            goal=property.goal, real_estate_id=property.real_estate_id
        )

        db.session.add(create_client)
        db.session.commit()
        db.session.refresh(create_client)
        return create_client


    @router_property.put("/{id_property}", response_model=SchemaProperties, status_code=status.HTTP_200_OK)
    def update(self, id_property: int, property: SchemaPropertyCreate):
        update_client = db.session.query(ModelProperty).filter(ModelProperty.id == id_property).first()

        if update_client is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

        db.session.query(ModelProperty).filter(ModelProperty.id == id_property).update(property)
        db.session.commit()
        db.session.refresh(update_client)
        return update_client


    @router_property.delete("/{id_property}", response_model=SchemaProperties, status_code=status.HTTP_200_OK)
    def delete(self, id_property: int):
        delete_client = db.session.query(ModelProperty).filter(ModelProperty.id == id_property).first()

        if delete_client is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

        db.session.delete(delete_client)
        db.session.commit()

    def get_real_estate_by_id(self, property):
        real_estate = db.session.query(ModelRealEstate).filter(ModelRealEstate.id == property.real_estate_id).first()
        return real_estate


@cbv(router_real_estate)
class RealEstate:
    @router_real_estate.get("/", response_model=List[SchemaRealEstate], status_code=status.HTTP_200_OK)
    def get_real_estate(self):
        real_estate = db.session.query(ModelRealEstate).all()
        return real_estate

    @router_real_estate.get("/{id_real_estate}", response_model=SchemaRealEstate, status_code=status.HTTP_200_OK)
    def get_real_estate_by_id(self, id_real_estate: int):
        real_estate = db.session.query(ModelRealEstate).filter(ModelRealEstate.id == id_real_estate).first()

        if real_estate is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Real Estate not found")
        return real_estate

    @router_real_estate.post("/", response_model=SchemaRealEstate, status_code=status.HTTP_201_CREATED)
    def create(self, real_estate: SchemaRealEstateCreate):
        create_real_estate = ModelRealEstate(name=real_estate.name, address=real_estate.address)

        db.session.add(create_real_estate)
        db.session.commit()
        db.session.refresh(create_real_estate)
        return create_real_estate

    @router_real_estate.put("/{id_real_estate}", response_model=SchemaRealEstate, status_code=status.HTTP_200_OK)
    def update(self, id_real_estate: int, real_estate: SchemaRealEstateCreate):
        update_real_estate = db.session.query(ModelRealEstate).filter(ModelRealEstate.id == id_real_estate).first()

        if update_real_estate is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Real Estate not found")

        db.session.query(ModelRealEstate).filter(ModelRealEstate.id == id_real_estate).update(real_estate)
        db.session.commit()
        db.session.refresh(update_real_estate)
        return update_real_estate

    @router_real_estate.delete("/{id_real_estate}", response_model=SchemaRealEstate, status_code=status.HTTP_200_OK)
    def delete(self, id_real_estate: int):
        delete_client = db.session.query(ModelRealEstate).filter(ModelRealEstate.id == id_real_estate).first()

        if delete_client is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Real Estate not found")

        db.session.delete(delete_client)
        db.session.commit()
        return delete_client
