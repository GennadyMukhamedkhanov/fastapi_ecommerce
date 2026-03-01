from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_seller
from app.db_depends import get_async_db
from app.models import User, ProductModel
from app.repositories.dependencies import get_product_repository, get_sort_params
from app.repositories.products import ProductRepository
from app.schemas import ProductCreate, ProductUpdate, ProductList, ProductOut, SortParams, SortOrderEnum, SortFieldEnum
from app.services.enum import UserRoles


async def get_all_products_services(page: int = Query(1, ge=1),
                                    page_size: int = Query(20, ge=1, le=100),
                                    db: AsyncSession = Depends(get_async_db),
                                    category_id: int | None = Query(
                                        None, description="ID категории для фильтрации"),
                                    min_price: float | None = Query(
                                        None, ge=0, description="Минимальная цена товара"),
                                    max_price: float | None = Query(
                                        None, ge=0, description="Максимальная цена товара"),
                                    in_stock: bool | None = Query(
                                        None, description="true — только товары в наличии, false — только без остатка"),
                                    seller_id: int | None = Query(
                                        None, description="ID продавца для фильтрации"),
                                    sort_params: SortParams = Depends(get_sort_params),
                                    products_repo: ProductRepository = Depends(get_product_repository)
                                    ):
    """
        Возвращает список всех активных товаров с поддержкой фильтров.
        """
    # Проверка логики min_price <= max_price
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price не может быть больше max_price",
        )

    # Формируем список фильтров
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

    # Применяем сортировку
    order_clauses = []

    # Добавляем основную сортировку
    column = getattr(ProductModel, sort_params.field)
    if sort_params.order == SortOrderEnum.desc:
        order_clauses.append(column.desc())
    else:
        order_clauses.append(column.asc())

    # Всегда добавляем сортировку по ID для стабильности
    if sort_params.field != SortFieldEnum.id:
        order_clauses.append(ProductModel.id)

    data = await products_repo.get_all_active_products(db,
                                                       page,
                                                       page_size,
                                                       filters,
                                                       order_clauses
                                                       )
    data['items'] = [ProductOut.model_validate(product) for product in data['items']]
    return ProductList(**data)


async def create_product_services(
        product_data: ProductCreate,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_seller),
        products_repo: ProductRepository = Depends(get_product_repository),
):
    if current_user.role != UserRoles.seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only sellers can perform this action")
        # raise seller_forbidden_action()

    product = await products_repo.create_product(db, product_data, current_user)
    return product


async def get_products_by_category_services(category_id: int,
                                            db: AsyncSession = Depends(get_async_db),
                                            products_repo: ProductRepository = Depends(get_product_repository)):
    products = await products_repo.get_products_by_category_id(db, category_id)

    return products


async def get_product_services(product_id: int,
                               db: AsyncSession = Depends(get_async_db),
                               products_repo: ProductRepository = Depends(get_product_repository)
                               ):
    product = await products_repo.get_product_id(db, product_id)
    return product


async def update_product_services(product_id: int,
                                  product_update: ProductUpdate,
                                  db: AsyncSession = Depends(get_async_db),
                                  current_user: User = Depends(get_current_seller),
                                  products_repo: ProductRepository = Depends(get_product_repository)
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
