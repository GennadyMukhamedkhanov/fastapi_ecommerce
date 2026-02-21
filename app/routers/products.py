from fastapi import APIRouter, status, Depends

from app.models import ProductModel
from app.schemas import ProductSchema
from app.services.products import (get_all_products_services, create_product_services,
                                   get_products_by_category_services,
                                   get_product_services, update_product_services, delete_product_services)

# Создаём маршрутизатор для товаров
router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_all_products(products: list[ProductModel] = Depends(get_all_products_services)):
    """
    Возвращает список всех активных товаров.


    """
    return products


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel = Depends(create_product_services)):
    """
    Создаёт новый товар.
    """

    return product


@router.get("/category/{category_id}", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_products_by_category(products: list[ProductModel] = Depends(get_products_by_category_services)):
    """
    Возвращает список товаров в указанной категории по её ID.
    """

    return products


@router.get("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product(product: ProductModel = Depends(get_product_services)):
    """
    Возвращает детальную информацию о товаре по его ID.
    """

    return product


@router.put("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def update_product(product: ProductModel = Depends(update_product_services)):
    """
    Обновляет товар по его ID.
    """
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product=Depends(delete_product_services)):
    """
    Удаляет товар по его ID.
    """

    return None
