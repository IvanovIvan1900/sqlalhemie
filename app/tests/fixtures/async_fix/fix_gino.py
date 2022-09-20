from gino import Gino
import gino
import pytest_asyncio
import pytest
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db(conn_url):
    async_conn_url = conn_url.replace("postgresql+psycopg2", "postgresql+asyncpg")
    engine = await gino.create_engine(async_conn_url, min_size=1,max_size=1)
    db = Gino()
    db.bind = engine
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