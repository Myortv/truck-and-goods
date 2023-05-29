import re

from typing import Optional

from pydantic import BaseModel, validator

from app.core.configs import settings


car_number_id = re.compile('^[1-9][0-9]{3}[A-Z]$')


class TruckBase(BaseModel):
    capacity: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @validator('capacity')
    def capacity_in_boarders(cls, v):
        if settings.MINIMUM_CAPASITY <= v <= settings.MAXIMUM_CAPASITY:
            return v
        raise ValueError(
            f'Truck capasity ({v}) is out of borders. '
            f'Make sure your capasity is in range of '
            f'[{settings.MINIMUM_CAPASITY}:{settings.MAXIMUM_CAPASITY}]'
        )


class TruckCreate(TruckBase):
    number_id: str

    @validator('number_id')
    def is_value_valid_car_number(cls, v):
        if car_number_id.match(v):
            return v
        else:
            raise ValueError(
                f'Your truck number ({v}) is invalid!'
            )


class TruckInDB(TruckCreate):
    pass


class TruckUpdate(TruckBase):
    pass
