from fastapi import status, HTTPException
from sqlalchemy import select, insert
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

        # db_product = ProductModel(**product.model_dump(), seller_id=current_user.id)
        stmt = insert(self.model).values(**product.model_dump()).returning(self.model)
        db_product = await db.execute(stmt)
        # db.add(db_product)
        # await db.commit()
        # await db.refresh(db_product)
        return db_product


'''
ProductRepository в app/repositories/products.py наследуется от CommonRepository и определяет model = ProductModel.
 Метод get_all_active_products строит запрос select(ProductModel).where(is_active=True), 
 исполняет его в сессии и извлекает все записи через scalars().all(). 
 Это позволяет легко расширять запросы для конкретных моделей.
'''
