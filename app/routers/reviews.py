from fastapi import APIRouter, status, Depends

from app.models import ProductModel
from app.schemas import ProductSchema
from app.services.products import (get_all_products_services, create_product_services,
                                   get_products_by_category_services,
                                   get_product_services, update_product_services, delete_product_services)

# Создаём маршрутизатор для отзывов
router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel = Depends(create_product_services)):
    """
    Создаёт новый товар.
    """
