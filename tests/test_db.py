import unittest
from shopping import db_session
from shopping.controller import add_shopping_list, get_shopping_list
from shopping.models import ShoppingList

db_session.global_init(':memory:')
session = db_session.create_session()


class Case(unittest.TestCase):
    def setUp(self):
        pass

    def test_db_add_shopping_list(self):
        shopping_list = ShoppingList()
        shopping_list.owner = "Steve"
        session.add(shopping_list)
        session.commit()
        shopping_list = session.query(ShoppingList).filter(ShoppingList.owner == "Steve").first()
        self.assertEqual(shopping_list.owner, "Steve")

    def test_add_shopping_list(self):
        shopping_list_data = {"owner": "Mike"}
        add_shopping_list(shopping_list_data)
        shopping_list = get_shopping_list(owner="Mike")
        self.assertEqual(shopping_list.owner, "Mike")
