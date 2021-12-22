import logging
from typing import Any, List, Optional, Tuple

from flask import jsonify
from shopping import db_session
from shopping.exceptions import (ProductNotFound,
                                 ShoppingListAlreadyExistsUnderThisOwner,
                                 ShoppingListNotFound)
from shopping.models import Product, ShoppingList
from sqlalchemy.exc import NoResultFound

logger = logging.getLogger(__name__)

FLASK_RESPONSE = Tuple[Optional[Any], int]


def healthcheck() -> Any:
    """Server healthcheck"""
    _logger = logger.getChild("healthcheck")
    _logger.info("OK")
    return {"status": "OK"}


def get_db_shopping_lists() -> List[ShoppingList]:
    """Get DB all shopping lists"""
    session = db_session.create_session()
    return session.query(ShoppingList).all()


def get_shopping_lists() -> FLASK_RESPONSE:
    """Get all shopping lists"""
    shopping_lists = get_db_shopping_lists()
    return [i.as_dict() for i in shopping_lists], 200


def get_db_shopping_list(owner: str) -> ShoppingList:
    session = db_session.create_session()
    try:
        shopping_list = session.query(ShoppingList).filter_by(**{"owner": owner}).one()
    except NoResultFound:
        raise ShoppingListNotFound
    return shopping_list


def get_shopping_list(owner: str) -> FLASK_RESPONSE:
    shopping_list = get_db_shopping_list(owner)
    return jsonify(shopping_list.as_dict()), 200


def add_shopping_list(new_shopping_list: dict) -> FLASK_RESPONSE:
    """Add shopping list"""
    session = db_session.create_session()
    owner = new_shopping_list["owner"]
    try:
        get_db_shopping_list(owner)
    except ShoppingListNotFound:
        pass
    else:
        raise ShoppingListAlreadyExistsUnderThisOwner(description=f"Shopping list already exists under this owner: {owner}")
    shopping_list = ShoppingList(owner=owner)
    session.add(shopping_list)
    session.commit()
    logger.debug(f"Added new shopping list: {shopping_list.owner}")
    return shopping_list.as_dict(), 200


def update_shopping_list(owner: str, update_shopping_list_information: dict) -> FLASK_RESPONSE:
    """Update shopping list"""
    session = db_session.create_session()
    session.query(ShoppingList).filter(ShoppingList.owner == owner).update(update_shopping_list_information)
    session.commit()
    updated_shopping_list = get_db_shopping_list(owner)
    return updated_shopping_list.as_dict(), 202


def delete_shopping_list(owner: str) -> Any:
    """Delete shopping list"""
    session = db_session.create_session()
    session.query(ShoppingList).filter(ShoppingList.owner == owner).delete()
    session.commit()
    return 200


def get_db_product(name: str) -> Product:
    """Get DB Product"""
    session = db_session.create_session()
    try:
        product = session.query(Product).filter_by(**{"name": name}).one()
    except NoResultFound:
        raise ProductNotFound
    return product


def get_product(name: str) -> FLASK_RESPONSE:
    """Get Product"""
    product = get_db_product(name)
    return product.as_dict(), 200


def get_db_products() -> List[Product]:
    """Get Db Products"""
    session = db_session.create_session()
    return session.query(Product).all()


def get_products() -> FLASK_RESPONSE:
    """Get Products"""
    products = get_db_products()
    return jsonify([product.as_dict() for product in products]), 200


def add_product(new_product: dict) -> FLASK_RESPONSE:
    """Add Product to collection"""
    session = db_session.create_session()
    product = Product(**new_product)
    session.add(product)
    session.commit()
    return product.as_dict(), 200


def update_product(name: str, update_product_information: dict) -> FLASK_RESPONSE:
    """Update Product"""
    session = db_session.create_session()
    session.query(Product).filter(Product.name == name).update(update_product_information)
    session.commit()
    updated_product = get_db_product(name)
    return updated_product.as_dict(), 202


def delete_product(name: str) -> Any:
    """Delete Product"""
    session = db_session.create_session()
    session.query(Product).filter(Product.name == name).delete()
    session.commit()
    logger.debug(f"Deleted product: {name}")
    return 200