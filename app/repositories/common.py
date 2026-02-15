from sqlalchemy.orm import DeclarativeBase


class CommonRepository:
    model: DeclarativeBase = None

    '''
    CommonRepository в app/repositories/common.py предоставляет универсальный метод get для выборки одного объекта по ID,
     условиям where, фильтрам filter_by и жадной загрузке (eager_load). 
     Он динамически строит SQLAlchemy-запрос с опциями,
      исполняет scalar_one_or_none() и возвращает модель или None. 
      Это базовый инструмент для CRUD-операций в других репозиториях.

    '''
#
#     async def get(
#         self,
#         session: AsyncSession,
#         id_name: str | None = None,
#         id_value: int | str | None = None,
#         where: list | None = None,
#         filter_by: dict | BaseModel | None = None,
#         eager_load: list | None = None,
#     ) -> type(DeclarativeBase) | None:
#
#         """
#         Получение одного объекта по id и условиям.
#         :param session: Объект сессии
#         :param id_name: Название столбца с id. Передается, если имя столбца не id
#         :param id_value: id объекта
#         :param where: Список условий where
#         :param filter_by: Словарь условий filter_by
#         :param eager_load: Список жадных загрузок
#         :return: Модель объекта или None
#         """
        # if where is None:
        #     where = []
        #
        # if filter_by is not None:
        #     filter_by = filter_by.model_dump(exclude_defaults=True) if isinstance(filter_by, BaseModel) else filter_by
        # else:
        #     filter_by = {}
        #
        # if id_value is not None:
        #     where = self._get_where_condition(id_name, id_value, where)
        #
        # query = select(self.model).where(*where).filter_by(**filter_by)
        #
        # if eager_load is not None:
        #     query = query.options(*eager_load)
        #
        # result = await session.execute(query)
        # result = result.scalar_one_or_none()
        # return result
