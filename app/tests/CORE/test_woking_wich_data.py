import collections
from operator import itemgetter
from typing import Any

import pytest
from sqlalchemy import (Numeric, and_, cast, delete, desc, func, insert, or_,
                        select, table, text, update)
from sqlalchemy.engine.base import Connection
from sqlalchemy.exc import IntegrityError


def get_dict_from_object(result_items):
    return dict(result_items._mapping.items())


class TestInsertion():
    def test_insert_cookie_one_method(self, connection:Connection, table_cookies:table, dict_cookie_one:dict):
        ins = table_cookies.insert().values(**dict_cookie_one)
        # print(str(ins))
        result = connection.execute(ins)
        assert result.rowcount == 1

    def test_insert_cookie_two_method(self, connection:Connection, table_cookies:table, dict_cookie_one:dict):
        ins = insert(table_cookies).values(**dict_cookie_one)
        # print(str(ins))
        result = connection.execute(ins)
        assert result.rowcount == 1
        # a = 4

    def test_insert_many(self, connection:Connection ,table_cookies:table, array_of_two_cookie:list[dict]):
        ins = table_cookies.insert()
        result = connection.execute(ins, array_of_two_cookie)
        assert result.rowcount == 2
# def test_fixture(my_fixture):
#     print(my_fixture)

class TestQueryingData():

    def test_query_one(self, connection:Connection, table_cookies:table, db_cookie_one:dict, dict_cookie_one:dict):
        s = select([table_cookies])
        result_proxy = connection.execute(s)
        results = result_proxy.fetchall()
        assert len(results) == 1
        # dict_cookie_one["cookie_id"] = results[0].cookie_id
        dict_from_db = dict(results[0]._mapping.items())
        assert dict_cookie_one == dict_from_db

    def test_query_two(self, connection:Connection, table_cookies:table, db_cookie_one:dict, dict_cookie_one:dict):
        s = table_cookies.select()
        result_proxy = connection.execute(s)
        results = result_proxy.fetchall()
        assert len(results) == 1
        # dict_cookie_one["cookie_id"] = results[0].cookie_id
        dict_from_db = dict(results[0]._mapping.items())
        assert dict_cookie_one == dict_from_db

    def test_result_proxy(self, connection:Connection, table_cookies:table, db_cookie_array_two_element:list[dict]):
        # sourcery skip: dict-comprehension
        s = table_cookies.select()
        result_proxy = connection.execute(s)
        results = result_proxy.fetchall()
        assert len(results) == 2

        first_row = results[0]
        column_by_index = first_row[0]
        column_by_name = first_row.cookie_name
        columnt_by_table_column = first_row[table_cookies.c.cookie_name]

        # так можно получить колонки и значени колонки в записи.
        dic_of_element = {}
        for column_name  in first_row.keys():
            dic_of_element[column_name] = first_row[column_name]
        a = 4

    def test_query_concrete_column(self, connection:Connection, table_cookies:table, db_cookie_one:dict):
        select_query = select([table_cookies.c.cookie_name, table_cookies.c.quantity])
        resutl_proxy = connection.execute(select_query)
        assert len(resutl_proxy.keys()) == 2
        print(resutl_proxy.keys())
        result = resutl_proxy.first()

    def test_query_order(self, connection:Connection, table_cookies:table, db_cookie_one:table, db_cookie_array_two_element:list[dict]):
        select_query = select([table_cookies.c.cookie_name, table_cookies.c.quantity])
        select_query = select_query.order_by(table_cookies.c.quantity)
        resutl_proxy = connection.execute(select_query)
        prev_quantity = 0
        for elem in resutl_proxy:
            assert prev_quantity <= elem.quantity
            prev_quantity = elem.quantity

    def test_query_order_desc(self, connection:Connection, table_cookies:table, db_cookie_one:dict, db_cookie_array_two_element:list[dict]):
        select_query = select([table_cookies.c.cookie_name, table_cookies.c.quantity])
        select_query = select_query.order_by(desc(table_cookies.c.quantity))
        resutl_proxy = connection.execute(select_query)
        prev_quantity = 10000000
        for elem in resutl_proxy:
            assert prev_quantity >= elem.quantity
            prev_quantity = elem.quantity

    def test_query_func(self, connection:Connection, table_cookies:table, db_cookie_one:dict, db_cookie_array_two_element:list[dict]):
        select_query = select([func.count(table_cookies.c.cookie_name).label('inventory_count')])
        resutl_proxy = connection.execute(select_query)
        result = resutl_proxy.first()
        assert 'inventory_count' in  result.keys()

    def test_query_filter(self, connection:Connection, table_cookies:table, db_cookie_one:dict, db_cookie_array_two_element:list[dict]):
        select_query = select([table_cookies]).where(table_cookies.c.cookie_name.like('%chocolate%'))
        resutl_proxy = connection.execute(select_query)
        for record in resutl_proxy.fetchall():
            assert 'chocolate' in record.cookie_name

    def test_query_operator(self, connection:Connection, table_cookies:table, db_cookie_one:dict, db_cookie_array_two_element:list[dict]):
        select_query = select([table_cookies.c.cookie_name, ('SKU-' + table_cookies.c.cookie_sku).label('sku'), table_cookies.c.cookie_sku])
        for row in connection.execute(select_query).fetchall():
            assert f'SKU-{row.cookie_sku}' == row.sku

    def test_query_operator_cast(self, connection:Connection, table_cookies:table, db_cookie_one:dict, db_cookie_array_two_element:list[dict]):
        select_query = select([table_cookies.c.cookie_name,
                    cast((table_cookies.c.quantity * table_cookies.c.unit_cost),
                    Numeric(12,2)).label('inv_cost'), table_cookies.c.quantity, table_cookies.c.unit_cost])
        for row in connection.execute(select_query).fetchall():
            assert row.inv_cost == row.quantity * row.unit_cost

    def test_query_where_and(self, connection:Connection, table_cookies:table, db_cookie_one:dict, db_cookie_array_two_element:list[dict]):
        select_query = select([table_cookies]).where(
                and_(
                table_cookies.c.quantity > 23,
                table_cookies.c.unit_cost < 0.40
                )
                )
        for row in connection.execute(select_query).fetchall():
            assert row.quantity > 23 and row.unit_cost < 0.40

    def test_query_where_or(self, connection:Connection, table_cookies:table, db_cookie_one:dict, db_cookie_array_two_element:list[dict]):
        select_query = select([table_cookies]).where(
                    or_(
                    table_cookies.c.quantity.between(10, 50),
                    table_cookies.c.cookie_name.contains('chip')
                    )
                    )
        for row in connection.execute(select_query).fetchall():
            assert 'chip' in row.cookie_name or (row.quantity > 10 and row.quantity < 50)

class TestUpdateData():
    def test_update(self, connection:Connection, table_cookies:table, db_cookie_one:dict):
        select_query = table_cookies.select()
        result_proxy = connection.execute(select_query)
        results = result_proxy.fetchall()
        assert len(results) == 1

        dict_before = get_dict_from_object(results[0])

        update_query = update(table_cookies).where(table_cookies.c.cookie_name == dict_before.get("cookie_name"))
        update_query = update_query.values(quantity=(table_cookies.c.quantity + 120))
        result = connection.execute(update_query)
        assert result.rowcount==1

        dict_before["quantity"] = dict_before["quantity"] + 120
        result_proxy = connection.execute(select_query)
        results = result_proxy.fetchall()
        assert len(results) == 1
        dict_after = get_dict_from_object(results[0])
        
        assert dict_before == dict_after

class TestDeletingData():
    def test_delete(self, connection:Connection, table_cookies:table, db_cookie_one:dict, db_cookie_array_two_element:list[dict]):
        select_query = table_cookies.select()
        result_proxy = connection.execute(select_query)
        results = result_proxy.fetchall()
        assert len(results) == 3

        list_of_id_before = [elem.cookie_id for elem in results]

        delete_query = delete(table_cookies).where(table_cookies.c.cookie_name == results[0].cookie_name)
        result = connection.execute(delete_query)
        assert result.rowcount == 1

        select_query = table_cookies.select()
        result_proxy = connection.execute(select_query)
        results = result_proxy.fetchall()
        assert len(results) == 2

        list_of_id_after = [elem.cookie_id for elem in results]

        del list_of_id_before[0]

        assert list_of_id_before == list_of_id_after

class TestJoinData():
    def test_join(self, connection:Connection, db_orders_all:list[dict], table_orders:table, table_users:table, table_cookies:table, table_line_items:table, db_user_one:dict):
        user_id_filter = db_user_one["user_id"]
        etalon_array_of_dict = []
        for order in db_orders_all:
            if order["user_id"] == user_id_filter:
                for line_item in order["line_items"]:
                    etalon_array_of_dict.append({
                        "order_id":order["order_id"],
                        "username":db_user_one["username"],
                        "phone":db_user_one["phone"],
                        "cookie_id":line_item["cookie_id"],
                        "quantity":line_item["quantity"],
                        "extended_cost":line_item["extended_cost"],
                        "line_items_id":line_item["line_items_id"],
                    })

        columns = [table_orders.c.order_id, table_users.c.username, table_users.c.phone,
            table_cookies.c.cookie_id, table_line_items.c.quantity,
            table_line_items.c.extended_cost, table_line_items.c.line_items_id]
        cookiemon_orders = select(columns)
        cookiemon_orders = cookiemon_orders.select_from(table_orders.join(table_users).join(
        table_line_items).join(table_cookies)).where(table_users.c.user_id == user_id_filter)
        result = connection.execute(cookiemon_orders).fetchall()
        array_db_data = [get_dict_from_object(elem) for elem in result]
        assert len(etalon_array_of_dict) == len(array_db_data)
        etalon_array_of_dict.sort(key=itemgetter("order_id", "line_items_id"))
        array_db_data.sort(key=itemgetter("order_id", "line_items_id"))
        for etalon, db in zip(etalon_array_of_dict, array_db_data):
            assert etalon == db


    def test_outer_join(self, connection:Connection, db_orders_all:list[dict], table_orders:table, table_users:table, table_cookies:table, table_line_items:table, db_user_one:dict):
        # It is also useful to get a count of orders by all users, including those who do not have
        # any present orders. To do this, we have to use the outerjoin() method, and it
        # requires a bit more care in the ordering of the join, as the table we use the outer
        # join() method on will be the one from which all results are returned 
        columns = [table_users.c.user_id, func.count(table_orders.c.order_id)]
        all_orders = select(columns)
        all_orders = all_orders.select_from(table_users.outerjoin(table_orders))
        all_orders = all_orders.group_by(table_users.c.username).order_by(table_users.c.user_id)
        result = connection.execute(all_orders).fetchall()
        
        dict_etalon:dict[Any, Any] = collections.defaultdict(int)
        for order in db_orders_all:
            dict_etalon[order["user_id"]] = dict_etalon[order["user_id"]] + 1
        
        dict_db = collections.defaultdict(int)
        for elem in result:
            dict_db[elem.user_id] = elem.count
        for key_etalon, key_db in zip(sorted(dict_etalon.keys()), sorted(dict_db.keys())):
            assert key_etalon == key_db
            assert dict_etalon[key_etalon] == dict_db[key_db]

class TestAliasData():
    def test_alias_simple(self, connection:Connection, table_emploee:table, db_employer_array_five:list[dict]):
        # Now suppose we want to select all the employees managed by an employee named
        # Fred.
        array_dic_etalon:list[str] = []
        for elem in db_employer_array_five:
            if elem["manager_id"] == db_employer_array_five[0]["id"]:
                array_dic_etalon.append(elem["name"])
        manager = table_emploee.alias('mgr')
        sel_q = select([table_emploee.c.name],
            and_(table_emploee.c.manager_id==manager.c.id,
                manager.c.name==db_employer_array_five[0]["name"]))
        result = connection.execute(sel_q).fetchall()
        array_dic_db:list[str] = []
        for elem_db in result:
            array_dic_db.append(elem_db.name)
        
        assert len(array_dic_etalon) == len(array_dic_db)
        for elem_etalon, elem_db in zip(array_dic_etalon, array_dic_db):
            assert elem_etalon == elem_db

class TestGroupData():
    def test_group_simple(self, connection:Connection, db_orders_all:list[dict], table_users:table, table_orders:table):
        array_dict_etalon:dict[Any, Any] = collections.defaultdict(int)
        for elem in db_orders_all:
            array_dict_etalon[elem.get("user_id")] = array_dict_etalon[elem.get("user_id")] + 1
        
        columns = [table_users.c.user_id, func.count(table_orders.c.order_id).label("count_order")]
        all_orders = select(columns)
        all_orders = all_orders.select_from(table_users.outerjoin(table_orders))
        all_orders = all_orders.group_by(table_users.c.user_id)
        result = connection.execute(all_orders).fetchall()
        
        array_dict_db = collections.defaultdict(int)
        for elem_db in result:
            array_dict_db[elem_db.user_id] = elem_db.count_order

        for key_etalon, key_db in zip(sorted(array_dict_etalon.keys()), sorted(array_dict_etalon.keys())):
            assert key_etalon == key_db
            assert array_dict_etalon[key_etalon] == array_dict_db[key_db]

class TestRawQuery():
    def test_raw_query_one(self, connection:Connection, table_cookies:table, db_cookie_one:dict):
        result = connection.execute("select * from cookies").fetchall()
        assert len(result) == 1
        object_out = get_dict_from_object(result[0])
        assert object_out == db_cookie_one

    def test_raw_query_partial(self, connection:Connection, table_cookies:table, db_cookie_array_two_element:list[dict]):
        stmt = select([table_cookies]).where(text("cookie_name='peanut butter'"))
        result = connection.execute(stmt).fetchall()
        assert len(result) == 1
        for elem in db_cookie_array_two_element:
            if elem.get('cookie_name') == 'peanut butter':
                object_out_dict = get_dict_from_object(result[0])
                assert elem == object_out_dict
                break

class TestException():
    def test_exception_attribut_error(self, connection:Connection, table_users:table, db_user_one:dict):
        with pytest.raises(AttributeError):
            sel_query = select([table_users.c.username])
            result = connection.execute(sel_query)
            for elem in result:
                passw = elem.password

    def test_exception_itegrity_error(self, connection:Connection, table_users:table, db_user_one:dict):
        with pytest.raises(IntegrityError):
            ins_query = insert(table_users).values(**db_user_one)
            result = connection.execute(ins_query)

class TestTransaction():
    connection:Connection = None
    table_line_items:table = None
    table_cookies:table = None
    table_orders:table = None

    def ship_it(self, order_id:int):
        success = True
        s = select([self.table_line_items.c.cookie_id, self.table_line_items.c.quantity])
        s = s.where(self.table_line_items.c.order_id == order_id)
        transaction = self.connection.begin()
        cookies_to_ship = self.connection.execute(s).fetchall()
        try:
            for cookie in cookies_to_ship:
                u = update(self.table_cookies).where(self.table_cookies.c.cookie_id == cookie.cookie_id)
                u = u.values(quantity = self.table_cookies.c.quantity-cookie.quantity)
                result = self.connection.execute(u)
            u = update(self.table_orders).where(self.table_orders.c.order_id == order_id)
            u = u.values(shipped=True)
            result = self.connection.execute(u)
            transaction.commit()
        except IntegrityError as error:
            success = False
            transaction.rollback()

        return success
    
    def test_transaction_succes(self, connection:Connection, db_orders_succes:dict, db_cookie_one:dict, table_line_items:table, table_cookies:table, table_orders:table):
        """this is order succes and commit transaction

        Args:
        """
        self.connection = connection
        self.table_line_items = table_line_items
        self.table_cookies = table_cookies
        self.table_orders = table_orders
        self.ship_it(db_orders_succes.get("order_id"))
        sel_query = select([table_cookies]).where(table_cookies.c.cookie_id == db_orders_succes["line_items"][0]["cookie_id"])
        result = connection.execute(sel_query).fetchall()
        assert result[0]["quantity"] == 1

    def test_transaction_not_succes(self, connection:Connection, db_orders_not_succes:dict, db_cookie_one:dict, table_line_items:table, table_cookies:table, table_orders:table):
        """this is order succes and rollback transaction

        Args:
        """
        self.connection = connection
        self.table_line_items = table_line_items
        self.table_cookies = table_cookies
        self.table_orders = table_orders
        self.ship_it(db_orders_not_succes.get("order_id"))
        sel_query = select([table_cookies]).where(table_cookies.c.cookie_id == db_orders_not_succes["line_items"][0]["cookie_id"])
        result = connection.execute(sel_query).fetchall()
        assert result[0]["quantity"] == db_cookie_one["quantity"]