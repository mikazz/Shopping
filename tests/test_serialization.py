import unittest

from server import generate_test_client
from shopping import db_session
from shopping.controller import add_shopping_list, get_shopping_list
from shopping.models import ShoppingList

db_session.global_init(':memory:')
session = db_session.create_session()


class Case(unittest.TestCase):
    def setUp(self):
        tc = generate_test_client()

    def test_db_add_shopping_list(self):
        shopping_list = ShoppingList()
        shopping_list.owner = "Steve"
        session.add(shopping_list)
        session.commit()
        shopping_list = session.query(ShoppingList).filter(ShoppingList.owner == "Steve").first()
