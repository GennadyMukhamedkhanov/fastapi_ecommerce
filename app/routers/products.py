from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_seller
from app.db_depends import get_async_db
from app.models import ProductModel, CategoryModel, User
from app.schemas import ProductSchema, ProductUpdate
from app.services.products import get_all_products, create_product, get_products_by_category

# Создаём маршрутизатор для товаров
router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_all_products(products: list[ProductModel] = Depends(get_all_products)):
    """
    Возвращает список всех активных товаров.


    """
    return products


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel = Depends(create_product)):
    """
    Создаёт новый товар.
    """

    return product


@router.get("/category/{category_id}", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_products_by_category(products: list[ProductModel] = Depends(get_products_by_category)):
    """
    Возвращает список товаров в указанной категории по её ID.
    """

    return products


@router.get("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    product = (await db.scalars(stmt)).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Products not found')
    return product


@router.put("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def update_product(
        product_id: int,
        product_update: ProductUpdate,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_seller)
):
    """
    Обновляет товар по его ID.
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id)
    product = (await db.scalars(stmt)).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Products not found')
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own products")
    if product_update.category_id is not None:
        stmt = select(CategoryModel).where(CategoryModel.id == product_update.category_id,
                                           CategoryModel.is_active == True)
        category = (await db.scalars(stmt)).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Category with id {product_update.category_id} not found')

    update_data = product_update.model_dump(exclude_unset=True)
    result = await db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(**update_data)
        .returning(ProductModel)
    )
    db_product = result.scalar_one()
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int,
                         db: AsyncSession = Depends(get_async_db),
                         current_user: User = Depends(get_current_seller)
                         ):
    """
    Удаляет товар по его ID.
    """

    stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active.is_(True))
    product = (await db.scalars(stmt)).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Products not found')
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can only delete your own products')
    await db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(is_active=False)
    )
    await db.commit()
    await db.refresh(product)
    return None
