from typing import Any, List
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import table
from sqlalchemy.orm.decl_api import DeclarativeMeta

@pytest.fixture(scope="function")
def db_cookie_array_two_element_postgres(connection_postgres, table_cookies, array_of_two_cookie):
    for dict_cookie_one in array_of_two_cookie:
        ins = table_cookies.insert()
        dict_cookie_one.pop("cookie_id", None)
        result = connection_postgres.execute(ins, [dict_cookie_one])
        dict_cookie_one["cookie_id"] = result.inserted_primary_key.cookie_id

    return array_of_two_cookie
