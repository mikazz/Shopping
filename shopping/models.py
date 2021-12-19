from sqlalchemy import String, Text, Column, Integer, ForeignKey, Boolean, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('sqlite:///sqlalchemy_example.db')

#Base = declarative_base()

from database import db


#class ShoppingList(Base):
class ShoppingList(db.Model):
    __tablename__ = 'ShoppingList'
    id = Column(Integer, primary_key=True)
    owner = Column(String(64), unique=True)
    #product_id = Column(Integer, ForeignKey('products.id'))  # FK


#class Product(Base):
class Product(db.Model):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    descr = Column(Text, unique=False, nullable=True)
    #shopping_list_items = relationship('ShoppingList', backref='Product')
    is_purchased = Column(Boolean)


#Base.metadata.create_all(engine)