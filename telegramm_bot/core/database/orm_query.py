import asyncio
from datetime import date
from typing import Tuple, List, Dict

from sqlalchemy import select, update, insert, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .engine import engine
from .models import Image, Article


async def write_article_to_bd(list_of_data: list, id_article: str = None, original: bool =
True, is_sko: bool = False, is_astana: bool = False, is_almata: bool = False):
    """Пишет оригинальную и обработанные статьи в БД"""
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
                        is_sko=True if is_sko else False,
                        is_astana=True if is_astana else False,
                        is_almata=True if is_almata else False,
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
                    article.reels_text = list_of_data[4]
                    article.prepared_for_reels = 1
                    print(f"текст для записи в рилса в БД - {article.reels_text}")
                    await session.commit()
                    print(f"Обновлена статья - {list_of_data[0]}")
                else:
                    print(f"Статья с id {id_article} не найдена")
            except Exception as e:
                print("Не удалось записать данные обработанные Нейросетью")
                print(f"Ошибка {e}")


async def get_exists_neiro_article(id) -> Tuple[str, str, str]:
    """Возвращает список статей обработанных в нейросети за сегодня"""
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(Article.image_text, Article.id_article, Article.prompt_image, Article.text_neiro_article,
                   Article.reels_text)
            .where(Article.id == id)
        )
        return query.first()


async def write_image_to_bd(dict_of_data: Dict[str, str]):
    """Запись пути картинки в БД"""
    async with AsyncSession(engine) as session:
        try:
            result = await session.execute(
                select(Image).where(Image.id_article == dict_of_data["id_article"])
            )
            image = result.scalar_one_or_none()

            if image:
                image.image_url = dict_of_data.get("image_url")
                image.image_path_with_text = dict_of_data.get("image_path_with_text")
                image.image_text = dict_of_data.get("image_text")
                image.is_published = True

            await session.commit()
            print(f"Добавлена новая картинка - {dict_of_data.get("image_path_with_text")}")
        except Exception as e:
            print("Не удалось записать данные картинки в базу данных")
            print(f"Ошибка {e}")


async def write_is_publised_article(id_article):
    """Помечает статью как опубликованную"""
    async with AsyncSession(engine) as session:
        try:
            await session.execute(
                update(Article)
                .where(Article.id_article == id_article)
                .values(is_published=1)
            )
            await session.commit()
        except Exception as e:
            print(f"Ошибка при обновлении is_published: \n{e}")


async def mark_artical_for_prepared_for_reels(id: int):
    """Помечает статью для обработки для Reels"""
    async with AsyncSession(engine) as session:
        try:
            await session.execute(
                update(Article)
                .where(Article.id == id)
                .values(prepared_for_reels=1)
            )
            await session.commit()
        except Exception as e:
            print(f"Ошибка при обновлении is_published: \n{e}")


async def write_reeels_text_to_bd(id_article: str, reels_text: str, prompt_image: str):
    """Пишет текст Reels для статьи в БД"""
    async with AsyncSession(engine) as session:
        try:
            await session.execute(
                update(Article)
                .where(Article.id_article == id_article)
                .values(reels_text=reels_text, prompt_image=prompt_image)
            )
            await session.commit()
        except Exception as e:
            print(f"Ошибка при обновлении is_published: \n{e}")


async def save_list_image_path_to_bd(dct_for_write_to_bd_image_path: Dict[str, str]):
    """Сохраняет список путей сгенерированных картинок в БД"""
    async with AsyncSession(engine) as session:
        try:
            new_article = Image(
                id_article=dct_for_write_to_bd_image_path.get("id_article"),
                image_url='',
                image_path_1=dct_for_write_to_bd_image_path.get("path_1"),
                image_path_2=dct_for_write_to_bd_image_path.get("path_2"),
                image_path_3=dct_for_write_to_bd_image_path.get("path_3"),
                image_path_4=dct_for_write_to_bd_image_path.get("path_4"),
                image_path_with_text='',
                image_text='',
                is_published=False
            )
            print('commit image')
            session.add(new_article)
            await session.commit()
        except Exception as e:
            print(f"Ошибка при обновлении is_published: \n{e}")


async def read_all_today_article() -> dict[str, str]:
    """Возвращает список заголовков статей и id за сегодня"""
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(Article.id, Article.title_original_article, Article.prepared_for_reels).where(
                func.date(Article.date_created) == date.today(),
                Article.is_published == False)
        )

        return query.all()


async def read_from_bd_origin_article(id: str) -> Tuple[str, str, str]:
    """Возвращает данные оригинальной статьи по ID"""
    async with AsyncSession(engine) as session:
        article = await session.execute(
            select(Article.id_article, Article.title_original_article, Article.text_original_article).where(
                Article.id == id)
        )
    return article.first()


async def read_all_original_artical_text() -> List[Tuple[str]]:
    """Выбирает все статьи за сегодня из БД, которые не обрабатывались"""
    async with AsyncSession(engine) as session:
        today = date.today()
        result = await session.execute(
            select(Article.id_article, Article.text_original_article, Article.prompt_image)
            .where(
                Article.date_created >= today,
                or_(
                    Article.reels_text == None,  # reels_text = NULL
                    Article.reels_text == ""  # reels_text = ''
                ),
                Article.prepared_for_reels == 1
            )
        )
        return result.all()


async def read_image_paths(id_article: str) -> str:
    """Выбирает из БД все пути картинок, если они существуют"""
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(Image.image_path_1, Image.image_path_2, Image.image_path_3, Image.image_path_4, ).where(
                Image.id_article == id_article)
        )

        row = query.first()
        return row if row else None


async def read_image_path_with_text(id_article: str) -> str:
    """Возвращает путь картинки с текстом для статьи по ID"""
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(Image.image_path_with_text).where(Image.id_article == id_article)
        )

        return query.first()


async def read_reels_text_and_id_from_bd() -> List[Tuple[str]]:
    """Возвращает текст Рилса и id"""
    async with AsyncSession(engine) as session:
        today = date.today()
        result = await session.execute(
            select(Article.id_article, Article.reels_text)
            .where(
                and_(
                    Article.reels_text != None,
                    Article.date_created >= today
                )
            )
        )
        return result.all()


if __name__ == '__main__':
    print(asyncio.run(read_reels_text_and_id_from_bd()))
