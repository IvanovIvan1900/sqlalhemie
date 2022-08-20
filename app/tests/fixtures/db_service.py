from datetime import datetime

import pytest
from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, ForeignKey,
                        ForeignKeyConstraint, Integer, MetaData, Numeric,
                        String, Table, create_engine, inspect)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker


@pytest.fixture(scope="session")
def engine():
    return  create_engine('sqlite:///:memory:')

@pytest.fixture(scope="session")
def connection(engine):
    return engine.connect()

@pytest.fixture(scope="session")
def Base():
    return declarative_base()


@pytest.fixture(scope="session")
def session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

@pytest.fixture(scope="session")
def table_line_items(engine, table_orders, table_cookies):
    metadata = MetaData(bind=engine)
    line_items = Table('line_items', metadata,
    Column('line_items_id', Integer(), primary_key=True),
    Column('order_id', ForeignKey(table_orders.c.order_id)),
    Column('cookie_id', ForeignKey(table_cookies.c.cookie_id)),
    Column('quantity', Integer()),
    Column('extended_cost', Numeric(12, 2))
    )
    metadata.create_all(engine)

    return line_items

@pytest.fixture(scope="session")
def table_orm_line_items(Base, engine, table_orm_orders, table_orm_cookies):
    class LineItem(Base):
        __tablename__ = 'line_items'
        line_item_id = Column(Integer(), primary_key=True)
        order_id = Column(Integer(), ForeignKey('orders.order_id'))
        cookie_id = Column(Integer(), ForeignKey('cookies.cookie_id'))
        quantity = Column(Integer())
        extended_cost = Column(Numeric(12, 2))
        order = relationship("Order", backref=backref('line_items',
        order_by=line_item_id))
        cookie = relationship("Cookie", uselist=False)

        def __repr__(self):
            return "LineItems(order_id={self.order_id}, " \
                    "cookie_id={self.cookie_id}, " \
                    "quantity={self.quantity}, " \
                    "extended_cost={self.extended_cost})".format(
                    self=self)

        

    Base.metadata.create_all(engine)
    return LineItem

@pytest.fixture(scope="session")
def table_orders(engine, table_users):
    metadata = MetaData(bind=engine)
    orders = Table('orders', metadata,
    Column('order_id', Integer(), primary_key=True),
    Column('user_id', ForeignKey(table_users.c.user_id)),
    Column('shipped', Boolean(), default=False)
    )
    metadata.create_all(engine)

    return orders

@pytest.fixture(scope="session")
def table_orm_orders(Base, engine, table_orm_users):
    class Order(Base):
        __tablename__ = 'orders'
        order_id = Column(Integer(), primary_key=True)
        user_id = Column(Integer(), ForeignKey('users.user_id'))
        shipped = Column(Boolean(), default=False)
        user = relationship("User", backref=backref('orders', order_by=order_id))

        def __repr__(self):
            return "Order(user_id={self.user_id}, " \
                "shipped={self.shipped})".format(self=self)

        @classmethod
        def create_from_dict(cls, dict_data:dict, table_orm_line_items):
            order = cls()
            order.user = dict_data["user"]
            for elem in dict_data["line_items"]:
                line_item = table_orm_line_items()
                line_item.cookie = elem["cookie"]
                order.line_items.append(line_item)

            return order

    Base.metadata.create_all(engine)
    return Order

@pytest.fixture(scope="session")
def table_users(engine):
    metadata = MetaData(bind=engine)
    users = Table('users', metadata,
    Column('user_id', Integer(), primary_key=True),
    Column('customer_number', Integer(), autoincrement=True),
    Column('username', String(15), nullable=False, unique=True),
    Column('email_address', String(255), nullable=False),
    Column('phone', String(20), nullable=False),
    Column('password', String(25), nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
    )
    metadata.create_all(engine)

    return users

@pytest.fixture(scope="session")
def table_orm_users(Base, engine):
    class User(Base):
        __tablename__ = 'users'
        user_id = Column(Integer(), primary_key=True)
        username = Column(String(15), nullable=False, unique=True)
        email_address = Column(String(255), nullable=False)
        customer_number = Column(Integer())
        phone = Column(String(20), nullable=False)
        password = Column(String(25), nullable=False)
        created_on = Column(DateTime(), default=datetime.now)
        updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)    

        def __repr__(self):
            return "User(username='{self.username}', " \
                    "email_address='{self.email_address}', " \
                    "phone='{self.phone}', " \
                    "password='{self.password}')".format(self=self)

    Base.metadata.create_all(engine)
    return User

@pytest.fixture(scope="session")
def table_cookies(engine):
    metadata = MetaData(bind=engine)
    cookies = Table('cookies', metadata,
    Column('cookie_id', Integer(), primary_key=True),
    Column('cookie_name', String(50), index=True),
    Column('cookie_recipe_url', String(255)),
    Column('cookie_sku', String(55)),
    Column('quantity', Integer()),
    Column('unit_cost', Numeric(12, 2)),
    CheckConstraint('quantity >= 0', name='quantity_positive')
    )
    metadata.create_all(engine)

    return cookies

@pytest.fixture(scope="session")
def table_orm_cookies(Base, engine):
    class Cookie(Base):
        __tablename__ = 'cookies'
        cookie_id = Column(Integer(), primary_key=True)
        cookie_name = Column(String(50), index=True)
        cookie_recipe_url = Column(String(255))
        cookie_sku = Column(String(55))
        quantity = Column(Integer())
        unit_cost = Column(Numeric(12, 2))

        def __repr__(self):
            return "Cookie(cookie_name='{self.cookie_name}', " \
                "cookie_recipe_url='{self.cookie_recipe_url}', " \
                "cookie_sku='{self.cookie_sku}', " \
                "quantity={self.quantity}, " \
                "unit_cost={self.unit_cost})".format(self=self)

        def __eq__(self, other):
            if type(self) != type(other):
                return False

            return all(self.__dict__.get(field_name) == other.__dict__.get(field_name) for field_name in self.__dict__)


    Base.metadata.create_all(engine)

    return Cookie

@pytest.fixture(scope="session")
def table_emploee(engine):
    metadata = MetaData(bind=engine)
    employee_table = Table(
        'employee', metadata,
        Column('id', Integer, primary_key=True),
        Column('manager_id', None, ForeignKey('employee.id')),
        Column('name', String(255)))    
    metadata.create_all(engine)

    return employee_table

@pytest.fixture(autouse=True)
def clear_db(engine):
# It may be enough to disable a foreign key checks just for the current session:
# con.execute('SET SESSION FOREIGN_KEY_CHECKS = ON')
    insp = inspect(engine)
    for table_name in insp.get_table_names():
        engine.execute(f"DELETE FROM {table_name}")

@pytest.fixture(scope="session")
def table_orm_test_constrains(engine):
    Base = declarative_base()
    class SomeDataClass(Base):
        __tablename__ = 'somedatatable'
        __table_args__ = (ForeignKeyConstraint(['id'], ['other_table.id']), 
                    CheckConstraint('unit_cost >= 0.00', 
                    name='unit_cost_positive'))
    Base.metadata.create_all(engine)

    return Cookie

