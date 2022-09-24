from functools import partial
from operator import itemgetter
from app.tests.tree.tree_implement import Tree
from pytest_dictsdiff import check_objects
import pytest

class TestTreeAddUpdateChild:


    @pytest.mark.parametrize("input_list, output_list, file_id_for_child, name_test",
                    [
                        (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("child_root"), "Folder_1", "AllTree"),
                        (pytest.lazy_fixture("all_tree_partial_1"),pytest.lazy_fixture("child_root"), "Folder_1", "Part_1"),
                        (pytest.lazy_fixture("all_tree_partial_2"),pytest.lazy_fixture("child_root"), "Folder_1", "Part_2"),
                        # (pytest.lazy_fixture(""),pytest.lazy_fixture("")),
                        (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("child_Folder_2_2"), "Folder_2_2", "default"),
                        (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("child_Folder_2_1"), "Folder_2_1", "default"),
                        (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("child_root"), None, "default"),
                    ]
                )
    def test_append_tree_and_get_child(self, input_list:list[dict], file_id_for_child:str, output_list:list[dict], name_test:str):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")
        for item_list in input_list:
            tree.add_data(item_list)

        list_output_tree = tree.get_child(file_id_for_child)
        assert len(output_list) == len(list_output_tree)

        for elem_etalon, elem_tree in zip(sorted(output_list, key=itemgetter("file_id")), sorted(list_output_tree, key=itemgetter("file_id"))):
            assert check_objects(elem_etalon , elem_tree, verbose=1)

    def test_get_child_wich_empty_tree(self):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")

        list_output_tree = tree.get_child()
        assert len(list_output_tree) == 0


    def test_update_element(self,all_tree_in_one_list, child_root):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")
        for item_list in all_tree_in_one_list:
            tree.add_data(item_list)
        key_change = "File_3_1"
        elem_change = [elem for elem in all_tree_in_one_list[0] if elem["file_id"] == key_change]
        elem_change[0]["size"] = 1024
        tree.add_data(all_tree_in_one_list[0])

        output_change = [elem for elem in child_root if elem["file_id"] == key_change]
        output_change[0]["size"] = 1024

        list_output_tree = tree.get_child("Folder_1")
        assert len(child_root) == len(list_output_tree)

        for elem_etalon, elem_tree in zip(sorted(child_root, key=itemgetter("file_id")), sorted(list_output_tree, key=itemgetter("file_id"))):
            assert check_objects(elem_etalon , elem_tree, verbose=1)


    @pytest.mark.parametrize("input_list, change_list, output_list, file_id_for_child",
        [
            (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("tree_change_root"), pytest.lazy_fixture("child_root_after_change_root"), "Folder_1"),
            (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("tree_change_root"), pytest.lazy_fixture("child_folder_Folder_2_1_after_change_root"), "Folder_2_1"),
            (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("tree_change_root"), pytest.lazy_fixture("child_folder_Folder_2_2_after_change_root"), "Folder_2_2"),
        ]
    )
    def test_update_root_element(self, input_list:list[dict], change_list:list[dict], file_id_for_child:str, output_list:list[dict]):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")
        for item_list in input_list:
            tree.add_data(item_list)

        tree.add_data(change_list)

        list_output_tree = tree.get_child(file_id_for_child)
        assert len(output_list) == len(list_output_tree)

        for elem_etalon, elem_tree in zip(sorted(output_list, key=itemgetter("file_id")), sorted(list_output_tree, key=itemgetter("file_id"))):
            assert check_objects(elem_etalon , elem_tree, verbose=1)

    @pytest.mark.parametrize("input_list, output_list, file_id_for_parent",
                    [
                        (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("parent_root"), "Folder_1"),
                        (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("parent_Folder_2_1"), "Folder_2_1"),
                        (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("parent_File_4_2"), "File_4_2"),
                        (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("parent_Folder_3_2"), "Folder_3_2"),
                        (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("parent_File_2_3"), "File_2_3"),
                        # (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture(""), ""),
                    ]
                )
    def test_get_parent(self, input_list:list[dict], file_id_for_parent:str, output_list:list[dict]):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")
        for item_list in input_list:
            tree.add_data(item_list)

        list_output_tree = tree.get_parent(file_id_for_parent)
        assert len(output_list) == len(list_output_tree)

        for elem_etalon, elem_tree in zip(sorted(output_list, key=itemgetter("file_id")), sorted(list_output_tree, key=itemgetter("file_id"))):
            assert check_objects(elem_etalon , elem_tree, verbose=1)

class TestTreeIncorrectData():

    def test_incorrect_data_two_root(self, all_tree_not_correct_two_root):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")
        with pytest.raises(AttributeError) as e_info:
            tree.add_data(all_tree_not_correct_two_root[0])
        assert 'have more than one root. Id is Folder_1, Folder_2_1' == e_info.value.args[0]

    def test_incorrect_data_net_exist_element(self, all_tree_in_incorrect_data_not_exist):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")
        with pytest.raises(AttributeError) as e_info:
            tree.add_data(all_tree_in_incorrect_data_not_exist[0])
        assert 'element wich id "Folder_1" has parent_id is "not_exist", but elemnt wich this is id is not exist' == e_info.value.args[0]

    def test_incorrect_data_cycle(self, all_tree_not_correct_cycle):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")
        with pytest.raises(AttributeError) as e_info:
            tree.add_data(all_tree_not_correct_cycle[0])
        assert 'have less than one root.' == e_info.value.args[0]


class TestDelete():


    @pytest.mark.parametrize("input_list, output_list, file_id_delete",
            [
                (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("list_tree_delete_Folder_2_2"), "Folder_2_2"),
                (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("list_tree_delete_File_2_3"), "File_2_3"),
                (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("list_tree_delete_root"), "Folder_1"),
                (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("list_tree_delete_Folder_3_2"), "Folder_3_2"),
                (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture("list_tree_delete_Folder_2_1"), "Folder_2_1"),
                # (pytest.lazy_fixture("all_tree_in_one_list"),pytest.lazy_fixture(""), ""),
            ]
        )
    def test_delete_item(self, input_list:list[dict], file_id_delete:str, output_list:list[dict]):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")
        for item_list in input_list:
            tree.add_data(item_list)
        tree.del_items(file_id_delete)
        file_id = None
        if tree.root is not None:
            file_id = tree.root["file_id"]
        list_output_tree = tree.get_child(file_id)
        assert len(output_list) == len(list_output_tree)

        for elem_etalon, elem_tree in zip(sorted(output_list, key=itemgetter("file_id")), sorted(list_output_tree, key=itemgetter("file_id"))):
            assert check_objects(elem_etalon , elem_tree, verbose=1)

class TestApplyFunc():

    def test_func_for_child(self, all_tree_in_one_list:list[dict]):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")
        for item_list in all_tree_in_one_list:
            tree.add_data(item_list)

        list_of_result:list[dict] = []
        def add_to_list(elem:dict, list_of_elem:list[dict])->None:
            elem_copy = {key:value for key,value in elem.items() if key != "children"}
            list_of_elem.append(elem_copy)

        my_func = partial(add_to_list, list_of_elem = list_of_result)
        elem_id = "Folder_2_2"
        tree.apply_func_for_all_child_and_node(my_func, elem_id)

        all_child = tree.get_child(elem_id)

        assert len(all_child) == len(list_of_result)

        assert check_objects(all_child, list_of_result)

    def test_func_for_parent(self, all_tree_in_one_list:list[dict]):
        tree = Tree(key_id = "file_id", key_parent_id = "parent_id")
        for item_list in all_tree_in_one_list:
            tree.add_data(item_list)

        list_of_result:list[dict] = []
        elem_id = "Folder_2_2"

        def add_to_list(elem:dict, list_of_elem:list[dict])->None:
            elem_copy = {key:value for key,value in elem.items() if key != "children"}
            list_of_elem.append(elem_copy)
        my_func = partial(add_to_list, list_of_elem = list_of_result)
        tree.apply_func_for_all_parent_node(my_func, elem_id)

        all_child = tree.get_parent(elem_id)

        assert len(all_child) == len(list_of_result)

        assert check_objects(all_child, list_of_result)
