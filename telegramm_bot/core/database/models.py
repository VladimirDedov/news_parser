from typing import List, Optional

from jeepney.low_level import Boolean
from sqlalchemy import Text, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    date_created: Mapped[DateTime] = mapped_column(DateTime,
                                                   default=func.now())  # func.now() - подтягивает текущее время
    date_updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Article(Base):
    __tablename__ = 'article'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_article: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    url_article: Mapped[str] = mapped_column(Text)
    title_original_article: Mapped[str] = mapped_column(Text)
    text_original_article: Mapped[str] = mapped_column(Text)
    title_neiro_article: Mapped[Optional[str]] = mapped_column(Text, default=None, nullable=True)
    text_neiro_article: Mapped[Optional[str]] = mapped_column(Text, default=None, nullable=True)
    prompt_image: Mapped[Optional[str]] = mapped_column(Text, default=None, nullable=True)
    is_view: Mapped[bool] = mapped_column(default=False)
    is_published: Mapped[bool] = mapped_column(default=False)


class Image(Base):
    __tablename__ = 'image'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_article: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    image_url: Mapped[Optional[str]] = mapped_column(Text, default=None, nullable=True)
    image_path_1: Mapped[Optional[str]] = mapped_column(Text, default=None, nullable=True)
    image_path_2: Mapped[Optional[str]] = mapped_column(Text, default=None, nullable=True)
    image_path_3: Mapped[Optional[str]] = mapped_column(Text, default=None, nullable=True)
    image_path_4: Mapped[Optional[str]] = mapped_column(Text, default=None, nullable=True)
    image_path_with_text: Mapped[Optional[str]] = mapped_column(Text, default=None)
    image_text: Mapped[Optional[str]] = mapped_column(Text, default=None, nullable=True)
    is_published: Mapped[bool] = mapped_column(default=False)
