import asyncio
from email.policy import default
from asyncpgsa import pg
from sqlalchemy.dialects import postgresql
import pytest
import pytest_asyncio
from sqlalchemy import MetaData, create_engine, Column, Integer, String, Table, inspect
from app.tests.utility import get_url_from_dict


@pytest.fixture(scope='session')
def async_pool(event_loop, dict_url:dict):
    from asyncpgsa import create_pool
    # from . import HOST, PORT, USER, PASS, DB_NAME

    pool = create_pool(
        min_size=1,
        max_size=3,
        host=dict_url["host"],
        port=dict_url["port"],
        user=dict_url["user"],
        password=dict_url["password"],
        database=dict_url["database"],
        timeout=1,
        loop=event_loop
    )

    event_loop.run_until_complete(pool)

    try:
        yield pool
    finally:
        event_loop.run_until_complete(pool.close())

@pytest_asyncio.fixture(scope="session")
async def pg_siglton_init(event_loop, dict_url:dict):
    await pg.init(
        host=dict_url["host"],
        port=dict_url["port"],
        user=dict_url["user"],
        password=dict_url["password"],
        database=dict_url["database"],
        loop=event_loop,
        min_size=5,
        max_size=10
    )

@pytest.fixture(scope='session')
def async_connection(async_pool, event_loop):
    conn = event_loop.run_until_complete(async_pool.acquire(timeout=2))
    asunc_pg_drop_the_table(conn, event_loop)
    try:
        yield conn
    finally:
        event_loop.run_until_complete(async_pool.release(conn))

# @pytest.fixture(scope="session")
# def async_event_loop():
#     policy = asyncio.get_event_loop_policy()
#     loop = policy.new_event_loop()
#     yield loop
#     loop.close()

@pytest.fixture(scope='session')
def asyncpg_metadata(dict_url:dict):
    async_conn_url =get_url_from_dict("postgresql", dict_url)
    metadata = MetaData()
    metadata.bind = create_engine(async_conn_url)
    return metadata


@pytest_asyncio.fixture(scope="session")
async def asyncpg_table_tasks(asyncpg_metadata, async_connection):
    # async_connection - необходим т.к. иначе эта фикстура вызывается раньше, очищаются созданные таблицы в базе
    task_table =  Table('tasks', asyncpg_metadata,
        Column('task_id', Integer, primary_key=True),
        Column('task_name', String(100), default='noname'),
        Column('Num_of_executors', Integer(), default = 1),
    )
    task_table.create(checkfirst = True)
    return task_table



@pytest.fixture()
def clear_db_async_pg(asyncpg_metadata):
# It may be enough to disable a foreign key checks just for the current session:
# con.execute('SET SESSION FOREIGN_KEY_CHECKS = ON')
    engine = asyncpg_metadata.bind
    insp = inspect(engine)
    for table_name in insp.get_table_names():
        engine.execute(f"DELETE FROM {table_name}")

def asunc_pg_drop_the_table(conn, event_loop):
    result = event_loop.run_until_complete(conn.fetch("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'public';"))
    if len(result) > 0:
        result =  event_loop.run_until_complete(conn.fetch("DROP SCHEMA public CASCADE;"))
    result =  event_loop.run_until_complete(conn.fetch("CREATE SCHEMA public;"))
