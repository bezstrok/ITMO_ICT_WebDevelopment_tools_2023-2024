import typing as tp
import uuid

import asyncpg
import dotenv
import psycopg2

_dsn = "postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}".format(**dotenv.dotenv_values())
_sync_connection = psycopg2.connect(_dsn)

_psycopg_statement = f"INSERT INTO users (username, hashed_password) VALUES (%s, %s)"
_asyncpg_statement = f"INSERT INTO users (username, hashed_password) VALUES ($1, $2)"


def fill_data(username: str) -> tuple[str, str]:
    password = str(uuid.uuid4())
    return f"{username}_{password[:3]}", password


async def async_insert(data: tp.Sequence[str]):
    connection = await asyncpg.connect(_dsn)
    values = list(map(fill_data, data))
    await connection.executemany(_asyncpg_statement, values)
    await connection.close()


def sync_insert(data: tp.Sequence[str]):
    cursor = _sync_connection.cursor()
    values = list(map(fill_data, data))
    cursor.executemany(_psycopg_statement, values)
    _sync_connection.commit()
    cursor.close()
