import unittest

from shopping import db_session
from shopping.controller import (add_product, add_shopping_list,
                                 delete_product, delete_shopping_list,
                                 get_db_product, get_db_shopping_list,
                                 get_db_shopping_lists, update_product)
from shopping.exceptions import ProductNotFound


class TestDataModel(unittest.TestCase):
    def setUp(self):
        db_session.global_init('sqlite:///:memory:?check_same_thread=False')
        shopping_list_data = {"owner": "Steve"}
        add_shopping_list(shopping_list_data)
        self.common_shopping_list = get_db_shopping_list(owner="Steve")

    def tearDown(self) -> None:
        delete_shopping_list("Steve")
        db_session.close_session()

    def test_count_create_multiple_shopping_lists(self):
        add_shopping_list({"owner": "Mike"})
        add_shopping_list({"owner": "Harry"})
        add_shopping_list({"owner": "Barry"})
        all_shopping_lists = get_db_shopping_lists()
        self.assertEqual(len(all_shopping_lists), 4)
        delete_shopping_list("Mike")
        delete_shopping_list("Harry")
        delete_shopping_list("Barry")

    def test_remove_shopping_lists(self):
        add_shopping_list({"owner": "Jack"})
        all_shopping_lists = get_db_shopping_lists()
        self.assertEqual(2, len(all_shopping_lists))
        delete_shopping_list("Jack")
        all_shopping_lists = get_db_shopping_lists()
        self.assertEqual(1, len(all_shopping_lists))
        delete_shopping_list("Steve")
        all_shopping_lists = get_db_shopping_lists()
        self.assertEqual(len(all_shopping_lists), 0)

    def test_set_product_as_purchased(self):
        shopping_list_data = {"owner": "Larry"}
        add_shopping_list(shopping_list_data)
        shopping_list = get_db_shopping_list(owner="Larry")
        new_product = {"name": "Milk",
                       "descr": "1L",
                       "shopping_list_id": shopping_list.id,
                       "is_purchased": True
                       }
        add_product(new_product)
        update_product("Milk", {"is_purchased": False})
        product_after = get_db_product("Milk")
        self.assertEqual(product_after.is_purchased, False)
        update_product("Milk", {"is_purchased": True})
        product_after = get_db_product("Milk")
        self.assertEqual(product_after.is_purchased, True)

    def test_delete_product(self):
        new_product = {"name": "Soda",
                       "descr": "0.5L",
                       "shopping_list_id": self.common_shopping_list.id,
                       "is_purchased": False
                       }
        add_product(new_product)
        product = get_db_product("Soda")
        self.assertEqual(product.name, "Soda")
        self.assertEqual(product.descr, "0.5L")
        self.assertEqual(product.shopping_list_id, self.common_shopping_list.id)
        self.assertEqual(product.is_purchased, False)
        delete_product(product.name)
        with self.assertRaises(ProductNotFound):
            get_db_product("Soda")

    def test_update_product(self):
        new_product = {"name": "Water",
                       "descr": "0.5L",
                       "shopping_list_id": self.common_shopping_list.id,
                       "is_purchased": False
                       }
        add_product(new_product)
        product = get_db_product("Water")
        self.assertEqual(product.descr, "0.5L")
        update_product("Water", {"descr": "1.0L"})
        product = get_db_product("Water")
        self.assertEqual(product.descr, "1.0L")

    def test_assign_product_to_shopping_list(self):
        new_product = {"name": "Juice",
                       "descr": "0.5L",
                       "shopping_list_id": self.common_shopping_list.id,
                       "is_purchased": False
                       }
        add_product(new_product)
        product_before = get_db_product("Juice")
        self.assertEqual(product_before.descr, "0.5L")
        update_product("Juice", {"descr": "1.0L"})
        product_after = get_db_product("Juice")
        self.assertEqual(product_after.descr, "1.0L")
