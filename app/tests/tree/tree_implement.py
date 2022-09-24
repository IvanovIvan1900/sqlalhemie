from queue import Queue
from typing import Any, Optional
from functools import partial

class Tree():
    """Реализует структуру дерева, которое поддерживает некоторые методы работы с ним. 
        Может быть использовано для тестирования реализаций древовидных структру в бд и сервисов по работе с ними"""
    key_id:str
    key_parent_id:str
    key_children:str
    dict_key_to_value:dict 
    root:dict = None


    def _apply_func_for_all_child(self, func:callable, elem_id:Any)->None:
        """recursive call func for all child for elem wich id 
           WARNING, INCLUDE curr node

        Args:
            func (callable): Function has a one parameter, item from tree
            elem_id (Any): id - item for child apply func
        """
        if self.root is None:
            return None
        root = self.dict_key_to_value.get(elem_id)
        if root is None:
            raise AttributeError(f'Tree apply func for all child. Item wich id is {elem_id} is not exist')
        anti_recursive_set = set()
        queue = Queue()
        queue.put(root)
        while not queue.empty():
            curr_elem = queue.get()
            if curr_elem[self.key_id] in anti_recursive_set:
                raise AttributeError(f'Tree has a cycle. Id is {curr_elem[self.key_id]}')
            func(curr_elem)
            for inner_elem in curr_elem[self.key_children]:
                queue.put(inner_elem)

    def _appy_func_for_all_parent(self, func:callable, elem_id:Any)->None:
        """recursive call func for all parent for elem wich id
           WARNING, not include curr node

        Args:
            func (callable): Function has a one parameter, item from tree
            elem_id (Any): id - item for parent apply func
        """
        parent_id = elem_id
        while parent_id is not None:
            curr_elem = self.dict_key_to_value.get(parent_id)
            if curr_elem is None:
                raise AttributeError(f'Func apply for all parent. Elem wich id {parent_id} is not present in tree')
            func(curr_elem)
            parent_id = curr_elem[self.key_parent_id]

    def __init__(self, key_id:str, key_parent_id:str, key_children:str = "children") -> None:
        """Creat class

        Args:
            key_id (str): name field wich key
            key_parent_id (str): name field wich key parent
            key_children (str): name field wich children
        """
        self.key_id = key_id
        self.key_parent_id = key_parent_id
        self.key_children = key_children
        self.dict_key_to_value = {}

    def _set_root(self):
        list_elem_wichout_root = [elem for elem in self.dict_key_to_value.values() if elem[self.key_parent_id] is None]
        if len(list_elem_wichout_root) == 1:
            self.root = list_elem_wichout_root[0]
        elif len(list_elem_wichout_root) > 1:
            raise AttributeError(f'have more than one root. Id is {", ".join((elem[self.key_id] for elem in list_elem_wichout_root))}')
        elif not list_elem_wichout_root and len(self.dict_key_to_value.keys()) > 0:
            raise AttributeError('have less than one root.')

    def add_data(self, list_of_data:list[dict])->None:
        """ Add or update data in tree

        Args:
            list_of_data (list[dict]): input list data
        """
        for elem in list_of_data:
            key = elem[self.key_id]
            new_elem = self.dict_key_to_value.get(key)
            if new_elem is not None:
                if new_elem[self.key_parent_id] != elem[self.key_parent_id] and new_elem[self.key_parent_id] is not None:
                    parent = self.dict_key_to_value.get(new_elem[self.key_parent_id])
                    parent[self.key_children] = [item for item in parent[self.key_children] if item[self.key_id] != key]
                new_elem.update(elem)
                new_elem[self.key_children] = self.dict_key_to_value[key][self.key_children]
                self.dict_key_to_value[key] = new_elem
            else:
                new_elem = elem.copy()
                new_elem[self.key_children] = []
                self.dict_key_to_value[key] = new_elem
        for elem in list_of_data:
            if elem[self.key_parent_id] is not None:
                parent = self.dict_key_to_value.get(elem[self.key_parent_id])
                if parent is None:
                    raise AttributeError(f'element wich id "{elem[self.key_id]}" has {self.key_parent_id} is "{elem[self.key_parent_id]}", but elemnt wich this is id is not exist')
                if elem[self.key_id] not in (item[self.key_id] for item in parent[self.key_children]):
                    parent[self.key_children].append(self.dict_key_to_value[elem[self.key_id]])
        self._set_root()

    def get_child(self, id_node:Optional[Any] = None)->list[dict]:
        """Get current node and all child

        Args:
            id_node (Optional[Any], optional): id - node, if None - get from root. Defaults to None.

        Raises:
            ValueError: if not exist raise exception

        Returns:
            list[dict]: list all child and node
        """
        if self.root is None:
            return []
        if id_node is None:
            id_node = self.root[self.key_id]
        elem_root = self.dict_key_to_value.get(id_node)
        if elem_root is None :
            raise ValueError(f'Key {id_node} not exist in tree')
        list_of_result:list[dict] = []

        def add_to_list(elem:dict, list_of_elem:list[dict])->None:
            elem_copy = {key:value for key,value in elem.items() if key != self.key_children}
            list_of_elem.append(elem_copy)

        my_func = partial(add_to_list, list_of_elem = list_of_result)
        self._apply_func_for_all_child(my_func, elem_id=id_node)

        return list_of_result

    def get_parent(self, id_node:Any)->list[dict]:
        list_of_result:list[dict] = []

        def add_to_list(elem:dict, list_of_elem:list[dict])->None:
            elem_copy = {key:value for key,value in elem.items() if key != self.key_children}
            list_of_elem.append(elem_copy)
        my_func = partial(add_to_list, list_of_elem = list_of_result)
        self._appy_func_for_all_parent(my_func, id_node)

        return list_of_result

    def del_items(self, id_node:Any)->None:
        """Delete node wich id, from tree

        Args:
            id_node (Any): id node

        Raises:
            AttributeError: if node is not exist
        """
        if self.root is None:
            return None
        if self.root[self.key_id] == id_node:
            self.dict_key_to_value = {}
            self.root = None
            return None
        elem = self.dict_key_to_value.get(id_node)
        if elem is None:
            raise AttributeError(f'Dele elem wich id {id_node}. Elem not present in tree')
        if elem[self.key_parent_id] is not None:
            parent = self.dict_key_to_value.get(elem[self.key_parent_id])
            parent[self.key_children] = [item for item in parent[self.key_children] if item[self.key_id] != id_node]
        list_child = self.get_child(id_node)
        list_id_delete = [elem[self.key_id] for elem in list_child]
        for elem_id in list_id_delete:
            del self.dict_key_to_value[elem_id]

    def apply_func_for_all_child_and_node(self, func: callable, elem_id:Optional[Any]= None)->None:
        """Apply any func for element in tree, curr node and all child
            WARNIN func apply and root node
        Args:
            func (callable): funciton , has one argument - element tree
            elem_id (Optional[Any], optional): id node, default - None - root tree. Defaults to None.
        """
        if self.root is None:
            return None
        self._apply_func_for_all_child(func=func, elem_id=elem_id)

    def apply_func_for_all_parent_node(self, func: callable, elem_id:Any)->None:
        """Apply any func for element in tree, parent for curr node
            WARNIN func NOT apply for root node
        Args:
            func (callable): funciton , has one argument - element tree
            elem_id (Any): id node
        """
        if self.root is None:
            return None
        self._appy_func_for_all_parent(func=func, elem_id=elem_id)
