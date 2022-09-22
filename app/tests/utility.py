from typing import Any
from sqlalchemy.engine.result  import RowProxy

def get_dict_from_RowProxy(row_proxy:RowProxy)->dict:
    # https://docs.sqlalchemy.org/en/13/core/connections.html?highlight=resultproxy#sqlalchemy.engine.ResultProxy
    if isinstance(row_proxy, RowProxy):
        return dict(row_proxy.items())
    else:
        raise AttributeError(f"input data not correct type. Expected RowProxy, get {type(row_proxy)}")


def copy_list_update_key_in_dict(input_list:list[dict], dict_update:dict)->list[dict]:
    return [dict(**dict_update, **elem) for elem in input_list]

def aplly_func_to_dict_and_return_dict(func, dict_input:dict)->dict:
    func(dict_input)
    return dict_input