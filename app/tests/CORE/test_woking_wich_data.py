from operator import attrgetter, itemgetter
import pytest
from sqlalchemy import Numeric, and_, cast, delete, desc, func, insert, or_, select, update


def get_dict_from_object(results_item):
    return {key:value for key, value in results_item._mapping.items() }

class TestInsertion():
    def test_insert_cookie_one_method(self, connection, table_cookies, dict_cookie_one):
        ins = table_cookies.insert().values(**dict_cookie_one)
        # print(str(ins))
        result = connection.execute(ins)
        assert result.rowcount == 1

    def test_insert_cookie_two_method(self, connection, table_cookies, dict_cookie_one):
        ins = insert(table_cookies).values(**dict_cookie_one)
        # print(str(ins))
        result = connection.execute(ins)
        assert result.rowcount == 1
        # a = 4

    def test_insert_many(self, connection ,table_cookies, array_of_two_cookie):
        ins = table_cookies.insert()
        result = connection.execute(ins, array_of_two_cookie)
        assert result.rowcount == 2
# def test_fixture(my_fixture):
#     print(my_fixture)

class TestQueryingData():

    def test_query_one(self, connection, table_cookies, db_cookie_one, dict_cookie_one):
        s = select([table_cookies])
        result_proxy = connection.execute(s)
        results = result_proxy.fetchall()
        assert len(results) == 1
        # dict_cookie_one["cookie_id"] = results[0].cookie_id
        dict_from_db = dict(results[0]._mapping.items())
        assert dict_cookie_one == dict_from_db

    def test_query_two(self, connection, table_cookies, db_cookie_one, dict_cookie_one):
        s = table_cookies.select()
        result_proxy = connection.execute(s)
        results = result_proxy.fetchall()
        assert len(results) == 1
        # dict_cookie_one["cookie_id"] = results[0].cookie_id
        dict_from_db = dict(results[0]._mapping.items())
        assert dict_cookie_one == dict_from_db

    def test_result_proxy(self, connection, table_cookies, db_cookie_array_two_element):
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

    def test_query_concrete_column(self, connection, table_cookies, db_cookie_one):
        select_query = select([table_cookies.c.cookie_name, table_cookies.c.quantity])
        resutl_proxy = connection.execute(select_query)
        assert len(resutl_proxy.keys()) == 2
        print(resutl_proxy.keys())
        result = resutl_proxy.first()

    def test_query_order(self, connection, table_cookies, db_cookie_one, db_cookie_array_two_element):
        select_query = select([table_cookies.c.cookie_name, table_cookies.c.quantity])
        select_query = select_query.order_by(table_cookies.c.quantity)
        resutl_proxy = connection.execute(select_query)
        prev_quantity = 0
        for elem in resutl_proxy:
            assert prev_quantity <= elem.quantity
            prev_quantity = elem.quantity

    def test_query_order_desc(self, connection, table_cookies, db_cookie_one, db_cookie_array_two_element):
        select_query = select([table_cookies.c.cookie_name, table_cookies.c.quantity])
        select_query = select_query.order_by(desc(table_cookies.c.quantity))
        resutl_proxy = connection.execute(select_query)
        prev_quantity = 10000000
        for elem in resutl_proxy:
            assert prev_quantity >= elem.quantity
            prev_quantity = elem.quantity

    def test_query_func(self, connection, table_cookies, db_cookie_one, db_cookie_array_two_element):
        select_query = select([func.count(table_cookies.c.cookie_name).label('inventory_count')])
        resutl_proxy = connection.execute(select_query)
        result = resutl_proxy.first()
        assert 'inventory_count' in  result.keys()

    def test_query_filter(self, connection, table_cookies, db_cookie_one, db_cookie_array_two_element):
        select_query = select([table_cookies]).where(table_cookies.c.cookie_name.like('%chocolate%'))
        resutl_proxy = connection.execute(select_query)
        for record in resutl_proxy.fetchall():
            assert 'chocolate' in record.cookie_name

    def test_query_operator(self, connection, table_cookies, db_cookie_one, db_cookie_array_two_element):
        select_query = select([table_cookies.c.cookie_name, ('SKU-' + table_cookies.c.cookie_sku).label('sku'), table_cookies.c.cookie_sku])
        for row in connection.execute(select_query).fetchall():
            assert f'SKU-{row.cookie_sku}' == row.sku

    def test_query_operator_cast(self, connection, table_cookies, db_cookie_one, db_cookie_array_two_element):
        select_query = select([table_cookies.c.cookie_name,
                    cast((table_cookies.c.quantity * table_cookies.c.unit_cost),
                    Numeric(12,2)).label('inv_cost'), table_cookies.c.quantity, table_cookies.c.unit_cost])
        for row in connection.execute(select_query).fetchall():
            assert row.inv_cost == row.quantity * row.unit_cost

    def test_query_where_and(self, connection, table_cookies, db_cookie_one, db_cookie_array_two_element):
        select_query = select([table_cookies]).where(
                and_(
                table_cookies.c.quantity > 23,
                table_cookies.c.unit_cost < 0.40
                )
                )
        for row in connection.execute(select_query).fetchall():
            assert row.quantity > 23 and row.unit_cost < 0.40

    def test_query_where_or(self, connection, table_cookies, db_cookie_one, db_cookie_array_two_element):
        select_query = select([table_cookies]).where(
                    or_(
                    table_cookies.c.quantity.between(10, 50),
                    table_cookies.c.cookie_name.contains('chip')
                    )
                    )
        for row in connection.execute(select_query).fetchall():
            assert 'chip' in row.cookie_name or (row.quantity > 10 and row.quantity < 50)

class TestUpdateData():
    def test_update(self, connection, table_cookies, db_cookie_one):
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
    def test_delete(self, connection, table_cookies, db_cookie_one, db_cookie_array_two_element):
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
    def test_join(self, connection, db_orders_all, table_orders, table_users, table_cookies, table_line_items, db_user_one):
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
        array_db_data = []
        for elem in result:
            array_db_data.append(get_dict_from_object(elem))
        assert len(etalon_array_of_dict) == len(array_db_data)
        etalon_array_of_dict.sort(key=itemgetter("order_id", "line_items_id"))
        array_db_data.sort(key=itemgetter("order_id", "line_items_id"))
        for etalon, db in zip(etalon_array_of_dict, array_db_data):
            assert etalon == db


