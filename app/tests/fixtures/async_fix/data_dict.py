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

@pytest.fixture()
def async_list_tack_dict_5():
    return {
        "tasks":[
        {
            "task_id": 1,
            "task_name": "Test postgres",
            "Num_of_executors": 1,
        },
        {
            "task_id": 2,
            "task_name": "Test pytest",
            "Num_of_executors": 2,
        },
        {
            "task_id": 3,
            "task_name": "Test python skills",
            "Num_of_executors": 3,
        },
        {
            "task_id": 4,
            "task_name": "Test async",
            "Num_of_executors": 4,
        },
        {
            "task_id": 5,
            "task_name": "Test all in the world",
            "Num_of_executors": 5,
        },
    ],
    "time_tracks":
    [
        {
            "task_id": 1,
            "time_track_id": 1,
            "count_secodns": 10,
        },
        {
            "task_id": 1,
            "time_track_id": 2,
            "count_secodns": 150,
        },
        {
            "task_id": 2,
            "time_track_id": 3,
            "count_secodns": 100,
        },
        {
            "task_id": 1,
            "time_track_id": 4,
            "count_secodns": 50,
        },
        {
            "task_id": 3,
            "time_track_id": 5,
            "count_secodns": 15,
        },
    ],
    }

