import unittest
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from shopping.controller import add_shopping_list
from shopping.models import Product, ShoppingList
from database import db


import unittest
from database import db
from shopping.models import Product, ShoppingList
from server import generate_app


class Case(unittest.TestCase):
    def setUp(self):
        app = generate_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite'
        db.create_all()

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()

    def test_create_new_shopping_list(self):
        shopping_list = ShoppingList(owner="Steve")
        db.session.add(shopping_list)
        db.session.commit()
        one_shopping_list = ShoppingList.query.first()
        self.assertEqual(one_shopping_list.owner, "Steve")
        add_shopping_list()


# class TestBasic(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         pass
#
#     def test_create_new_shopping_list(self):
#         shopping_list = ShoppingList(owner="Steve")
#         db.session.add(shopping_list)
#         db.session.commit()

