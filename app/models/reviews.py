from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import String, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GradeEnum(int, PyEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Reviews(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str | None] = mapped_column(String(500), nullable=True)
    comment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    grade: Mapped[GradeEnum] = mapped_column(Enum(GradeEnum, native_enum=False), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'), nullable=False)

    author: Mapped['User'] = relationship('User', back_populates='reviews')
    product: Mapped['ProductModel'] = relationship('ProductModel', back_populates='reviews')

