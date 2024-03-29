from typing import Any, List
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import table
# from sqlalchemy.orm.decl_api import DeclarativeMeta

@pytest.fixture(scope="function")
def db_cookie_one(connection, table_cookies, dict_cookie_one):
    ins = table_cookies.insert()
    dict_cookie_one.pop("cookie_id", None)
    result = connection.execute(ins, [dict_cookie_one])
    dict_cookie_one["cookie_id"] = result.inserted_primary_key[0]

    return dict_cookie_one

@pytest.fixture(scope="function")
def db_orm_cookie_one(session:Session, table_orm_cookies, dict_cookie_one:dict):
    cookie = table_orm_cookies(**dict_cookie_one)
    session.add(cookie)
    session.commit()
    return cookie

@pytest.fixture(scope="function")
def db_cookie_array_two_element(connection, table_cookies, array_of_two_cookie):
    for dict_cookie_one in array_of_two_cookie:
        ins = table_cookies.insert()
        dict_cookie_one.pop("cookie_id", None)
        result = connection.execute(ins, [dict_cookie_one])
        dict_cookie_one["cookie_id"] = result.inserted_primary_key[0]

    return array_of_two_cookie

@pytest.fixture(scope="function")
def db_orm_cookie_array_two_element(session:Session, table_orm_cookies, array_of_two_cookie:list[dict])->list[Any]:
    list_of_result:list[Any] = []
    for elem in array_of_two_cookie:
        cookie = table_orm_cookies(**elem)
        session.add(cookie)
        list_of_result.append(cookie)
    session.commit()
    return list_of_result


@pytest.fixture(scope="function")
def db_user_one(connection, table_users, dict_user_one):
    ins_q = table_users.insert()
    dict_user_one.pop("user_id", None)
    result = connection.execute(ins_q, [dict_user_one])
    dict_user_one["user_id"] = result.inserted_primary_key[0]

    return dict_user_one

@pytest.fixture(scope="function")
def db_orm_user_one(session:Session, table_orm_users, dict_user_one:dict):
    user = table_orm_users(**dict_user_one)
    session.add(user)
    session.commit()
    return user

@pytest.fixture(scope="function")
def db_user_two(connection, table_users, dict_user_two):
    dict_user_two.pop("user_id", None)
    ins_q = table_users.insert()
    result = connection.execute(ins_q, [dict_user_two])
    dict_user_two["user_id"] = result.inserted_primary_key[0]

    return dict_user_two

@pytest.fixture(scope="function")
def db_orm_user_two(session:Session, table_orm_users, dict_user_two:dict):
    user = table_orm_users(**dict_user_two)
    session.add(user)
    session.commit()
    return user

@pytest.fixture(scope="function")
def db_orders_one(connection, table_line_items , dict_orders_one, table_orders):
    dict_orders_one.pop("order_id", None)
    ins_q = table_orders.insert()
    result = connection.execute(ins_q, [dict_orders_one])
    dict_orders_one["order_id"] = result.inserted_primary_key[0]
    ins_line_q = table_line_items.insert()
    for elem in dict_orders_one["line_items"]:
        elem["order_id"] = dict_orders_one["order_id"]
        elem.pop("line_items_id", None)
        result = connection.execute(ins_line_q, [elem])
        elem["line_items_id"] = result.inserted_primary_key[0]

    return dict_orders_one

@pytest.fixture(scope="function")
def db_orm_orders_one(session: Session, table_orm_line_items , dict_orm_orders_one:dict, table_orm_orders):
    order = table_orm_orders.create_from_dict(dict_orm_orders_one, table_orm_line_items)
    session.add(order)
    session.commit()

    return order

@pytest.fixture(scope="function")
def db_orders_succes(connection, table_line_items , dict_orders_succes, table_orders):
    dict_orders_succes.pop("order_id", None)
    ins_q = table_orders.insert()
    result = connection.execute(ins_q, [dict_orders_succes])
    dict_orders_succes["order_id"] = result.inserted_primary_key[0]
    ins_line_q = table_line_items.insert()
    for elem in dict_orders_succes["line_items"]:
        elem["order_id"] = dict_orders_succes["order_id"]
        elem.pop("line_items_id", None)
        result = connection.execute(ins_line_q, [elem])
        elem["line_items_id"] = result.inserted_primary_key[0]

    return dict_orders_succes

@pytest.fixture(scope="function")
def db_orm_orders_succes(session:Session, table_orm_line_items , dict_orm_orders_succes, table_orm_orders):
    order = table_orm_orders.create_from_dict(dict_orm_orders_succes, table_orm_line_items)
    session.add(order)
    session.commit()

    return order

@pytest.fixture(scope="function")
def db_orders_not_succes(connection, table_line_items , dict_orders_not_succes, table_orders):
    dict_orders_not_succes.pop("order_id", None)
    ins_q = table_orders.insert()
    result = connection.execute(ins_q, [dict_orders_not_succes])
    dict_orders_not_succes["order_id"] = result.inserted_primary_key[0]
    ins_line_q = table_line_items.insert()
    for elem in dict_orders_not_succes["line_items"]:
        elem["order_id"] = dict_orders_not_succes["order_id"]
        elem.pop("line_items_id", None)
        result = connection.execute(ins_line_q, [elem])
        elem["line_items_id"] = result.inserted_primary_key[0]

    return dict_orders_not_succes

@pytest.fixture(scope="function")
def db_orm_orders_not_succes(session:Session, table_orm_line_items , dict_orm_orders_not_succes, table_orm_orders):
    order = table_orm_orders.create_from_dict(dict_orm_orders_not_succes, table_orm_line_items)
    session.add(order)
    session.commit()

    return order

@pytest.fixture(scope="function")
def db_orders_two(connection, table_line_items, dict_orders_two, table_orders):
    dict_orders_two.pop("order_id", None)
    ins_q = table_orders.insert()
    result = connection.execute(ins_q, [dict_orders_two])
    dict_orders_two["order_id"] = result.inserted_primary_key[0]
    ins_line_q = table_line_items.insert()
    for elem in dict_orders_two["line_items"]:
        elem["order_id"] = dict_orders_two["order_id"]
        elem.pop("line_items_id", None)
        result = connection.execute(ins_line_q, [elem])
        elem["line_items_id"] = result.inserted_primary_key[0]

    return dict_orders_two

@pytest.fixture(scope="function")
def db_orders_three(connection, table_line_items, dict_orders_tree, table_orders):
    dict_orders_tree.pop("order_id", None)
    ins_q = table_orders.insert()
    result = connection.execute(ins_q, [dict_orders_tree])
    dict_orders_tree["order_id"] = result.inserted_primary_key[0]
    ins_line_q = table_line_items.insert()
    for elem in dict_orders_tree["line_items"]:
        elem["order_id"] = dict_orders_tree["order_id"]
        elem.pop("line_items_id", None)
        result = connection.execute(ins_line_q, [elem])
        elem["line_items_id"] = result.inserted_primary_key[0]

    return dict_orders_tree

@pytest.fixture(scope="function")
def db_orders_all(connection, db_orders_one, db_orders_two, db_orders_three):
    return [db_orders_one, db_orders_two, db_orders_three]

@pytest.fixture(scope="function")
def db_employer_array_five(connection, table_emploee, dict_emploee_array_five):
    ins_q = table_emploee.insert()
    result = connection.execute(ins_q, dict_emploee_array_five)

    return dict_emploee_array_five

@pytest.fixture(scope="function")
def db_orm_employer_array_three(session:Session, table_orm_emploee, dict_orm_emploee_array_three:list[dict]):
    dic_name_to_object = {}
    for elem in dict_orm_emploee_array_three:
        dic_name_to_object[elem["name"]] = table_orm_emploee(name=elem["name"])
        session.add(dic_name_to_object[elem["name"]])
    for elem in dict_orm_emploee_array_three:
        if elem["manager_name"] is not None:
            dic_name_to_object[elem["name"]].reports.append(dic_name_to_object[elem["manager_name"]])

    session.commit()






