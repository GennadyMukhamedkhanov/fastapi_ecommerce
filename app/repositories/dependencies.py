from fastapi import Query

from app.repositories.categories import CategoryRepository
from app.repositories.products import ProductRepository
from app.repositories.reviews import ReviewRepository
from app.schemas import SortFieldEnum, SortOrderEnum, SortParams


async def get_product_repository() -> ProductRepository:
    """
    Возвращает репозиторий продукта.
    """
    return ProductRepository()


async def get_category_repository() -> CategoryRepository:
    """
    Возвращает репозиторий категории.
    """
    return CategoryRepository()


async def get_review_repository() -> ReviewRepository:
    """
    Возвращает репозиторий комментария.
    """
    return ReviewRepository()


# Зависимость для получения параметров сортировки
async def get_sort_params(
        field: SortFieldEnum = Query(SortFieldEnum.id, description="Поле для сортировки"),
        order: SortOrderEnum = Query(SortOrderEnum.asc, description="Направление сортировки")
) -> SortParams:
    return SortParams(field=field, order=order)
