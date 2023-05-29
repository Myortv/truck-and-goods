from typing import List

from fastapi import HTTPException
from fastapi import APIRouter, Depends, HTTPException

from app.core.configs import settings

from app.controllers import truck

from app.schemas.truck import (
    TruckInDB,
    TruckCreate,
    TruckUpdate,
)

router = APIRouter()


@router.get('/truck', response_model=TruckInDB)
async def get_truck_by_number_id(
    number_id: str,
):
    """return truck by it's car number id"""
    if result := await truck.get_by_id(number_id):
        return result
    else:
        raise HTTPException(404)


@router.put('/truck', response_model=TruckInDB)
async def update_truck(
    number_id: str,
    truck_data: TruckUpdate,
):
    if result := await truck.update(number_id, truck_data):
        return result
    else:
        raise HTTPException(404)


@router.post('/truck', response_model=TruckInDB)
async def create_truck(
    truck_data: TruckCreate,
):
    if result := await truck.create(truck_data):
        return result
    else:
        raise HTTPException(404)


@router.delete('/truck', response_model=TruckInDB)
async def delete_truck_by_number_id(
    number_id: str,
):
    if result := await truck.delete(number_id):
        return result
    else:
        raise HTTPException(404)
