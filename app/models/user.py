from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.baskend.db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str | None] = mapped_column()
    last_name: Mapped[str | None] = mapped_column()
    username: Mapped[str | None] = mapped_column(unique=True)
    email: Mapped[str | None] = mapped_column(unique=True)
    hashed_password: Mapped[str | None] = mapped_column()
    is_active: Mapped[bool | None] = mapped_column(default=True)
    is_admin: Mapped[bool | None] = mapped_column(default=False)
    is_supplier: Mapped[bool | None] = mapped_column(default=False)
    is_customer: Mapped[bool | None] = mapped_column(default=True)
