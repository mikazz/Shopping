from sqlalchemy import String, Text, Column, Integer, Boolean
from shopping.db_session import SqlAlchemyBase


class BaseSerializer:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ShoppingList(SqlAlchemyBase, BaseSerializer):
    __tablename__ = 'ShoppingList'
    id = Column(Integer, primary_key=True)
    owner = Column(String(64), unique=True)
    #product_id = Column(Integer, ForeignKey('products.id'))  # FK


class Product(SqlAlchemyBase, BaseSerializer):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    descr = Column(Text, unique=False, nullable=True)
    #shopping_list_items = relationship('ShoppingList', backref='Product')
    is_purchased = Column(Boolean)
