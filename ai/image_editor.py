import asyncio
from PIL import Image, ImageDraw, ImageFont
from config import PATH_FONT, PATH_FINAL_IMAGE, PATH_FINAL_IMAGE_REELS
from telegramm_bot.core.database.orm_query import read_reels_text_and_id_from_bd, read_image_paths


def wrap_text(text, font, max_width, draw):
    """Разбивает текст на строки, которые помещаются в максимальную ширину"""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]  # кровь из глаз...
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def draw_text_with_outline(draw, position, text, font, text_color="white", outline_color="black", outline_width=2):
    x, y = position
    # Рисуем контур (все соседние пиксели)
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    # Основной текст
    draw.text((x, y), text, font=font, fill=text_color)


def add_text_to_image(image_path: str = '', text_for_image: str = '', id_article: str = '',
                      font_size: int = 80, line_spacing: int = 30, reels: bool = False) -> str:
    """Добавляем текст на выбранную картинку и возвращаю путь картинки с текстом"""
    if reels:
        PATH_FINAL_IMAGE = PATH_FINAL_IMAGE_REELS

    image_path_with_text = f"{PATH_FINAL_IMAGE}-{id_article}.jpeg"
    print(image_path_with_text)
    # Загружаем изображение
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Шрифт
    font = ImageFont.truetype(PATH_FONT, size=font_size)

    # Обернутый текст
    wrapped_lines = wrap_text(text_for_image, font, max_width=img.width - 40, draw=draw)

    # Межстрочный интервал line_spacing
    line_height = font.getbbox("A")[3] - font.getbbox("A")[1] + line_spacing
    total_text_height = line_height * len(wrapped_lines)
    y_start = (img.height - total_text_height) // 2

    # Отрисовка текста с обводкой
    for i, line in enumerate(wrapped_lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (img.width - line_width) // 2
        y = y_start + i * line_height
        draw_text_with_outline(draw, (x, y), line, font, text_color="white", outline_color="black", outline_width=3)

    img.save(image_path_with_text)
    return image_path_with_text


async def main():
    """Генерит картинки с надписью рилса, для создания видео"""
    list_reels_and_id_article = await read_reels_text_and_id_from_bd()
    print(list_reels_and_id_article)
    for tpl in list_reels_and_id_article:
        list_image_paths = []
        id_article, reels_text = tpl
        list_image_paths = await read_image_paths(id_article)
        print(list_image_paths)
        try:
            if list_image_paths[0]:
                add_text_to_image(image_path=list_image_paths[0],
                                  id_article=id_article,
                                  text_for_image=reels_text,
                                  font_size=60,
                                  line_spacing=40,
                                  reels=True)
        except Exception as e:
            print(f"У статьи нет картинок {id_article}")


if __name__ == "__main__":
    asyncio.run(main())
    # add_text_to_image(image_path='/home/vvv/Видео/Ютуб/Видео - факты/Животные/Вымирающие Дельфин, леопард/1/Дальневосточный леопард, сумчатый дьявол и дельфин вакаита на одном изображении в естественной среде.jpeg',
    #
    #                   text_for_image="Они ещё живы... но уже вымерли...",
    #                   font_size=110,
    #                   line_spacing=40,
    #                   reels=True)
