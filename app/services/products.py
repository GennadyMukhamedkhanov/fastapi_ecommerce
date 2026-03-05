from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_seller
from app.db_depends import get_async_db
from app.models import User, ProductModel
from app.repositories.dependencies import get_product_repository, get_sort_params
from app.repositories.products import ProductRepository
from app.schemas import (ProductCreate, ProductUpdate, ProductList, ProductOut, SortParams, SortOrderEnum,
                         SortFieldEnum,
                         PageValidateSchema, ProductFilterParamsSchema)
from app.services.enum import UserRoles
from typing import Annotated


async def get_all_products_services(pagination_params: Annotated[PageValidateSchema, Depends()],
                                    db: Annotated[AsyncSession, Depends(get_async_db)],
                                    filters: Annotated[ProductFilterParamsSchema, Depends()],
                                    sort_params: Annotated[SortParams, Depends(get_sort_params)],
                                    products_repo: Annotated[ProductRepository, Depends(get_product_repository)]
                                    ):
    """
    Возвращает список товаров с учетом фильтров и сортировки.

    :param pagination_params: Параметры пагинации.
    :param db: Сессия к базе данных.
    :param filters: Фильтры для товаров.
    :param sort_params: Параметры сортировки.
    :param products_repo: Репозиторий для работы с товарами.

    :return: Список товаров в виде ProductList.
    """

    # Проверка логики min_price <= max_price
    validate_price_range(filters.min_price, filters.max_price)

    # Формируем список фильтров
    filters = get_list_filters(filters.category_id,
                               filters.min_price,
                               filters.max_price,
                               filters.in_stock,
                               filters.seller_id)

    # Применяем сортировку
    order_sorting_list = get_order_sorting_list(sort_params)

    data = await products_repo.get_all_active_products(db,
                                                       pagination_params.page,
                                                       pagination_params.page_size,
                                                       filters,
                                                       order_sorting_list
                                                       )
    data['items'] = [ProductOut.model_validate(product) for product in data['items']]
    return ProductList(**data)


def validate_price_range(min_price: float | None, max_price: float | None) -> None:
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price не может быть больше max_price")


def get_list_filters(category_id, min_price, max_price, in_stock, seller_id):
    filters = [ProductModel.is_active.is_(True)]

    if category_id is not None:
        filters.append(ProductModel.category_id == category_id)
    if min_price is not None:
        filters.append(ProductModel.price >= min_price)
    if max_price is not None:
        filters.append(ProductModel.price <= max_price)
    if in_stock is not None:
        filters.append(ProductModel.stock > 0 if in_stock else ProductModel.stock == 0)
    if seller_id is not None:
        filters.append(ProductModel.seller_id == seller_id)
    return filters


def get_order_sorting_list(sort_params: SortParams):
    order_clauses = []

    # Добавляем основную сортировку
    column = getattr(ProductModel, sort_params.field)
    if sort_params.order == SortOrderEnum.desc:
        order_clauses.append(column.desc())
    else:
        order_clauses.append(column.asc())

    # Добавляем сортировку по ID для стабильности
    if sort_params.field != SortFieldEnum.id:
        order_clauses.append(ProductModel.id)

    return order_clauses


async def create_product_services(
        product_data: ProductCreate,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_seller),
        products_repo: ProductRepository = Depends(get_product_repository),
):
    if current_user.role != UserRoles.SELLER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can perform this action")

    product = await products_repo.create_product(db, product_data, current_user)
    return product


async def get_products_by_category_services(pagination_params: Annotated[PageValidateSchema, Depends()],
                                            filters: Annotated[ProductFilterParamsSchema, Depends()],
                                            sort_params: Annotated[SortParams, Depends(get_sort_params)],
                                            category_id: Annotated[int, Path(gt=0)],
                                            db: Annotated[AsyncSession, Depends(get_async_db)],
                                            products_repo: Annotated[
                                                ProductRepository, Depends(get_product_repository)]):
    # Проверка логики min_price <= max_price
    validate_price_range(filters.min_price, filters.max_price)

    # Формируем список фильтров
    filters = get_list_filters(filters.category_id,
                               filters.min_price,
                               filters.max_price,
                               filters.in_stock,
                               filters.seller_id)

    # Применяем сортировку
    order_sorting_list = get_order_sorting_list(sort_params)

    data = await products_repo.get_products_by_category_id(db,
                                                           category_id,
                                                           pagination_params.page,
                                                           pagination_params.page_size,
                                                           filters,
                                                           order_sorting_list)

    data['items'] = [ProductOut.model_validate(product) for product in data['items']]
    return ProductList(**data)


async def get_product_services(product_id: int,
                               db: AsyncSession = Depends(get_async_db),
                               products_repo: ProductRepository = Depends(get_product_repository)
                               ):
    product = await products_repo.get_product_id(db, product_id)
    return product


async def update_product_services(product_id: Annotated[int, Path(gt=0)],
                                  product_update: Annotated[ProductUpdate, Depends()],
                                  db: Annotated[AsyncSession, Depends(get_async_db)],
                                  current_user: Annotated[User, Depends(get_current_seller)],
                                  products_repo: Annotated[ProductRepository, Depends(get_product_repository)]
                                  ):
    product = await products_repo.update_product(db, product_id, product_update, current_user)
    return product


async def delete_product_services(product_id: int,
                                  db: AsyncSession = Depends(get_async_db),
                                  current_user: User = Depends(get_current_seller),
                                  products_repo: ProductRepository = Depends(get_product_repository)
                                  ):
    product = await products_repo.delete_product(db, product_id, current_user)
    return product
