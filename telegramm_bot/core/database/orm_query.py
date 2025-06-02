from datetime import date
from requests import session
from sqlalchemy import select, update, insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Bundle
from aiogram import types
from sympy.polys.polyconfig import query

from .engine import engine
from .models import Image, Article


async def write_article_to_bd(list_of_data: list, id_article: str = None, original: bool =
True):
    async with AsyncSession(engine) as session:
        if original:
            try:
                # Проверка, существует ли статья
                print('True article')
                existing = await session.execute(
                    select(Article).where(Article.id_article == list_of_data[0])
                )
                result = existing.scalar_one_or_none()
                print(result)
                if result:
                    print(f"{list_of_data[2]} - Статья уже была, пропускаем.")
                else:
                    print('new article')
                    new_article = Article(
                        id_article=list_of_data[0],
                        url_article=list_of_data[1],
                        title_original_article=list_of_data[2],
                        text_original_article=list_of_data[3],
                    )
                    print('commit article')
                    session.add(new_article)
                    await session.commit()
                    print(f"Добавлена новая статья - {list_of_data[2]}")
            except Exception as e:
                print("Не удалось записать данные оригинальной статьи")
                print(f"Ошибка {e}")
        else:
            try:
                # Обновление полей нейросети
                result = await session.execute(
                    select(Article).where(Article.id_article == id_article)
                )
                article = result.scalar_one_or_none()

                if article:
                    article.title_neiro_article = list_of_data[0]
                    article.text_neiro_article = list_of_data[1]
                    article.prompt_image = list_of_data[2]
                    await session.commit()
                    print(f"Обновлена статья - {list_of_data[0]}")
                else:
                    print(f"Статья с id {id_article} не найдена")
            except Exception as e:
                print("Не удалось записать данные обработанные Нейросетью")
                print(f"Ошибка {e}")


async def read_from_bd_origin_article(id: str):
    async with AsyncSession(engine) as session:
        article = await session.execute(
            select(Article.id_article, Article.title_original_article, Article.text_original_article).where(
                Article.id == id)
        )
    return article.first()


async def write_image_to_bd(list_of_data: list):
    pass


async def read_all_today_article() -> dict[str, str]:
    async with AsyncSession(engine) as session:
        query = await session.execute(select(Article.id, Article.title_original_article).where(
            func.date(Article.date_created) == date.today(),
            Article.is_view == False)
        )

        return {id: title for id, title in query.all()}

# async def orm_get_all_list(table_name: str, session: AsyncSession):
#     model_class_name = __get_model_class_name(table_name)
#     query = select(Bundle("lst", model_class_name.name, model_class_name.id, model_class_name.is_published))
#     result = await session.execute(query)
#     return result.scalars().all()
#
#
# # get one record
# async def orm_get_row(session: AsyncSession, table_name: str, id: int):
#     model_class_name = __get_model_class_name(table_name)
#     query = select(model_class_name).where(model_class_name.id == id)
#     result = await session.execute(query)
#     return result.scalar()
#
#
# async def orm_add_user(message: types.Message, session: AsyncSession):
#     query = select(User.user_id)
#     result = await session.execute(query)
#     lst_users = result.scalars().all()
#     if message.from_user.id not in lst_users:
#         obj = User(
#             user_id=message.from_user.id,
#             name=message.from_user.first_name
#         )
#         session.add(obj)
#         await session.commit()
