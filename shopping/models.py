from shopping.db_session import SqlAlchemyBase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class SerializerMixin:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ShoppingList(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'ShoppingList'
    id = Column(Integer, primary_key=True)
    owner = Column(String(64), unique=True)
    product_items = relationship('Product', backref='ShoppingList')


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    descr = Column(Text, unique=False, nullable=True)
    shopping_list_id = Column(Integer, ForeignKey('ShoppingList.id'))  # FK
    is_purchased = Column(Boolean)
