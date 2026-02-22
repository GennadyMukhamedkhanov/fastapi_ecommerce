from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ProductModel, CategoryModel, User
from app.repositories.common import CommonRepository
from app.schemas import ProductCreate


class ProductRepository(CommonRepository):
    model = ProductModel

    async def get_all_active_products(self, db: AsyncSession):
        stmt = select(self.model).where(self.model.is_active.is_(True))
        result = await db.execute(stmt)
        product = result.scalars().all()
        return product

    async def create_product(self,
                             db: AsyncSession,
                             product: ProductCreate,
                             current_user: User):
        stmt = select(CategoryModel).where(CategoryModel.id == product.category_id,
                                           CategoryModel.is_active.is_(True))
        category = (await db.scalars(stmt)).first()

        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Category with id {product.category_id} not found or inactive')

        db_product = self.model(**product.model_dump(), seller_id=current_user.id)
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)

        return db_product

    async def get_products_by_category_id(self,
                                          db: AsyncSession,
                                          category_id
                                          ):
        stmt = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active.is_(True))
        result = await db.execute(stmt)
        category = result.scalars().first()
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category not found or inactive')

        stmt = select(self.model).where(self.model.category_id == category_id, self.model.is_active.is_(True))
        result = await db.execute(stmt)
        products = result.scalars().all()
        return products

    async def get_product_id(self,
                             db: AsyncSession,
                             product_id: int
                             ):
        stmt = select(self.model).where(self.model.id == product_id, self.model.is_active.is_(True))
        result = await db.execute(stmt)
        product = result.scalars().first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Products not found')

        return product

    async def update_product(self,
                             db: AsyncSession,
                             product_id: int,
                             product_update,
                             current_user
                             ):
        stmt = select(self.model).where(self.model.id == product_id)
        result = await db.execute(stmt)
        product = result.scalars().first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Products not found')
        if product.seller_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own products")
        if product_update.category_id is not None:
            stmt = select(CategoryModel).where(CategoryModel.id == product_update.category_id,
                                               CategoryModel.is_active.is_(True))
            result = await db.execute(stmt)
            category = result.scalars().first()
            if not category:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'Category with id {product_update.category_id} not found')

        update_data = product_update.model_dump(exclude_unset=True)
        stmt = update(self.model).where(self.model.id == product_id).values(**update_data).returning(self.model)
        result = await db.execute(stmt)
        db_product = result.scalar_one()
        await db.commit()

        return db_product

    async def delete_product(self,
                             db: AsyncSession,
                             product_id: int,
                             current_user
                             ):
        stmt = select(self.model).where(self.model.id == product_id, self.model.is_active.is_(True))
        result = await db.execute(stmt)
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Products not found')
        if product.seller_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can only delete your own products')

        stmt = update(self.model).where(self.model.id == product_id).values(is_active=False).returning(self.model)
        result = await db.execute(stmt)
        product_db = result.scalar_one()
        await db.commit()
        await db.refresh(product_db)
        return product_db
