import pytest
from sqlalchemy import inspect
from sqlalchemy import table

pytestmark = pytest.mark.usefixtures("clear_db")

class TestWorkWichMetadta:

    def test_inspect_table(self, engine, table_orm_users_test_raw:table):
        inspector = inspect(engine)
        schemas = inspector.get_schema_names()
        dict_info = {}
        for schema in schemas:
            for table_name in inspector.get_table_names(schema=schema):
                dict_info[table_name] = []
                for column in inspector.get_columns(table_name, schema=schema):
                    dict_info[table_name].append(column)

        a = 4