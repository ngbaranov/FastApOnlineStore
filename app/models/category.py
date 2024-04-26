from app.baskend.db import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models import *


class Category(Base):
    __tablename__ = 'categories'

    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    products = relationship("Product", back_populates="category")

from sqlalchemy.schema import CreateTable
print(CreateTable(Category.__table__))

