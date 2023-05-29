from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.core.configs import settings

from app.controllers import cargo
# from app.schemas.cargo import (
#     CargoInDB,
#     CargoCreate,
#     CargoUpdate,
#     CargoNearestTrucks,
#     CargoAllTrucks,
#     CargoFiler,
# )

router = APIRouter()



