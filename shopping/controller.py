import logging
from flask import abort
from typing import Any
from shopping import db_session
from sqlalchemy import delete
from shopping.models import ShoppingList, Product
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.ext.serializer import dumps
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
    #return [dumps(shopping_list) for shopping_list in shopping_lists]



def get_shopping_list(owner: str):
    session = db_session.create_session()
    # session.query(ShoppingList).filter_by(**{"owner":"Mike"}).all()
    # return session.query(ShoppingList).filter(ShoppingList.owner == owner).first()
    try:
        shopping_list = session.query(ShoppingList).filter_by(**{"owner": owner}).one()
    except MultipleResultsFound as e:
        abort(500, "Database constrains error")
    except NoResultFound as e:
        abort(404, "No such shopping list")
    else:
        return shopping_list
    return abort(500, "Unknown error")


def add_shopping_list(new_shopping_list: dict) -> None:
    """Add shopping list"""
    session = db_session.create_session()
    owner = new_shopping_list["owner"]
    existing_shopping_list = session.query(ShoppingList).filter_by(**{"owner": owner}).all()
    if existing_shopping_list:
        abort(400, f"Shopping List with owner: {owner} already exists")

    shopping_list = ShoppingList(owner=owner)
    session.add(shopping_list)
    try:
        session.commit()
    except IntegrityError:
        abort(400)
    except SQLAlchemyError:
        abort(400, "Cant add new shopping list")
    else:
        logger.debug(f"Added new shopping list {shopping_list.owner}")


def update_shopping_list():
    """Add shopping list"""
    pass


def delete_shopping_list(owner: str) -> None:
    """Delete shopping list"""
    session = db_session.create_session()
    #session.query(ShoppingList).filter_by(**{"owner": owner}).delete()
    #session.delete(ShoppingList).filter_by(**{"owner": owner})
    session.query(ShoppingList).filter(ShoppingList.owner == owner).delete()
    session.commit()


def get_product():
    pass


def update_product():
    pass


def delete_product():
    pass


def set_product_purchased():
    pass