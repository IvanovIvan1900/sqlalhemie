import pytest

@pytest.fixture
def all_tree_in_one_list()->list[dict]:
    return [[
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },
        # {
        #     "file_id": "",
        #     "type_file": "FILE",
        #     "parent_id": None,
        #     "size": 10,
        # },
    ],
    ]

@pytest.fixture
def all_tree_partial_1()->list[dict]:
    return [
        [
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },
        ],
        [
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,},
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },

        # {
        #     "file_id": "",
        #     "type_file": "FILE",
        #     "parent_id": None,
        #     "size": 10,
        # },
    ],
    ]

@pytest.fixture
def all_tree_partial_2()->list[dict]:
    return [
        [
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },

        ],
        [
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },

        ],
        [
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        # {
        #     "file_id": "",
        #     "type_file": "FILE",
        #     "parent_id": None,
        #     "size": 10,
        # },
    ],

    ]

@pytest.fixture
def parent_root()->list[dict]:
    return [
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
    ]

@pytest.fixture
def parent_Folder_2_1()->list[dict]:
    return [
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },

    ]

@pytest.fixture
def parent_File_4_2()->list[dict]:
    return [
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },

        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },

    ]


@pytest.fixture
def parent_Folder_3_2()->list[dict]:
    return [
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },

        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },

    ]

@pytest.fixture
def parent_File_2_3()->list[dict]:
    return [
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },

    ]

@pytest.fixture
def child_root()->list[dict]:
    return [
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },

    ]

@pytest.fixture
def child_Folder_2_2()->list[dict]:
    return [
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },

    ]

@pytest.fixture
def child_Folder_2_1()->list[dict]:
    return [
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
    ]

@pytest.fixture
def all_tree_not_correct_two_root()->list[dict]:
    return [[
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },
        # {
        #     "file_id": "",
        #     "type_file": "FILE",
        #     "parent_id": None,
        #     "size": 10,
        # },
    ],
    ]

@pytest.fixture
def all_tree_not_correct_cycle()->list[dict]:
    return [[
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_3_2",
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },
        # {
        #     "file_id": "",
        #     "type_file": "FILE",
        #     "parent_id": None,
        #     "size": 10,
        # },
    ],
    ]

@pytest.fixture
def all_tree_in_incorrect_data_not_exist()->list[dict]:
    return [[
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": "not_exist",
            "size": 0,
        },
    ],
    ]

@pytest.fixture
def tree_change_root()->list[dict]:
    return [
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_1",
            "size": 0,
        },
    ]


@pytest.fixture
def child_root_after_change_root()->list[dict]:
    return [
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_1",
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },

    ]

@pytest.fixture
def child_folder_Folder_2_1_after_change_root()->list[dict]:
    return [
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_1",
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },

    ]

@pytest.fixture
def child_folder_Folder_2_2_after_change_root()->list[dict]:
        return [
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
   ]


@pytest.fixture
def list_tree_delete_Folder_2_2()->list[dict]:
    return [
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },

    ]


@pytest.fixture
def list_tree_delete_File_2_3()->list[dict]:
    return [
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },
    ]

@pytest.fixture
def list_tree_delete_root()->list[dict]:
    return [
    ]

@pytest.fixture
def list_tree_delete_Folder_3_2()->list[dict]:
    return [
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_1",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
    ]

@pytest.fixture
def list_tree_delete_Folder_2_1()->list[dict]:
    return [
        {
            "file_id": "Folder_1",
            "type_file": "FOLDER",
            "parent_id": None,
            "size": 0,
        },
        {
            "file_id": "Folder_2_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_1",
            "size": 0,
        },
        {
            "file_id": "File_2_3",
            "type_file": "FILE",
            "parent_id": "Folder_1",
            "size": 128,
        },
        {
            "file_id": "File_3_1",
            "type_file": "FILE",
            "parent_id": "Folder_2_2",
            "size": 512,
        },
        {
            "file_id": "Folder_3_2",
            "type_file": "FOLDER",
            "parent_id": "Folder_2_2",
            "size": 0,
        },
        {
            "file_id": "File_4_1",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 1024,
        },
        {
            "file_id": "File_4_2",
            "type_file": "FILE",
            "parent_id": "Folder_3_2",
            "size": 2048,
        },
    ]