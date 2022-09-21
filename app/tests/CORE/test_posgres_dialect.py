from copy import deepcopy
from operator import itemgetter
from unittest.mock import ANY
from sqlalchemy import (Numeric, and_, cast, delete,
                        select, table, text, update)
from sqlalchemy.engine.base import Connection
from sqlalchemy.dialects.postgresql import insert
import pytest

pytestmark = pytest.mark.usefixtures("clear_db_pg")


def get_dict_from_object(result_items):
    return dict(result_items._mapping.items())

def get_dict_from_row_proxy(row):
    return {elem[0]: elem[1] for elem in row.items()}

class TestRetriviend():

    def test_insert_cookie_and_return_inserted_values(self, connection_postgres:Connection, table_cookies_postgres:table, dict_cookie_one:dict):
        ins = insert(table_cookies_postgres).values(**dict_cookie_one).returning(table_cookies_postgres.c.cookie_id, table_cookies_postgres.c.cookie_name)
        result = connection_postgres.execute(ins)
        assert result.rowcount == 1
        result_elem = next(result)
        assert (ANY, dict_cookie_one["cookie_name"]) ==  result_elem

    def test_delete_cookie_and_return(self, connection_postgres:Connection, table_cookies_postgres:table, db_cookie_array_two_element_postgres:list[dict]):
        delete_query = delete(table_cookies_postgres)
        delete_query = delete_query.where(table_cookies_postgres.c.cookie_name == db_cookie_array_two_element_postgres[0]["cookie_name"])
        delete_query = delete_query.returning(table_cookies_postgres.c.cookie_id, table_cookies_postgres.c.cookie_name)
        result = connection_postgres.execute(delete_query)
        assert result.rowcount == 1
        result_elem = next(result)
        assert (db_cookie_array_two_element_postgres[0]["cookie_id"], db_cookie_array_two_element_postgres[0]["cookie_name"]) == result_elem

class TestOnConflict():

    def test_on_conflict_do_nothing(self, connection_postgres:Connection, table_cookies_postgres:table, array_of_two_cookie:list[dict]):
        new_array = deepcopy(array_of_two_cookie)
        new_array[0]["quantity"] = new_array[0]["quantity"] + 50
        new_array[1]["quantity"] = new_array[1]["quantity"] + 50

        stmt_ins = insert(table_cookies_postgres).on_conflict_do_nothing(index_elements=['cookie_name'])

        connection_postgres.execute(stmt_ins, [array_of_two_cookie[0]])
        connection_postgres.execute(stmt_ins, new_array)

        stmt_get = select(table_cookies_postgres.c)
        returnin_values = connection_postgres.execute(stmt_get)
        returnin_array = [get_dict_from_row_proxy(elem) for elem in returnin_values]
        new_array[0]["quantity"] = new_array[0]["quantity"] - 50
        new_array[0]["cookie_id"] = ANY
        new_array[1]["cookie_id"] = ANY
        assert len(new_array) == len(returnin_array)
        for elem_etalon, elem_db in zip(sorted(new_array, key = itemgetter("cookie_name")), sorted(returnin_array, key = itemgetter("cookie_name"))):
            assert elem_etalon == elem_db

    def test_on_conflict_do_update(self, connection_postgres:Connection, table_cookies_postgres:table, array_of_two_cookie:list[dict]):
        new_array = deepcopy(array_of_two_cookie)
        new_array[0]["quantity"] = new_array[0]["quantity"] + 50
        new_array[1]["quantity"] = new_array[1]["quantity"] + 50

        stmt_ins = insert(table_cookies_postgres)
        stmt_ins = stmt_ins.on_conflict_do_update(constraint='name_constrains',
                    set_=dict(
                        quantity = stmt_ins.excluded.quantity,
                        cookie_recipe_url = stmt_ins.excluded.cookie_recipe_url,
                        cookie_sku = stmt_ins.excluded.cookie_sku,
                        unit_cost = stmt_ins.excluded.unit_cost,
                        ),
                    )
        connection_postgres.execute(stmt_ins, [array_of_two_cookie[0]])
        connection_postgres.execute(stmt_ins, new_array)

        stmt_get = select(table_cookies_postgres.c)
        returnin_values = connection_postgres.execute(stmt_get)
        returnin_array = [get_dict_from_row_proxy(elem) for elem in returnin_values]
        new_array[0]["cookie_id"] = ANY
        new_array[1]["cookie_id"] = ANY
        assert len(new_array) == len(returnin_array)
        for elem_etalon, elem_db in zip(sorted(new_array, key = itemgetter("cookie_name")), sorted(returnin_array, key = itemgetter("cookie_name"))):
            assert elem_etalon == elem_db
