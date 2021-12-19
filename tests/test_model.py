import unittest
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from shopping.models import Product, ShoppingList
from shopping.models import engine
Base = declarative_base()


class TestBasic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #engine = create_engine('sqlite:///sqlalchemy_example.db')
        # Base.metadata.create_all(engine)
        # Base.metadata.bind = engine
        db_session = sessionmaker(bind=engine)
        cls.session = db_session()

    def test_create_new_product(self):
        shopping_list = ShoppingList(owner="Steve")
        self.session.add(shopping_list)
        self.session.commit()
        #Product(name="Soap", descr="To wash", is_purchased=False)

