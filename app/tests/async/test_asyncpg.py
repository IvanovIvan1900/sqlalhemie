from operator import itemgetter

import pytest
from pytest_dictsdiff import check_objects
from sqlalchemy import literal_column, update
from sqlalchemy.dialects.postgresql import insert


from app.tests.utility import get_dict_from_record

pytestmark = pytest.mark.usefixtures("clear_db_async_pg")

class TestSimpleQuery():

    @pytest.mark.asyncio
    async def test_insert(self, asyncpg_table_tasks, async_connection, async_list_dict_5:list[dict])->None:
        # for elem in async_list_dict_5:
        # query = insert(asyncpg_table_tasks).values(async_list_dict_5).returning(literal_column('*'))
        query = insert(asyncpg_table_tasks).values(async_list_dict_5).returning(asyncpg_table_tasks.c.task_name, asyncpg_table_tasks.c.Num_of_executors)
        result = await async_connection.fetch(query)
        list_from_db = [get_dict_from_record(elem) for elem in result]
        func_sort = itemgetter("task_name")
        for elem_etalon, elem_db in zip(sorted(async_list_dict_5, key=func_sort), sorted(list_from_db, key=func_sort)):
            assert check_objects(elem_etalon, elem_db)

    @pytest.mark.asyncio
    async def test_update_return_all_column(self, asyncpg_table_tasks, async_connection, asyncpg_db_list_dict_5:list[dict])->None:
        elem_update = asyncpg_db_list_dict_5[0]
        elem_update["Num_of_executors"] = elem_update["Num_of_executors"]+5
        query = update(asyncpg_table_tasks).values(elem_update). \
                    where(asyncpg_table_tasks.c.task_id == elem_update["task_id"]).returning(literal_column("*"))

        result = await async_connection.fetchrow(query)
        result_db = get_dict_from_record(result)
        assert check_objects(elem_update, result_db)

