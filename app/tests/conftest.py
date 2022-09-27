from .fixtures import *  # Do not remove this line!
from .tree.tree_fixture import *
import pytest

@pytest.fixture(scope="session")
def dict_url():
    return {
        "host": "127.0.0.1",
        "port": 5456,
        "database": "alchemie_test",
        "user": "alchemie_test",
        "password": "test",
    }
