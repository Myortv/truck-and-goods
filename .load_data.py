import csv
import asyncpg
from asyncpg import Connection
import asyncio

from app.core.configs import settings


async def move_data_to_database(
    conn: Connection,
):
    with open('uszips.csv', 'r') as file:
        reader = csv.DictReader(file)
        # statement = await conn.prepare(
        #     '''
        #         insert into
        #             location
        #                 (zip, lat, lng, city, state_name)
        #         values
        #             ($1, $2, $3, $4, $5)
        #         on conflict
        #             do nothing
        #     '''
        # )
        for row in reader:
            await conn.execute(
                '''
                    insert into
                        location
                            (zip, lat, lng, city, state_name)
                    values
                        ($1, $2, $3, $4, $5)
                    on conflict
                        do nothing
                ''',
                row['zip'],
                float(row['lat']),
                float(row['lng']),
                row['city'],
                row['state_name'],
            )

    print("Data loaded successfully!")


async def connect():
    return await asyncpg.connect(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT
    )


async def main():
    connection = await connect()
    try:
        await move_data_to_database(connection)
    finally:
        await connection.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
