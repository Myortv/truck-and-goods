from typing import Optional

from pydantic import BaseModel, validator

from app.core.configs import settings




class CargoBase(BaseModel):
    anything: int
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


class TruckInDB(TruckCreate):
    pass


class TruckUpdate(TruckBase):
    pass
