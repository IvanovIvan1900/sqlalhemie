import collections
from operator import attrgetter, itemgetter
from typing import Any

import pytest
from sqlalchemy import (Numeric, and_, cast, delete, desc, func, insert,
                        inspect, or_, select, table, text, update)
from sqlalchemy.engine.base import Connection
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get_dict_from_object(result_items):
    return dict(result_items._mapping.items())

def get_session_state(db_object: Any) -> dict[str, bool]:
    insp = inspect(db_object)
    return {state: getattr(insp, state) for state in ['transient', 'pending', 'persistent', 'detached']}

class TestORMInsertion():
    def test_insertion_coockie_commit(self, session:Session, table_orm_cookies:table, dict_cookie_one:dict):
        coockie = table_orm_cookies(**dict_cookie_one)
        session.add(coockie)
        dict_session_state = get_session_state(coockie)
        assert dict_session_state["pending"]
        session.commit()
        assert coockie.cookie_id is not None
        dict_session_state = get_session_state(coockie)
        assert dict_session_state["persistent"]

    def test_insertion_coockie_flush(self, session:Session, table_orm_cookies:table, array_of_two_cookie:dict):
        # Notice that we used the flush() method on the session instead of commit() in
        # Example 7-2. A flush is like a commit; however, it doesn’t perform a database commit
        # and end the transaction. Because of this, the dcc and mol instances are still connected
        # to the session, and can be used to perform additional database tasks without trigger‐
        # ing additional database queries. We also issue the session.flush() statement one
        # time, even though we added multiple records into the database.
        cookie_one = table_orm_cookies(**array_of_two_cookie[0])
        cookie_two = table_orm_cookies(**array_of_two_cookie[1])
        session.add(cookie_one)
        session.add(cookie_two)
        session.flush()
        assert cookie_one.cookie_id is not None
        dict_session_state = get_session_state(cookie_one)
        assert dict_session_state["persistent"]

    def test_insertion_coockie_bulk_update(self, session:Session, table_orm_cookies:table, array_of_two_cookie:dict):
        cookie_one = table_orm_cookies(**array_of_two_cookie[0])
        cookie_two = table_orm_cookies(**array_of_two_cookie[1])
        session.bulk_save_objects([cookie_one,cookie_two])
        session.commit()
        assert cookie_one.cookie_id is  None

class TestORMQueryingData():
    def test_select(self, session: Session, table_orm_cookies:table, db_orm_cookie_array_two_element:list[dict]):
        cookies_form_db = session.query(table_orm_cookies).all()
        for elem_db, elem_fixture in zip(sorted(cookies_form_db, key=attrgetter("cookie_id")), sorted(db_orm_cookie_array_two_element, key=attrgetter("cookie_id"))):
            assert elem_db == elem_fixture

    def test_select_iterator(self, session: Session, table_orm_cookies:table, db_orm_cookie_array_two_element:list[dict]):
        for elem_db, elem_fixture in zip(session.query(table_orm_cookies), sorted(db_orm_cookie_array_two_element, key=attrgetter("cookie_id"))):
            assert elem_db == elem_fixture

    def test_select_field(self, session: Session, table_orm_cookies:table, db_orm_cookie_array_two_element:list[dict]):
        list_of_cookie_form_db = session.query(table_orm_cookies.cookie_name, table_orm_cookies.quantity).all()

        list_of_cookie_form_data = [(elem.cookie_name, elem.quantity) for elem in db_orm_cookie_array_two_element]
        for elem_db, elem_fixture in zip(sorted(list_of_cookie_form_db, key=itemgetter(0)), sorted(list_of_cookie_form_data, key=itemgetter(0))):
            assert elem_db == elem_fixture

    def test_select_orders(self, session: Session, table_orm_cookies:table, db_orm_cookie_array_two_element:list[dict]):
        max_quantiti = 9999999
        for elem in session.query(table_orm_cookies).order_by(desc(table_orm_cookies.quantity)):
            assert elem.quantity <= max_quantiti
            max_quantiti = elem.quantity

    def test_select_limit(self, session: Session, table_orm_cookies:table, db_orm_cookie_array_two_element:list[dict]):
        # return list
        query_one = session.query(table_orm_cookies).order_by(table_orm_cookies.quantity)[:1]
        assert len(query_one) == 1
        assert type(query_one) == list

        # return query result, whichout all
        query_two = session.query(table_orm_cookies).order_by(table_orm_cookies.quantity).limit(1).all()
        assert len(query_two) == 1

    def test_build_in_function_and_label(self, session: Session, table_orm_cookies:table, db_orm_cookie_array_two_element:list[dict]):
        inv_count = session.query(func.sum(table_orm_cookies.quantity)).scalar()
        inv_count_from_data = sum(elem.quantity for elem in db_orm_cookie_array_two_element)

        assert inv_count_from_data == inv_count

        rec_count = session.query(func.count(table_orm_cookies.cookie_name).label('inventory_count')).first()

        assert len(db_orm_cookie_array_two_element) == rec_count.inventory_count

    def test_filter(self, session: Session, table_orm_cookies:table, db_orm_cookie_array_two_element:list[dict]):
        for elem in session.query(table_orm_cookies).filter(table_orm_cookies.cookie_name == 'chocolate chip'):
            assert elem.cookie_name == 'chocolate chip'

    def test_operator(self, session: Session, table_orm_cookies:table, db_orm_cookie_array_two_element:list[dict]):
        list_of_cookie_form_db = session.query(table_orm_cookies.cookie_name,
                cast((table_orm_cookies.quantity * table_orm_cookies.unit_cost),
                Numeric(12,2)).label('inv_cost')).all()

        list_of_cookie_form_data = [(elem.cookie_name, elem.quantity*elem.unit_cost) for elem in db_orm_cookie_array_two_element]

        for elem_db, elem_fixture in zip(sorted(list_of_cookie_form_db, key=itemgetter(0)), sorted(list_of_cookie_form_data, key=itemgetter(0))):
            assert elem_db == elem_fixture

    def test_boolean_operators(self, session: Session, table_orm_cookies:table, db_orm_cookie_array_two_element:list[dict]):
        query = session.query(table_orm_cookies).filter(
                    or_(
                    table_orm_cookies.quantity.between(10, 50),
                    table_orm_cookies.cookie_name.contains('chip')))
        for elem in query:
            assert (elem.quantity > 10 or elem.quantity < 50) or 'chip' in elem.name

    
