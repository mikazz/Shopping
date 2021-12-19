import logging
from typing import Any
from database import db
from shopping.models import ShoppingList, Product

logger = logging.getLogger(__name__)


def error(message: str) -> dict:
    _logger = logger.getChild("error")
    _logger.info(f"Returning error: {message}")
    return {"error": message}


def healthcheck() -> Any:
    """Server healthcheck"""
    _logger = logger.getChild("healthcheck")
    _logger.info("OK")
    return {"status": "OK"}


# def get_invoices() -> Any:
#     """Get all invoices"""
#     pass
#     #return Invoice.objects.to_json()


def get_shopping_lists():
    """Return all shopping lists"""
    pass


def add_shopping_list():
    """Add shopping list"""
    shopping_list = ShoppingList(owner="Steve")
    db.session.add(shopping_list)
    db.session.commit()


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


