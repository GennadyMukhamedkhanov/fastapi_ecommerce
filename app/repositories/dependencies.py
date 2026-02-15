from app.repositories.products import ProductRepository


async def get_product_repository() -> ProductRepository:
    """
    Возвращает репозиторий продукта.
    """
    return ProductRepository()


