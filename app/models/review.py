from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.baskend.db import Base
from app.models import *


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    comment: Mapped[str | None]
    comment_date: Mapped[date | None]
    rating: Mapped[int | None] = mapped_column(default=0)
    is_active: Mapped[bool | None] = mapped_column(default=True)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    product: Mapped["Product"] = relationship(back_populates="reviews")
