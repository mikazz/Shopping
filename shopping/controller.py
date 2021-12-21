import logging
from flask import abort
from typing import Any
from shopping import db_session
from shopping.models import ShoppingList, Product
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
logger = logging.getLogger(__name__)


def healthcheck() -> Any:
    """Server healthcheck"""
    _logger = logger.getChild("healthcheck")
    _logger.info("OK")
    return {"status": "OK"}


def get_shopping_lists():
    """Return all shopping lists"""
    session = db_session.create_session()
    shopping_lists = session.query(ShoppingList).all()
    return [i.as_dict() for i in shopping_lists]


def get_db_shopping_list(owner: str):
    session = db_session.create_session()
    shopping_list = session.query(ShoppingList).filter_by(**{"owner": owner}).one()
    return shopping_list


def get_shopping_list(owner: str):
    try:
        shopping_list = get_db_shopping_list(owner)
    except NoResultFound:
        abort(404, "No such shopping list")
    else:
        return shopping_list.as_dict()


def add_shopping_list(new_shopping_list: dict) -> None:
    """Add shopping list"""
    session = db_session.create_session()
    owner = new_shopping_list["owner"]
    try:
        get_db_shopping_list(owner)
    except NoResultFound:
        pass
    else:
        abort(400, f"Shopping List with owner: {owner} already exists")

    shopping_list = ShoppingList(owner=owner)
    session.add(shopping_list)
    try:
        session.commit()
    except SQLAlchemyError:
        abort(400, "Cant add new shopping list")
    else:
        logger.debug(f"Added new shopping list: {shopping_list.owner}")


def update_shopping_list(owner: str, update_shopping_list_information: dict):
    """Update shopping list"""
    session = db_session.create_session()
    session.query(ShoppingList).filter(ShoppingList.owner == owner).update(update_shopping_list_information)
    session.commit()


def delete_shopping_list(owner: str) -> None:
    """Delete shopping list"""
    session = db_session.create_session()
    session.query(ShoppingList).filter(ShoppingList.owner == owner).delete()
    session.commit()


def get_db_product(name: str):
    """Get DB Product"""
    session = db_session.create_session()
    product = session.query(Product).filter_by(**{"name": name}).one()
    return product


def get_product(name: str):
    """Get Product"""
    try:
        product = get_db_product(name)
    except NoResultFound as e:
        abort(404, "No such shopping list")
    else:
        return product.as_dict()


def get_db_products():
    session = db_session.create_session()
    return session.query(Product).all()


def get_products():
    products = get_db_products()
    return [product.as_dict() for product in products]


def add_product(new_product: dict):
    session = db_session.create_session()
    name = new_product["name"]
    owner = new_product["owner"]
    descr = new_product["descr"]
    is_purchased = new_product["is_purchased"]
    try:
        shopping_list = get_db_shopping_list(owner)
    except NoResultFound:
        abort(404, f"No such shopping list for {owner}")
    else:
        product = Product(name=name, descr=descr, shopping_list_id=shopping_list.id, is_purchased=is_purchased)
        session.add(product)
        session.commit()


def update_product(name: str, update_product_information: dict):
    session = db_session.create_session()
    session.query(Product).filter(Product.name == name).update(update_product_information)
    session.commit()


def delete_product(name: str):
    session = db_session.create_session()
    session.query(Product).filter(Product.name == name).delete()
    session.commit()
