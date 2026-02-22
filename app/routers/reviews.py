from fastapi import APIRouter, status, Depends

from app.models import Reviews
from app.schemas import ReviewsSchema
from app.services.reviews import create_review_services

# Создаём маршрутизатор для отзывов
router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.post("/", response_model=ReviewsSchema, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewsSchema = Depends(create_review_services)):
    """
    Создаёт новый комментарий.
    """
    return review
