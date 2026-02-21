from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.db_depends import get_async_db
from app.models import User
from app.repositories.categories import CategoryRepository
from app.repositories.dependencies import get_category_repository
from app.schemas import CategoryCreate


async def get_all_categories_services(db: AsyncSession = Depends(get_async_db),
                                      category_repo: CategoryRepository = Depends(get_category_repository)):
    categories = await category_repo.get_all_active_categories(db)
    return categories


async def create_category_services(category_data: CategoryCreate,
                                   db: AsyncSession = Depends(get_async_db),
                                   category_repo: CategoryRepository = Depends(get_category_repository)
                                   ):
    category = await category_repo.create_category(db, category_data)
    return category


async def update_category_services(category_id: int,
                                   category: CategoryCreate,
                                   db: AsyncSession = Depends(get_async_db),
                                   category_repo: CategoryRepository = Depends(get_category_repository)
                                   ):
    category = await category_repo.update_category(db, category_id, category)
    return category


async def delete_category_services(category_id: int,
                                   db: AsyncSession = Depends(get_async_db),
                                   category_repo: CategoryRepository = Depends(get_category_repository)
                                   ):
    await category_repo.delete_category(db, category_id)
