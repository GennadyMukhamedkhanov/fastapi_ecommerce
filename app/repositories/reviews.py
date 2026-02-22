from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ProductModel, User, Reviews
from app.repositories.common import CommonRepository
from app.schemas import ReviewsCreate


class ReviewRepository(CommonRepository):
    model = Reviews

    async def create_review(self,
                            db: AsyncSession,
                            review_data: ReviewsCreate,
                            current_user: User) -> Reviews:
        """
        Создаёт новый отзыв к товару.

        :param db: Сессия к базе данных.
        :param review_data: Модель для создания отзыва.
        :param current_user: Пользователь, который оставляет отзыв.
        :return: Созданный отзыв.
        :raises HTTPException: If product with given id is not found or inactive, or if user has already reviewed this product.
        """
        stmt = select(ProductModel).where(ProductModel.id == review_data.product_id,
                                          ProductModel.is_active.is_(True))
        result = await db.execute(stmt)
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Product with id {review_data.product_id} not found or inactive')

        stmt = select(self.model).where(self.model.product_id == review_data.product_id,
                                        self.model.user_id == current_user.id,
                                        self.model.is_active.is_(True))
        result = await db.execute(stmt)
        review = result.scalars().first()

        if review:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='You have already reviewed this product')

        db_review = self.model(**review_data.model_dump(exclude_unset=True),
                               user_id=current_user.id)
        db.add(db_review)
        await db.commit()
        await db.refresh(db_review)

        return db_review
