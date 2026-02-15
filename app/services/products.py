from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_seller
from app.db_depends import get_async_db
from app.models import User
from app.repositories.dependencies import get_product_repository
from app.repositories.products import ProductRepository
from app.schemas import ProductCreate


async def get_all_products(db: AsyncSession = Depends(get_async_db),
                           products_repo: ProductRepository = Depends(get_product_repository)):
    product = await products_repo.get_all_active_products(db)
    return product


async def create_product(
        product_data: ProductCreate,  # ← из тела запроса
        db: AsyncSession = Depends(get_async_db),
        products_repo: ProductRepository = Depends(get_product_repository),
        current_user: User = Depends(get_current_seller),
):
    product = await products_repo.create_product(db, product_data, current_user)
    return product
