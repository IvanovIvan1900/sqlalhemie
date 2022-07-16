from decimal import Decimal
import pytest

@pytest.fixture(scope="session")
def dict_cookie_one()->dict:
    return {
        "cookie_name":"chocolate chip",
        "cookie_recipe_url":"http://some.aweso.me/cookie/recipe.html",
        "cookie_sku":"CC01",
        "quantity":12,
        "unit_cost":Decimal(0.50)
    }

@pytest.fixture(scope="session")
def array_of_two_cookie()->list[dict]:
    data_list = [
    {
    'cookie_name': 'peanut butter',
    'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
    'cookie_sku': 'PB01',
    'quantity': 24,
    'unit_cost': Decimal(0.25)
    },
    {
    'cookie_name': 'oatmeal raisin',
    'cookie_recipe_url': 'http://some.okay.me/cookie/raisin.html',
    'cookie_sku': 'EWW01',
    'quantity': 100,
    'unit_cost': Decimal(1.00)
    }
    ]
    return data_list

@pytest.fixture(scope="session")
def dict_user_one()->dict:
    return {
        "customer_number":"10",
        "username":"user one",
        "email_address":"user_one@mail.ru",
        "phone":"111-111-1111",
        "password":"passw_one",
    }

@pytest.fixture(scope="session")
def dict_user_two()->dict:
    return {
        "customer_number":"20",
        "username":"user two",
        "email_address":"user_two@mail.ru",
        "phone":"222-222-2222",
        "password":"passw_two",
    }

@pytest.fixture(scope="function")
def dict_orders_one(db_user_one, db_cookie_one, db_cookie_array_two_element)->dict:
    return {
        "user_id":db_user_one["user_id"], 
        "line_items":[
            {
                "cookie_id":db_cookie_one["cookie_id"],
                "quantity":10,
                "extended_cost":150,
            },
            {
                "cookie_id":db_cookie_array_two_element[0]["cookie_id"],
                "quantity":2,
                "extended_cost":10,
            },
            {
                "cookie_id":db_cookie_array_two_element[1]["cookie_id"],
                "quantity":150,
                "extended_cost":2300,
            },
        ]
    }

@pytest.fixture(scope="function")
def dict_orders_two(db_user_one,db_cookie_one, db_cookie_array_two_element)->dict:
    return {
        "user_id":db_user_one["user_id"], 
        "line_items":[
            {
                "cookie_id":db_cookie_one["cookie_id"],
                "quantity":10,
                "extended_cost":150,
            },
            {
                "cookie_id":db_cookie_array_two_element[1]["cookie_id"],
                "quantity":150,
                "extended_cost":2300,
            },
        ]
    }

@pytest.fixture(scope="function")
def dict_orders_tree(db_user_two,db_cookie_one, db_cookie_array_two_element)->dict:
    return {
        "user_id":db_user_two["user_id"], 
        "line_items":[
        ]
    }

