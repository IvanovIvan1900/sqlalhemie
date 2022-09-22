import pytest
from app.tests.utility import get_dict_from_RowProxy, copy_list_update_key_in_dict
import pytest_asyncio
from sqlalchemy.dialects.postgresql import insert
from gino import Gino

@pytest_asyncio.fixture()
async def gino_list_dict_5(table_tasks, async_list_dict_5:list[dict])->list[dict]:
    stmt = insert(table_tasks).values(async_list_dict_5)
    result = await stmt.returning(table_tasks.__table__).gino.all()
    return [get_dict_from_RowProxy(elem) for elem in result]

