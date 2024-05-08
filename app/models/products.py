from app.baskend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from app.models import *


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    stock = Column(Integer)
    supplier_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    rating = Column(Float, default=1.0)
    is_active = Column(Boolean, default=True)

    category = relationship('Category', back_populates='products')

    reviews = relationship("Review", collection_class=set)

from sqlalchemy.schema import CreateTable
print(CreateTable(Product.__table__))
