from fastapi import APIRouter, status, Depends

from app.models import Reviews
from app.schemas import ReviewsSchema
from app.services.reviews import (create_review_services, get_all_reviews_services, get_product_reviews_services,
                                  delete_review_services)

# Создаём маршрутизатор для отзывов
router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.get("/", response_model=list[ReviewsSchema], status_code=status.HTTP_200_OK)
async def get_all_reviews(reviews: list[Reviews] = Depends(get_all_reviews_services)):
    """
    Возвращает список всех комментариев.

    :returns: Список комментариев
    :rtype: List[ReviewsSchema]
    """
    return reviews


@router.get("/products/{product_id}/reviews/", response_model=list[ReviewsSchema], status_code=status.HTTP_200_OK)
async def get_product_reviews(reviews: list[Reviews] = Depends(get_product_reviews_services)):
    """
    Возвращает список всех комментариев для указанного товара по его ID.

    :returns: Список комментариев
    :rtype: List[ReviewsSchema]
    """
    return reviews


@router.post("/", response_model=ReviewsSchema, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewsSchema = Depends(create_review_services)):
    """
    Создаёт новый комментарий.
    """
    return review


@router.delete("/reviews/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(review: ReviewsSchema = Depends(delete_review_services)):
    """
    Удаляет отзыв по его идентификатору (мягкое удаление, поле is_active=True -> False).

    :param review_id: ID удаляемого отзыва

    :return: удаленный отзыв
    :rtype: ReviewsSchema
    """
    return review
