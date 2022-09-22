from gino import Gino
import gino
import pytest_asyncio
import pytest
import asyncio
from sqlalchemy import inspect

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db(conn_url):
    # https://python-gino.org/docs/en/master/explanation/engine.html
#     For Dialect:

    #     isolation_level

    #     paramstyle

    # For Engine:

    #     echo

    #     execution_options

    #     logging_name

    async_conn_url = conn_url.replace("postgresql+psycopg2", "postgresql+asyncpg")
    engine = await gino.create_engine(async_conn_url, min_size=1,max_size=1)
    db = Gino()
    db.bind = engine
    await drop_the_table(db)
    yield db
    await db.pop_bind().close()


@pytest_asyncio.fixture(scope="session")
async def table_tasks(db):
    class Task(db.Model):
        __tablename__ = 'tasks'

        task_id = db.Column(db.Integer(), primary_key=True)
        task_name = db.Column(db.String(100), default='noname')
        Num_of_executors = db.Column(db.Integer(), default = 1)

    await db.gino.create_all()

    return Task

@pytest_asyncio.fixture()
async def clear_db_gino(db):
    for table in db.sorted_tables:
        await db.status(db.text(f"TRUNCATE {table.name} RESTART IDENTITY CASCADE"))

async def drop_the_table(db):
    result =  await db.status(db.text("DROP SCHEMA public CASCADE;")) 
    result =  await db.status(db.text("CREATE SCHEMA public;")) 
