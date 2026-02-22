from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.db_depends import get_async_db
from app.models import User
from app.repositories.dependencies import get_review_repository
from app.repositories.reviews import ReviewRepository
from app.schemas import ReviewsCreate, ReviewsSchema


async def create_review_services(
        review_data: ReviewsCreate,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user),
        reviews_repo: ReviewRepository = Depends(get_review_repository),
):
    """
        Создаёт новый комментарий.
        Возвращает созданный комментарий.

        :param review_data: Модель для создания комментария.
        :param db: Сессия к базе данных.
        :param current_user: Пользователь, который оставляет комментарий.
        :param reviews_repo: Репозиторий для работы с комментариями.
        :return: Созданный комментарий.
    """
    db_review = await reviews_repo.create_review(db, review_data, current_user)

    # 2. Загружаем связанные данные (автора и продукт)
    await db.refresh(db_review, ['author', 'product'])

    # 3. Формируем ответ со всеми полями
    return ReviewsSchema(
        id=db_review.id,
        comment=db_review.comment,
        comment_date=db_review.comment_date,
        grade=db_review.grade,
        is_active=db_review.is_active,
        user_id=db_review.user_id,
        product_id=db_review.product_id,
        author_name=db_review.author.email if db_review.author else None,
        product_name=db_review.product.name if db_review.product else None
    )
