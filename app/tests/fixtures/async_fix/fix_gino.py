from gino import Gino
import gino
import pytest_asyncio
import pytest
import asyncio
from sqlalchemy import inspect, ForeignKey
from enum import Enum
from gino.dialects.asyncpg import AsyncEnum
from app.tests.utility import get_url_from_dict

class TypeFiles(Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db(dict_url):
    # https://python-gino.org/docs/en/master/explanation/engine.html
#     For Dialect:
    #     isolation_level
    #     paramstyle
    # For Engine:
    #     echo
    #     execution_options
    #     logging_name

    # async_conn_url = conn_url.replace("postgresql+psycopg2", "postgresql+asyncpg")
    async_conn_url =get_url_from_dict("postgresql+asyncpg", dict_url)
    engine = await gino.create_engine(async_conn_url, min_size=1,max_size=5)
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

        def __init__(self, **kw):
                super().__init__(**kw)
                self._time_tracks = set()

        def __repr__(self) -> str:
            return f'id: {self.task_id}, name: {self.task_name}, num: {self.Num_of_executors}'

        @property
        def time_tracks(self):
            return self._time_tracks

        @time_tracks.setter
        def add_time_tracks(self, value):
            self._time_tracks.add(value)

    await db.gino.create_all()

    return Task


@pytest_asyncio.fixture(scope="session")
async def table_tasks_time_track(db, table_tasks):
    class TimeTrack(db.Model):
        __tablename__ = 'time_tracks'

        task_id = db.Column(db.Integer(), ForeignKey(table_tasks.task_id))
        time_track_id = db.Column(db.Integer(), primary_key=True)
        count_secodns = db.Column(db.Integer())

        def __repr__(self) -> str:
            return f'task_id: {self.task_id}, track_id: {self.time_track_id}, count: {self.count_secodns}'
    await db.gino.create_all()

    return TimeTrack

@pytest_asyncio.fixture(scope="session")
async def table_files(db):
    class File(db.Model):
        __tablename__ = 'files'

        file_id = db.Column(db.String(40), primary_key=True)
        type_file = db.Column(AsyncEnum(TypeFiles), nullable=False)
        parent_id = db.Column(db.String(40), db.ForeignKey('files.file_id', ondelete="CASCADE"), nullable = True)
        size = db.Column(db.Integer())

        def __repr__(self) -> str:
            return f'id: {self.file_id}, parent: {self.parent_id}, size: {self.size}, type: {self.type_file}'

    await db.gino.create_all()
    return File

@pytest_asyncio.fixture()
async def clear_db_gino(db):
    for table in db.sorted_tables:
        await db.status(db.text(f"TRUNCATE {table.name} RESTART IDENTITY CASCADE"))

async def drop_the_table(db):
    result = await db.all(db.text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'public';"))
    if len(result) > 0:
        result =  await db.status(db.text("DROP SCHEMA public CASCADE;"))
    result =  await db.status(db.text("CREATE SCHEMA public;"))
