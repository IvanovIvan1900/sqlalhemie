import logging
import sys
from datetime import datetime

import pytest
from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, ForeignKey,
                        ForeignKeyConstraint, Integer, MetaData, Numeric,
                        String, Table, UniqueConstraint, create_engine,
                        inspect)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy.sql import func


@pytest.fixture(scope="session")
def conn_url():
    return 'postgresql+psycopg2://alchemie_test:test@127.0.0.1:5456/alchemie_test'

@pytest.fixture(scope="session")
def engine_postgres(conn_url):
    logging.basicConfig()
    root = logging.getLogger('sqlalchemy.engine')
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    engine_postgres =  create_engine(conn_url)
    drop_the_table(engine_postgres)
    # drop_the_table(engine_postgres_=engine_postgres)
    return engine_postgres

@pytest.fixture(scope="session")
def connection_postgres(engine_postgres):
    return engine_postgres.connect()


@pytest.fixture(scope="session")
def table_users_postgres(engine_postgres):
    metadata = MetaData(bind=engine_postgres)
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

    metadata.create_all(engine_postgres)

    return users

@pytest.fixture(scope="session")
def table_cookies_postgres(engine_postgres):
    metadata = MetaData(bind=engine_postgres)
    cookies = Table('cookies', metadata,
    Column('cookie_id', Integer(), primary_key=True),
    Column('cookie_name', String(50), index=True, unique=True),
    Column('cookie_recipe_url', String(255)),
    Column('cookie_sku', String(55)),
    Column('quantity', Integer()),
    Column('unit_cost', Numeric(12, 2)),
    CheckConstraint('quantity >= 0', name='quantity_positive'),
    UniqueConstraint('cookie_name', name='name_constrains')
    )
    metadata.create_all(engine_postgres)

    return cookies

@pytest.fixture()
def clear_db_pg(engine_postgres):
# It may be enough to disable a foreign key checks just for the current session:
# con.execute('SET SESSION FOREIGN_KEY_CHECKS = ON')
    insp = inspect(engine_postgres)
    for table_name in insp.get_table_names():
        engine_postgres.execute(f"DELETE FROM {table_name}")

def drop_the_table(engine_postgres_):
    engine_postgres_.execute("DROP SCHEMA public CASCADE;")
    engine_postgres_.execute("CREATE SCHEMA public;")