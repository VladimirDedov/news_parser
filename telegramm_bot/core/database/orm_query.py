from datetime import date
from typing import Tuple
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
                existing = await session.execute(
                    select(Article).where(Article.id_article == list_of_data[0])
                )
                result = existing.scalar_one_or_none()
                if result:
                    print(f"{list_of_data[2]} - Статья уже была, пропускаем.")
                else:
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
                # Обновление полей полученных от нейросети
                result = await session.execute(
                    select(Article).where(Article.id_article == id_article)
                )
                article = result.scalar_one_or_none()

                if article:
                    article.title_neiro_article = list_of_data[0]
                    article.text_neiro_article = list_of_data[1]
                    article.prompt_image = list_of_data[2]
                    article.image_text = list_of_data[3]
                    await session.commit()
                    print(f"Обновлена статья - {list_of_data[0]}")
                else:
                    print(f"Статья с id {id_article} не найдена")
            except Exception as e:
                print("Не удалось записать данные обработанные Нейросетью")
                print(f"Ошибка {e}")


async def get_exists_neiro_article(id) -> Tuple[str, str, str]:
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(Article.image_text, Article.id_article, Article.prompt_image).where(Article.id == id)
        )
        return query.first()


async def read_from_bd_origin_article(id: str) -> Tuple[str, str, str]:
    async with AsyncSession(engine) as session:
        article = await session.execute(
            select(Article.id_article, Article.title_original_article, Article.text_original_article).where(
                Article.id == id)
        )
    return article.first()


async def write_image_to_bd(dict_of_data: list):
    async with AsyncSession(engine) as session:
        try:
            new_article = Image(
                id_article=dict_of_data.get("id_article"),
                image_url=dict_of_data.get("image_url"),
                image_path_1=dict_of_data.get(1),
                image_path_2=dict_of_data.get(2),
                image_path_3=dict_of_data.get(3),
                image_path_4=dict_of_data.get(4),
                image_path_with_text=dict_of_data.get("image_path_with_text"),
                image_text=dict_of_data.get("image_text"),
                is_published=True
            )
            print('commit image')
            session.add(new_article)
            await session.commit()
            print(f"Добавлена новая картинка - {dict_of_data.get("image_path_with_text")}")
        except Exception as e:
            print("Не удалось записать данные картинки в базу данных")
            print(f"Ошибка {e}")


async def read_all_today_article() -> dict[str, str]:
    async with AsyncSession(engine) as session:
        query = await session.execute(select(Article.id, Article.title_original_article).where(
            func.date(Article.date_created) == date.today(),
            Article.is_view == False)
        )

        return {id: title for id, title in query.all()}
