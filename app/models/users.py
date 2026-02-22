from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.services.enum import UserRoles


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    role: Mapped[UserRoles] = mapped_column(String(6), default=UserRoles.BUYER, nullable=False)

    products: Mapped[list["ProductModel"]] = relationship('ProductModel', back_populates='seller')
    reviews: Mapped[list["Reviews"]] = relationship('Reviews', back_populates='author')
