from datetime import datetime

import pytest
from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, MetaData,
                        Numeric, String, Table, create_engine, inspect)


@pytest.fixture(scope="session")
def engine():
    return  create_engine('sqlite:///:memory:')

@pytest.fixture(scope="session")
def connection(engine):
    return engine.connect()

@pytest.fixture(scope="session")
def table_line_items(engine, table_orders, table_cookies):
    metadata = MetaData(bind=engine)
    line_items = Table('line_items', metadata,
    Column('line_items_id', Integer(), primary_key=True),
    Column('order_id', ForeignKey(table_orders.c.order_id)),
    Column('cookie_id', ForeignKey(table_cookies.c.cookie_id)),
    Column('quantity', Integer()),
    Column('extended_cost', Numeric(12, 2))
    )
    metadata.create_all(engine)

    return line_items

@pytest.fixture(scope="session")
def table_orders(engine, table_users):
    metadata = MetaData(bind=engine)
    orders = Table('orders', metadata,
    Column('order_id', Integer(), primary_key=True),
    Column('user_id', ForeignKey(table_users.c.user_id)),
    Column('shipped', Boolean(), default=False)
    )
    metadata.create_all(engine)

    return orders

@pytest.fixture(scope="session")
def table_users(engine):
    metadata = MetaData(bind=engine)
    users = Table('users', metadata,
    Column('user_id', Integer(), primary_key=True),
    Column('customer_number', Integer(), autoincrement=True),
    Column('username', String(15), nullable=False, unique=True),
    Column('email_address', String(255), nullable=False),
    Column('phone', String(20), nullable=False),
    Column('password', String(25), nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
    )
    metadata.create_all(engine)

    return users

@pytest.fixture(scope="session")
def table_cookies(engine):
    metadata = MetaData(bind=engine)
    cookies = Table('cookies', metadata,
    Column('cookie_id', Integer(), primary_key=True),
    Column('cookie_name', String(50), index=True),
    Column('cookie_recipe_url', String(255)),
    Column('cookie_sku', String(55)),
    Column('quantity', Integer()),
    Column('unit_cost', Numeric(12, 2)),
    CheckConstraint('quantity >= 0', name='quantity_positive')
    )
    metadata.create_all(engine)

    return cookies

@pytest.fixture(scope="session")
def table_emploee(engine):
    metadata = MetaData(bind=engine)
    employee_table = Table(
        'employee', metadata,
        Column('id', Integer, primary_key=True),
        Column('manager_id', None, ForeignKey('employee.id')),
        Column('name', String(255)))    
    metadata.create_all(engine)

    return employee_table

@pytest.fixture(autouse=True)
def clear_db(engine):
# It may be enough to disable a foreign key checks just for the current session:
# con.execute('SET SESSION FOREIGN_KEY_CHECKS = ON')
    insp = inspect(engine)
    for table_name in insp.get_table_names():
        engine.execute(f"DELETE FROM {table_name}")

