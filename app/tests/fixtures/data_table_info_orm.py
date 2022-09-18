from datetime import datetime
import sys

import pytest
from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, ForeignKey,
                        ForeignKeyConstraint, Integer, MetaData, Numeric,
                        String, Table, create_engine, inspect)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy.sql import func


@pytest.fixture(scope="session")
def Base():
    return declarative_base()

@pytest.fixture(scope="session")
def session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

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
def table_orm_users(Base, engine):
    class User(Base):
        __tablename__ = 'users'
        __mapper_args__ = {'polymorphic_identity': 'users'}
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

        def __eq__(self, other):
                if isinstance(other, self.__class__):
                    return self.__dict__ == other.__dict__
                else:
                    return False
    Base.metadata.create_all(engine)
    return User

@pytest.fixture(scope="session")
def table_orm_users_test_raw(Base, engine, table_orm_users):
    class User_wich_autodefault(table_orm_users):
        __mapper_args__ = {'polymorphic_identity': 'users_addit'}
        created_on_bd = Column(DateTime(timezone=True), server_default=func.now())

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return User_wich_autodefault


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
def table_orm_emploee(Base, engine):
    class Employee(Base):
        __tablename__ = 'employees'
        id = Column(Integer(), primary_key=True)
        manager_id = Column(Integer(), ForeignKey('employees.id'))
        name = Column(String(255), nullable=False)
        manager = relationship("Employee", backref=backref('reports'),
                remote_side=[id])

    Base.metadata.create_all(engine)

    return Employee

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

    return SomeDataClass

