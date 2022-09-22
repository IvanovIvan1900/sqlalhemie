from operator import setitem
from typing import Any
from unittest.mock import ANY
import pytest
from gino import Gino
from sqlalchemy.dialects.postgresql import insert
import sqlalchemy
from app.tests.utility import get_dict_from_RowProxy, copy_list_update_key_in_dict, aplly_func_to_dict_and_return_dict
from pytest_dictsdiff import check_objects
from sqlalchemy.engine.result import RowProxy

pytestmark = pytest.mark.usefixtures("clear_db_gino")

class TestGinoQuery():

    @pytest.mark.asyncio
    async def test_insert_value(self, table_tasks, async_list_dict_5:list[dict], dicts_are_same)->None:
        stmt = insert(table_tasks).values(async_list_dict_5)
        result = await stmt.returning(table_tasks.__table__).gino.all()
        assert isinstance(result, list)
        assert isinstance(result[0], sqlalchemy.engine.result.RowProxy)
        list_wich_task_id = copy_list_update_key_in_dict(async_list_dict_5, {"task_id":ANY})
        assert dicts_are_same(list_wich_task_id[0] , get_dict_from_RowProxy(result[0]))

    @pytest.mark.asyncio
    async def test_create_(self, table_tasks, async_list_dict_5:list[dict], dicts_are_same)->None:
        teask_object = await table_tasks.create(**async_list_dict_5[0])
        assert isinstance(teask_object, table_tasks)
        dict_task_object = teask_object.__dict__["__values__"]
        list_wich_task_id = copy_list_update_key_in_dict(async_list_dict_5, {"task_id":ANY})
        assert check_objects(list_wich_task_id[0], dict_task_object, verbose= 1)

    @pytest.mark.asyncio
    async def test_insert_many(self, table_tasks, async_list_dict_5:list[dict])->None:
        result = await table_tasks.insert().returning(table_tasks.__table__).gino.all(async_list_dict_5)
        assert result is None
        list_result = await table_tasks.query.gino.all()
        assert len(list_result) == len(async_list_dict_5)
        assert isinstance(list_result[0], table_tasks)

    @pytest.mark.asyncio
    async def test_select_queyr(self, table_tasks, gino_list_dict_5:list[Any], async_list_dict_5:list[dict])->None:
        # all() returns all results in a list, which may be empty when the query has no result, empty but still a list.
        # first() returns the first result directly, or None if there is no result at all. There is usually some optimization behind the scene to efficiently get only the first result, instead of loading the full result set into memory.
        # one() returns exactly one result. If there is no result at all or if there are multiple results, an exception is raised.
        # one_or_none() is similar to one(), but it returns None if there is no result instead or raising an exception.
        # scalar() is similar to first(), it returns the first value of the first result. Quite convenient to just retrieve a scalar value from database, like NOW(), MAX(), COUNT() or whatever generates a single value. None is also returned when there is no result, it is up to you how to distinguish no result and the first value is NULL.
        # status() executes the query and discard all the query results at all. Instead it returns the execution status line as it is, usually a textual string. Note, there may be no optimization to only return the status without loading the results, so make your query generate nothing if you don’t want any result.
        task_list  = await table_tasks.query.order_by(table_tasks.task_id).gino.all()
        assert isinstance(task_list, list)
        assert isinstance(task_list[0], table_tasks)
        list_wich_task_id = copy_list_update_key_in_dict(async_list_dict_5, {"task_id":ANY})
        for elem_etalon, elem_db in zip(list_wich_task_id, task_list):
            assert check_objects(elem_etalon, elem_db.__dict__["__values__"], verbose= 1)

    @pytest.mark.asyncio
    async def test_select_iterate(self, db:Gino, table_tasks, gino_list_dict_5:list[Any], async_list_dict_5:list[dict])->None:
        # https://python-gino.org/docs/en/master/reference/api/gino.engine.html#gino.engine.GinoConnection.iterate
        # Cursors must work within transactions:
        async with db.transaction():
            cursor = await db.iterate(table_tasks.query)
            user = await cursor.next()
            assert isinstance(user, table_tasks)
            users = await cursor.many(3)
            assert 3 == len(users)


    @pytest.mark.asyncio
    async def test_delete_query(self, table_tasks, gino_list_dict_5:list[Any], async_list_dict_5:list[dict])->None:
        # status() executes the query and discard all the query results at all. Instead it returns the execution status line as it is, usually a textual string. Note, there may be no optimization to only return the status without loading the results, so make your query generate nothing if you don’t want any result.
        list_id_delete = [gino_list_dict_5[0]["task_id"], gino_list_dict_5[1]["task_id"]]
        result = await table_tasks.delete.where(table_tasks.task_id.in_(list_id_delete)).gino.status()
        assert f'DELETE {len(list_id_delete)}' == result[0]
        list_wich_task_id = copy_list_update_key_in_dict(async_list_dict_5[2:], {"task_id":ANY})
        list_db = await table_tasks.query.gino.all()
        assert len(list_wich_task_id) == len(list_db)
        for elem_etalon, elem_db in zip(list_wich_task_id, list_db):
            assert check_objects(elem_etalon, elem_db.__dict__["__values__"], verbose= 1)

    @pytest.mark.asyncio
    async def test_delete_query_returning(self, table_tasks, gino_list_dict_5:list[Any], async_list_dict_5:list[dict])->None:
        # all() returns all results in a list, which may be empty when the query has no result, empty but still a list.
        list_id_delete = [gino_list_dict_5[0]["task_id"], gino_list_dict_5[1]["task_id"]]
        delete_items = await table_tasks.delete.where(table_tasks.task_id.in_(list_id_delete)).returning(table_tasks.__table__).gino.all()
        assert len(list_id_delete) == len(delete_items)
        list_wich_task_id = copy_list_update_key_in_dict(async_list_dict_5[:2], {"task_id":ANY})
        for elem_etalon, elem_db in zip(list_wich_task_id, delete_items):
            assert check_objects(elem_etalon, elem_db.__dict__["__values__"], verbose= 1)

    @pytest.mark.asyncio
    async def test_update_query(self, table_tasks, gino_list_dict_5:list[Any], async_list_dict_5:list[dict])->None:
        list_of_id = [gino_list_dict_5[0]["task_id"], gino_list_dict_5[1]["task_id"]]
        task_list = table_tasks.update.values(Num_of_executors = table_tasks.Num_of_executors +5).where(table_tasks.task_id.in_(list_of_id))
        result_list = await task_list.returning(table_tasks.task_name, table_tasks.Num_of_executors).gino.all()
        assert isinstance(result_list[0], table_tasks)
        list_etalon = async_list_dict_5[:2]
        func_input = (lambda x: setitem(x, "Num_of_executors", x["Num_of_executors"] +5))
        list_etalon = [aplly_func_to_dict_and_return_dict(func=func_input, dict_input=elem) for elem in list_etalon]
        assert len(list_etalon) == len(result_list)

        for elem_etalon, elem_db in zip(list_etalon, result_list):
            assert check_objects(elem_etalon, elem_db.__dict__["__values__"], verbose= 1)

    @pytest.mark.asyncio
    async def test_raw_query_get_first(self, db:Gino, table_tasks, gino_list_dict_5:list[Any], async_list_dict_5:list[dict])->None:
        # https://github.com/python-gino/gino/blob/83e60e80e43f7714a626590c3c61385c735457bc/tests/test_crud.py
        #
        # read Using Textual SQL
        # https://docs.sqlalchemy.org/en/14/core/tutorial.html
        engine = db.bind
        u2 = await engine.first(
                db.text("SELECT * FROM tasks WHERE task_id = :uid")
                .bindparams(uid=gino_list_dict_5[0]["task_id"])
                .columns(*table_tasks)
                .execution_options(model=table_tasks)
            )
        assert isinstance(u2, table_tasks)
        assert check_objects(gino_list_dict_5[0], u2.__dict__["__values__"])

    @pytest.mark.asyncio
    async def test_raw_query_get_first(self, db:Gino, table_tasks, gino_list_dict_5:list[Any], async_list_dict_5:list[dict])->None:
        # https://github.com/python-gino/gino/blob/83e60e80e43f7714a626590c3c61385c735457bc/tests/test_crud.py
        sql_exp = db.text("""SELECT * FROM tasks WHERE task_id = ANY (:list_uid)""")
        sql_exp = sql_exp.bindparams(sqlalchemy.bindparam('list_uid'))
        params = {
            "list_uid": [gino_list_dict_5[0]["task_id"], gino_list_dict_5[1]["task_id"]],
        }
        list_row_proxy = await db.all(sql_exp, params)
        assert isinstance(list_row_proxy, list)
        assert isinstance(list_row_proxy[0], RowProxy)
        assert check_objects(gino_list_dict_5[0], get_dict_from_RowProxy(list_row_proxy[0]))