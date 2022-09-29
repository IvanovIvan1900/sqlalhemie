from operator import itemgetter

import pytest
from pytest_dictsdiff import check_objects
from sqlalchemy import column, literal_column, update, select, text
from sqlalchemy.dialects.postgresql import insert
from asyncpgsa import pg

from app.tests.utility import get_dict_from_record
from asyncpg import Record

pytestmark = pytest.mark.usefixtures("clear_db_async_pg")

class TestSimpleQuery():

    @pytest.mark.asyncio
    async def test_insert_many(self, asyncpg_table_tasks, async_connection, async_list_dict_5:list[dict])->None:
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

    @pytest.mark.asyncio
    async def test_select_column_name(self, asyncpg_table_tasks, async_connection, asyncpg_db_list_dict_5:list[dict])->None:
        query = select([literal_column("task_id"),column("task_name"), asyncpg_table_tasks.c.Num_of_executors]).order_by(column("task_id"))
        result_list = await async_connection.fetch(query)
        assert len(result_list) == len(asyncpg_db_list_dict_5)
        assert isinstance(result_list[0], Record)
        func_sort = itemgetter("task_id")
        for elem_etalon, elem_db in zip(sorted(asyncpg_db_list_dict_5, key=func_sort), (get_dict_from_record(elem) for elem in result_list)):
            assert check_objects(elem_etalon, elem_db)

    @pytest.mark.asyncio
    async def test_select_wich_cursor(self, pg_siglton_init, asyncpg_table_tasks, async_connection, asyncpg_db_list_dict_5:list[dict])->None:
        # Если мы хотим использовать курсор - надо использовать синглтон pg, предварительно его инициализировав
        stmt = asyncpg_table_tasks.select().order_by(column("task_id"))
        prefetch = 2
        iterator_etalon = iter(sorted(asyncpg_db_list_dict_5,key=itemgetter("task_id")))
        async with pg.query(stmt, prefetch=prefetch) as cursor:
            async for row in cursor:
                row_etalon = next(iterator_etalon)
                dict_db = get_dict_from_record(row)
                assert check_objects(row_etalon, dict_db)

    @pytest.mark.asyncio
    async def test_raw_query_wich_param(self, asyncpg_table_tasks, async_connection, asyncpg_db_list_dict_5:list[dict])->None:
        stmt = text("SELECT * FROM tasks WHERE task_id = ANY(:list_id)").\
                bindparams(list_id = [elem["task_id"] for elem in asyncpg_db_list_dict_5[:2]])
        result_list = await async_connection.fetch(stmt)
        assert 2 == len(result_list)
        assert isinstance(result_list[0], Record)
        func_sort = itemgetter("task_id")
        for elem_etalon, elem_db in zip(sorted(asyncpg_db_list_dict_5, key=func_sort)[:2], (get_dict_from_record(elem) for elem in result_list)):
            assert check_objects(elem_etalon, elem_db)


    @pytest.mark.asyncio
    async def test_transaction(self, async_pool, asyncpg_table_tasks, async_connection, asyncpg_db_list_dict_5:list[dict])->None:
        # Если мы хотим использовать курсор - надо использовать синглтон pg, предварительно его инициализировав
        try:
            async with async_pool.transaction() as conn:
                elem_update = asyncpg_db_list_dict_5[0]
                elem_update["Num_of_executors"] = elem_update["Num_of_executors"]+5
                query = update(asyncpg_table_tasks).values(elem_update). \
                            where(asyncpg_table_tasks.c.task_id == elem_update["task_id"])
                await conn.fetch(query)
                elem_update["Num_of_executors"] = elem_update["Num_of_executors"]-5
                raise Exception
        except:
            pass
        stmt = asyncpg_table_tasks.select().order_by(column("task_id"))
        result_list = await async_connection.fetch(stmt)
        assert len(asyncpg_db_list_dict_5) == len(result_list)
        assert isinstance(result_list[0], Record)
        func_sort = itemgetter("task_id")
        for elem_etalon, elem_db in zip(sorted(asyncpg_db_list_dict_5, key=func_sort), (get_dict_from_record(elem) for elem in result_list)):
            assert check_objects(elem_etalon, elem_db)
