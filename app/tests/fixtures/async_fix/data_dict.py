from unittest.mock import ANY
import pytest


@pytest.fixture()
def async_list_dict_5():
    return [
        {
            "task_name": "Test postgres",
            "Num_of_executors": 1,
        },
        {
            "task_name": "Test pytest",
            "Num_of_executors": 2,
        },
        {
            "task_name": "Test python skills",
            "Num_of_executors": 3,
        },
        {
            "task_name": "Test async",
            "Num_of_executors": 4,
        },
        {
            "task_name": "Test all in the world",
            "Num_of_executors": 5,
        },
    ]