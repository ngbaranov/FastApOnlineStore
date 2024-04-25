from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import CreateTable
from app.baskend.db import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str | None]
    slug: Mapped[str | None] = mapped_column(unique=True, index=True)
    description: Mapped[str | None]
    price: Mapped[int | None]
    image_url: Mapped[str | None]
    stock: Mapped[int | None]
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    rating: Mapped[float | None]
    is_active: Mapped[bool | None]

    category: Mapped["Category"] = relationship(back_populates="products_mod")


class Category(Base):
    __tablename__ = "categories"

    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column()
    slug: Mapped[str | None] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool | None] = mapped_column(default=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category_mod")


print(CreateTable(Category.__table__))