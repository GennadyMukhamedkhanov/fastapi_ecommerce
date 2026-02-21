from fastapi import status, HTTPException
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ProductModel, CategoryModel, User
from app.repositories.common import CommonRepository
from app.schemas import ProductCreate, CategoryCreate


class CategoryRepository(CommonRepository):
    model = CategoryModel

    async def get_all_active_categories(self, db: AsyncSession):
        stmt = select(self.model).where(self.model.is_active.is_(True))
        result = await db.execute(stmt)
        categories = result.scalars().all()
        return categories

    async def create_category(self, db: AsyncSession, category):
        # Проверка существования parent_id, если указан

        if category.parent_id is not None:
            stmt = select(self.model).where(self.model.id == category.parent_id,
                                            self.model.is_active.is_(True))
            result = await db.execute(stmt)
            parent = result.scalars().first()
            if parent is None:
                raise HTTPException(status_code=400, detail="Parent category not found")

        # Создание новой категории
        db_category = self.model(**category.model_dump(), is_active=True)
        db.add(db_category)
        await db.commit()
        await db.refresh(db_category)
        return db_category

    async def update_category(self,
                              db: AsyncSession,
                              category_id: int,
                              category: CategoryCreate
                              ):
        # Проверяем существование категории
        stmt = select(self.model).where(self.model.id == category_id,
                                        self.model.is_active.is_(True))
        result = await db.execute(stmt)
        db_category = result.scalars().first()
        if not db_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        # Проверяем parent_id, если указан
        if category.parent_id is not None:
            stmt = select(self.model).where(self.model.id == category.parent_id,
                                            self.model.is_active.is_(True))
            result = await db.execute(stmt)
            parent = result.scalars().first()
            if not parent:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parent category not found")
            if parent.id == category_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category cannot be its own parent")

        # Обновляем категорию
        update_data = category.model_dump(exclude_unset=True)
        stmt = update(self.model).where(self.model.id == category_id).values(**update_data).returning(self.model)
        result = await db.execute(stmt)
        category = result.scalar_one()
        await db.commit()
        return category

    async def delete_category(self,
                              db: AsyncSession,
                              category_id: int,
                              ):
        # Проверяем существование категории
        stmt = select(self.model).where(self.model.id == category_id,
                                        self.model.is_active.is_(True))
        result = await db.execute(stmt)
        db_category = result.scalars().first()
        if not db_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        # Мягкое удаление категории
        stmt = update(self.model).where(self.model.id == category_id).values(is_active=False)
        await db.execute(stmt)
        await db.commit()
