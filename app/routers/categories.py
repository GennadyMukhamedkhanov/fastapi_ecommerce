from fastapi import APIRouter, status, Depends

from app.auth import get_current_user, get_current_seller
from app.models import CategoryModel
from app.schemas import CategorySchema
from app.services.categories import get_all_categories_services, create_category_services, update_category_services, \
    delete_category_services

# Создаём маршрутизатор с префиксом и тегом
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get("/",
            response_model=list[CategorySchema],
            dependencies=[Depends(get_current_user)],
            status_code=status.HTTP_200_OK)
async def get_all_categories(categories: list[CategoryModel] = Depends(get_all_categories_services)):
    """
    Возвращает список всех категорий товаров.
    """
    return categories


@router.post("/",
             response_model=CategorySchema,
             dependencies=[Depends(get_current_seller)],
             status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryModel = Depends(create_category_services)):
    """
    Создаёт новую категорию и возвращает ее.
    """
    return category


@router.put("/{category_id}",
            dependencies=[Depends(get_current_seller)],
            response_model=CategorySchema)
async def update_category(category: CategoryModel = Depends(update_category_services)):
    """
    Обновляет категорию по её ID.
    """
    return category


@router.delete("/{category_id}",
               dependencies=[Depends(delete_category_services), Depends(get_current_seller)],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_category():
    """
        Выполняет  мягкое удаление категории по её ID, изменяет поле is_active=True на is_active=False

    """
