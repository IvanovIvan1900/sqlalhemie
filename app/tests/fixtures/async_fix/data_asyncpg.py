import pytest
from sqlalchemy import literal_column
from sqlalchemy.dialects.postgresql import insert
from app.tests.utility import get_dict_from_record
import pytest_asyncio


@pytest_asyncio.fixture()
async def asyncpg_db_list_dict_5(async_connection, asyncpg_table_tasks, async_list_dict_5:list[dict])->list[dict]:
    query = insert(asyncpg_table_tasks).values(async_list_dict_5).returning(literal_column("*"))
    result = await async_connection.fetch(query)
    return  [get_dict_from_record(elem) for elem in result]
