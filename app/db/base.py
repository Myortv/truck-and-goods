from fastapi import HTTPException

from pydantic import ValidationError, BaseModel

import asyncpg

import logging

from app.utils.exceptions import raise_exception


class DatabaseManager:
    POOL: asyncpg.Pool = None

    @classmethod
    async def start(
        cls,
        database: str,
        user: str,
        password: str,
        host: str,
    ) -> None:
        cls.POOL = await asyncpg.create_pool(
            database=database,
            user=user,
            password=password,
            host=host,
        )
        logging.info(f'DatabaseManager create postgres pool on:{cls.POOL}')

    @classmethod
    async def stop(cls):
        await cls.POOL.close()
        logging.info(f'DatabaseManager stops postgres pool on:{cls.POOL}')



    @classmethod
    def acquire_connection(cls):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                async with cls.POOL.acquire() as conn:
                    try:
                        result = await func(*args, conn=conn, **kwargs)
                        return result
                    except ValidationError as e:
                        raise_exception(e)
                    except HTTPException as e:
                        raise_exception(e)
                    except Exception as e:
                        logging.warning(e)
            return wrapper
        return decorator


def unpack_data(data: dict | BaseModel):
    if isinstance(data, dict):
        fields = list(data.keys())
        values = list(data.values())
        return fields, values
    fields = list(data.__dict__.keys())
    values = list(data.__dict__.values())
    assert len(fields) == len(values)
    return (fields, values)


def generate_placeholder(
    data: dict | BaseModel,
    i: int = 0
):
    pair = []
    values_out = []
    fields, values = unpack_data(data)
    for j, field in enumerate(fields):
        if values[j] is not None:
            i += 1
            pair.append(f' {field} = ${i} ')
            values_out.append(values[j])
    return pair, values_out


def throwout_nulls(data: dict | BaseModel):
    fields, values = unpack_data(data)
    fields_out = []
    values_out = []
    for i, value in enumerate(values):
        if value:
            values_out.append(value)
            fields_out.append(fields[i])
    return fields_out, values_out


def update_q(data, datatable, **conditions):
    placeholder, values = generate_placeholder(data)
    condition, cond_values = generate_placeholder(conditions, len(values))
    query = (
        f'UPDATE '
        f'{datatable} '
        f'set {", ".join(placeholder)} '
        f'where {" AND ".join(condition)} '
        f'returning *')
    return (query, *values, *cond_values)


def insert_q(data, datatable):
    fields, values = throwout_nulls(data)
    query = (
        f'INSERT INTO '
        f'    {datatable} '
        f'    ({", ".join(fields)}) '
        f'VALUES '
        f'    ({", ".join( [ f"${i+1}" for i in range(0, len(values)) ])}) '
        f'RETURNING *'
    )
    return query, *values

