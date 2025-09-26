import google.generativeai as genai
from config import GEMINI_API_KEY


def get_ask_text(title: bool = False, image_text: bool = False, prompt: bool = False) -> str:
    if title and image_text:
        ask_text = (f"Перепиши заголовок другими словами от пяти до 7 слов. Только один заголовок, без вариантов "
                    f"выбора. Заголовок - ")
    elif title:
        ask_text = (f"Придумай заголовок для статьи, проанализировав её. Без ковычек. Только один заголовок, "
                    f"без вариантов выбора. - ")
    elif prompt:
        ask_text = (f"Напиши промпт для генерации картинки. Только суть, без фамилий, без каких либо твоих "
                    f"дополнений и лишних вопросов. максимум 480 символов. Если тема запрещенная, то опиши не "
                    f"запрещенными словами для Bing.com - ")
    else:
        ask_text = (f"Перепиши статью другими словами всего должно быть 480 символов, убрав все упоминания nur.kz, "
                    f"Акорды, телеграмм каналов и т.д. Статья: ")

    return ask_text

def get_context_from_ai(text: str, title: bool = False, image_text: bool = False, prompt: bool = False) -> str:
    """Генерирует заголовок, текст статьи и описание для картинки. Переписать с использованием чата,
    чтобы не передвать всегда статью целиком для обработки. Экономить токены"""

    model_list = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-8b-latest", "gemini-1.5-flash-8b" ]
    genai.configure(api_key=GEMINI_API_KEY)

    ask_text = get_ask_text(title, image_text, prompt) + text

    for model_name in model_list:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(ask_text)
            return response.text
        except Exception as e:
            print(e)
            print(f"Не удалось получить данные с {model}\n Пробую со след модели в списке")
            continue
