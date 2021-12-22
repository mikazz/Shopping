from werkzeug.exceptions import Conflict, NotFound


class ShoppingListAlreadyExistsUnderThisOwner(Conflict):
    description = None


class ShoppingListNotFound(NotFound):
    description = "Shopping list not found"


class ProductNotFound(NotFound):
    description = "Product not found"

