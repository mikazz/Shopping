import logging
from flask import abort, jsonify
from typing import Any
from shopping import db_session
from shopping.models import ShoppingList, Product
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

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


def get_shopping_list(owner: str):
    session = db_session.create_session()
    return session.query(ShoppingList).filter(ShoppingList.owner == owner).first()


def add_shopping_list(new_shopping_list: dict):
    """Add shopping list"""
    logger.debug("Adding new shopping list")
    session = db_session.create_session()
    owner = new_shopping_list["owner"]
    shopping_list = ShoppingList(owner=owner)
    session.add(shopping_list)
    try:
        session.commit()
    except IntegrityError:
        abort(404)
    except SQLAlchemyError:
        abort(404)


def update_shopping_list():
    """Add shopping list"""
    pass


def delete_shopping_list():
    """Add shopping list"""
    pass


def get_product():
    pass


def update_product():
    pass


def delete_product():
    pass


