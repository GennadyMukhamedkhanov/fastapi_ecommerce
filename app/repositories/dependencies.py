from app.repositories.categories import CategoryRepository
from app.repositories.products import ProductRepository
from app.repositories.reviews import ReviewRepository


async def get_product_repository() -> ProductRepository:
    """
    Возвращает репозиторий продукта.
    """
    return ProductRepository()


async def get_category_repository() -> CategoryRepository:
    """
    Возвращает репозиторий продукта.
    """
    return CategoryRepository()




async def get_review_repository() -> ReviewRepository:
    """
    Возвращает репозиторий комментария.
    """
    return ReviewRepository()
