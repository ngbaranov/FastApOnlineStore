from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import CreateTable
from app.baskend.db import Base
from app.models.products_mod import *

class Category(Base):
    __tablename__ = "categories"

    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column()
    slug: Mapped[str | None] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool | None] = mapped_column(default=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category_mod")


print(CreateTable(Category.__table__))
