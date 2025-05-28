from PIL import Image, ImageDraw, ImageFont

def wrap_text(text, font, max_width, draw):
    """Разбивает текст на строки, которые помещаются в max_width"""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
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

def add_text_to_image(id_article: str, text_for_image: str) -> str:
    image_path = f"/home/vvv/Python/scraper_news/Scraper_News/images/bing_image/{id_article}"
    image_path_with_text = f"/home/vvv/Python/scraper_news/Scraper_News/images/prepared_image/final-{id_article}"

    # Загружаем изображение
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Шрифт
    font = ImageFont.truetype("/home/vvv/Python/scraper_news/Scraper_News/Fonts/ubuntu-bold.ttf", size=80)

    # Обернутый текст
    wrapped_lines = wrap_text(text_for_image, font, max_width=img.width - 40, draw=draw)

    # Межстрочный интервал
    line_spacing = 30
    line_height = font.getbbox("A")[3] - font.getbbox("A")[1] + line_spacing
    total_text_height = line_height * len(wrapped_lines)
    y_start = (img.height - total_text_height) // 2

    # Отрисовка текста с обводкой
    for i, line in enumerate(wrapped_lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (img.width - line_width) // 2
        y = y_start + i * line_height
        draw_text_with_outline(draw, (x, y), line, font, text_color="white", outline_color="black", outline_width=2)

    img.save(image_path_with_text)
    return image_path_with_text, image_path

if __name__ == "__main__":
    add_text_to_image("-imatkefed-s-m_1.jpeg", "Министерство транспорта Казахстана отменит плату за дефектные дороги")


# from PIL import Image, ImageDraw, ImageFont
#
# def wrap_text(text, font, max_width, draw):
#     """Разбивает текст на строки, которые помещаются в max_width"""
#     words = text.split()
#     lines = []
#     current_line = ""
#
#     for word in words:
#         test_line = current_line + (" " if current_line else "") + word
#         bbox = draw.textbbox((0, 0), test_line, font=font)
#         line_width = bbox[2] - bbox[0]
#         if line_width <= max_width:
#             current_line = test_line
#         else:
#             lines.append(current_line)
#             current_line = word
#     if current_line:
#         lines.append(current_line)
#     return lines
#
# def add_text_to_image(id_article: str, text_for_image: str) -> str:
#     image_path = f"/home/vvv/Python/scraper_news/Scraper_News/images/bing_image/{id_article}"
#     image_path_with_text = f"/home/vvv/Python/scraper_news/Scraper_News/images/prepared_image/final-{id_article}"
#     # Загружаем изображение
#     img = Image.open(image_path)
#
#     # Создаем объект для рисования
#     draw = ImageDraw.Draw(img)
#
#     # Задаем шрифт и размер
#     font = ImageFont.truetype("/home/vvv/Python/scraper_news/Scraper_News/Fonts/ubuntu-bold.ttf", size=80)
#
#
#     # Переносим текст вручную по ширине изображения
#     wrapped_lines = wrap_text(text_for_image, font, max_width=760, draw=draw)
#
#     # Высота строки
#     line_spacing = 30
#     line_height = font.getbbox("A")[3] - font.getbbox("A")[1] + line_spacing
#
#     # Общая высота текста
#     total_text_height = line_height * len(wrapped_lines)
#
#     # Начальная координата Y для вертикального центрирования
#     y_start = (img.height - total_text_height) // 2
#
#     # Рисуем строки по центру
#     for i, line in enumerate(wrapped_lines):
#         bbox = draw.textbbox((0, 0), line, font=font)
#         line_width = bbox[2] - bbox[0]
#         x = (img.width - line_width) // 2
#         y = y_start + i * line_height
#
#         draw.text((x, y), line, font=font, fill='black')
#
#     # Сохраняем результат
#     img.save(image_path_with_text)
#
#     return image_path_with_text, image_path
#
#
# if __name__ == "__main__":
#     add_text_to_image("-imatkefed-s-m_1.jpeg", "Министерство транспорта Казахстана отменит плату за дефектные дороги")
