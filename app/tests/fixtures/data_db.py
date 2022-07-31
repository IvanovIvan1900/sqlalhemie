import pytest

@pytest.fixture(scope="function")
def db_cookie_one(connection, table_cookies, dict_cookie_one):
    ins = table_cookies.insert()
    dict_cookie_one.pop("cookie_id", None)
    result = connection.execute(ins, [dict_cookie_one])
    dict_cookie_one["cookie_id"] = result.inserted_primary_key.cookie_id

    return dict_cookie_one

@pytest.fixture(scope="function")
def db_cookie_array_two_element(connection, table_cookies, array_of_two_cookie):
    for dict_cookie_one in array_of_two_cookie:
        ins = table_cookies.insert()
        dict_cookie_one.pop("cookie_id", None)
        result = connection.execute(ins, [dict_cookie_one])
        dict_cookie_one["cookie_id"] = result.inserted_primary_key.cookie_id

    return array_of_two_cookie

@pytest.fixture(scope="function")
def db_user_one(connection, table_users, dict_user_one):
    ins_q = table_users.insert()
    dict_user_one.pop("user_id", None)
    result = connection.execute(ins_q, [dict_user_one])
    dict_user_one["user_id"] = result.inserted_primary_key.user_id

    return dict_user_one

@pytest.fixture(scope="function")
def db_user_two(connection, table_users, dict_user_two):
    dict_user_two.pop("user_id", None)
    ins_q = table_users.insert()
    result = connection.execute(ins_q, [dict_user_two])
    dict_user_two["user_id"] = result.inserted_primary_key.user_id

    return dict_user_two

@pytest.fixture(scope="function")
def db_orders_one(connection, table_line_items , dict_orders_one, table_orders):
    dict_orders_one.pop("order_id", None)
    ins_q = table_orders.insert()
    result = connection.execute(ins_q, [dict_orders_one])
    dict_orders_one["order_id"] = result.inserted_primary_key.order_id
    ins_line_q = table_line_items.insert()
    for elem in dict_orders_one["line_items"]:
        elem["order_id"] = dict_orders_one["order_id"]
        elem.pop("line_items_id", None)
        result = connection.execute(ins_line_q, [elem])
        elem["line_items_id"] = result.inserted_primary_key.line_items_id
    
    return dict_orders_one

@pytest.fixture(scope="function")
def db_orders_succes(connection, table_line_items , dict_orders_succes, table_orders):
    dict_orders_succes.pop("order_id", None)
    ins_q = table_orders.insert()
    result = connection.execute(ins_q, [dict_orders_succes])
    dict_orders_succes["order_id"] = result.inserted_primary_key.order_id
    ins_line_q = table_line_items.insert()
    for elem in dict_orders_succes["line_items"]:
        elem["order_id"] = dict_orders_succes["order_id"]
        elem.pop("line_items_id", None)
        result = connection.execute(ins_line_q, [elem])
        elem["line_items_id"] = result.inserted_primary_key.line_items_id
    
    return dict_orders_succes

@pytest.fixture(scope="function")
def db_orders_not_succes(connection, table_line_items , dict_orders_not_succes, table_orders):
    dict_orders_not_succes.pop("order_id", None)
    ins_q = table_orders.insert()
    result = connection.execute(ins_q, [dict_orders_not_succes])
    dict_orders_not_succes["order_id"] = result.inserted_primary_key.order_id
    ins_line_q = table_line_items.insert()
    for elem in dict_orders_not_succes["line_items"]:
        elem["order_id"] = dict_orders_not_succes["order_id"]
        elem.pop("line_items_id", None)
        result = connection.execute(ins_line_q, [elem])
        elem["line_items_id"] = result.inserted_primary_key.line_items_id
    
    return dict_orders_not_succes

@pytest.fixture(scope="function")
def db_orders_two(connection, table_line_items, dict_orders_two, table_orders):
    dict_orders_two.pop("order_id", None)
    ins_q = table_orders.insert()
    result = connection.execute(ins_q, [dict_orders_two])
    dict_orders_two["order_id"] = result.inserted_primary_key.order_id
    ins_line_q = table_line_items.insert()
    for elem in dict_orders_two["line_items"]:
        elem["order_id"] = dict_orders_two["order_id"]
        elem.pop("line_items_id", None)
        result = connection.execute(ins_line_q, [elem])
        elem["line_items_id"] = result.inserted_primary_key.line_items_id

    return dict_orders_two

@pytest.fixture(scope="function")
def db_orders_three(connection, table_line_items, dict_orders_tree, table_orders):
    dict_orders_tree.pop("order_id", None)
    ins_q = table_orders.insert()
    result = connection.execute(ins_q, [dict_orders_tree])
    dict_orders_tree["order_id"] = result.inserted_primary_key.order_id
    ins_line_q = table_line_items.insert()
    for elem in dict_orders_tree["line_items"]:
        elem["order_id"] = dict_orders_tree["order_id"]
        elem.pop("line_items_id", None)
        result = connection.execute(ins_line_q, [elem])
        elem["line_items_id"] = result.inserted_primary_key.line_items_id

    return dict_orders_tree

@pytest.fixture(scope="function")
def db_orders_all(connection, db_orders_one, db_orders_two, db_orders_three):
    return [db_orders_one, db_orders_two, db_orders_three]

@pytest.fixture(scope="function")
def db_employer_array_five(connection, table_emploee, dict_emploee_array_five):
    ins_q = table_emploee.insert()
    result = connection.execute(ins_q, dict_emploee_array_five)

    return dict_emploee_array_five