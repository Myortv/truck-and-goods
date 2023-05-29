from typing import List, Dict
from asyncpg import Connection

from app.schemas.cargo import (

)

from app.db.base import (
    DatabaseManager as DM,
    update_q,
    insert_q,
)


@DM.acquire_connection()
async def get_by_id(
    number_id: int,
    conn: Connection = None,
) -> TruckInDB:
    result = await conn.fetchrow(
        'select * from truck where number_id = $1',
        number_id,
    )
    if not result:
        return
    truck = TruckInDB(**result)
    return truck


@DM.acquire_connection()
async def update(
    number_id: int,
    truck_data: TruckUpdate,
    conn: Connection = None,
) -> TruckInDB:
    result = await conn.fetchrow(*update_q(
        truck_data,
        'truck',
        number_id=number_id,
    ))
    if not result:
        return
    truck = TruckInDB(**result)
    return truck


@DM.acquire_connection()
async def create(
    truck_data: TruckCreate,
    conn: Connection = None,
) -> TruckInDB:
    result = await conn.fetchrow(*insert_q(truck_data, 'truck'))
    if not result:
        return
    truck = TruckInDB(**result)
    return truck


@DM.acquire_connection()
async def delete(
    number_id: int,
    conn: Connection = None,
) -> TruckInDB:
    result = await conn.fetchrow(
        'delete from truck where number_id = $1 returning *',
        number_id,
    )
    if not result:
        return
    truck = TruckInDB(**result)
    return truck
