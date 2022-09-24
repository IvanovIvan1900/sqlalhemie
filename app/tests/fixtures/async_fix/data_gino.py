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

@pytest_asyncio.fixture()
async def gino_list_tack_dict_5(table_tasks,table_tasks_time_track, async_list_tack_dict_5:dict)->list[dict]:
    stmt = insert(table_tasks).values(async_list_tack_dict_5["tasks"])
    result = await stmt.gino.all()

    stmt = insert(table_tasks_time_track).values(async_list_tack_dict_5["time_tracks"])
    result = await stmt.gino.all()

    return async_list_tack_dict_5

@pytest_asyncio.fixture()
async def gino_list_files_dict(table_files, async_file_tree:list[dict])->list[dict]:
    stmt = insert(table_files).values(async_file_tree)
    result = await stmt.gino.status()

    return async_file_tree


