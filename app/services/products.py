from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_seller
from app.db_depends import get_async_db
from app.models import User
from app.repositories.dependencies import get_product_repository
from app.repositories.products import ProductRepository
from app.schemas import ProductCreate, ProductUpdate
from app.services.enum import UserRoles


async def get_all_products_services(db: AsyncSession = Depends(get_async_db),
                                    products_repo: ProductRepository = Depends(get_product_repository)):
    product = await products_repo.get_all_active_products(db)
    return product


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
