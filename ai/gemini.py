import google.generativeai as genai
from config import GEMINI_API_KEY


def get_ask_text(title: bool = False, image_text: bool = False, prompt: bool = False, reels: bool = False) -> str:
    if title and image_text:
        ask_text = (f"Представь, что ты профессиональный журналист. Перепиши заголовок другими словами от семи до 15 слов. "
                    f"Если указан район или область, то обязательно включай в текст. Только один заголовок, без вариантов "
                    f"выбора. Без ковычек и звездочек. Заголовок - ")
    elif title:
        ask_text = (f"Представь, что ты профессиональный журналист. Придумай заголовок для статьи, проанализировав её. "
                    f"Без ковычек и звездочек. Только один заголовок, "
                    f"без вариантов выбора. Если указан район или область, то обязательно включай в текст. - ")
    elif prompt:
        ask_text = (f"Напиши промпт для генерации картинки. Только суть, без фамилий, без каких либо твоих "
                    f"дополнений и лишних вопросов. максимум 480 символов. Если тема запрещенная, то опиши не "
                    f"запрещенными словами для Bing.com - ")
    elif reels:
        ask_text = (
            f"Представь, что ты профессиональный журналист. Напиши кратко описание статьи для reels instagram, убрав все упоминания nur.kz, "
            f"Акорды, телеграмм каналов и т.д. Напиши только текст, без всяких твоих вступлений. Если указан район или область, город, то обязательно "
            f"включай в текст. Не пиши подробнее в материале или статье. Длина текста до 35 слов. Статья: ")
    else:
        ask_text = (f"Представь, что ты профессиональный журналист. Перепиши статью другими словами всего должно быть 480 символов, "
                    f"убрав все упоминания nur.kz, "
                    f"Акорды, телеграмм каналов и т.д. Без ковычек и звездочек в начале и конце. Статья: ")

    return ask_text



def get_context_from_ai(text: str, title: bool = False, image_text: bool = False, prompt: bool = False, reels:bool=False) -> str:
    """Генерирует заголовок, текст статьи и описание для картинки. Переписать с использованием чата,
    чтобы не передвать всегда статью целиком для обработки. Экономить токены"""

    model_list = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-8b-latest", "gemini-1.5-flash-8b"]
    genai.configure(api_key=GEMINI_API_KEY)

    ask_text = get_ask_text(title, image_text, prompt, reels) + text

    for model_name in model_list:
        try:

            model = genai.GenerativeModel(model_name)
            response = model.generate_content(ask_text)
            return response.text
        except Exception as e:
            print(e)
            print(f"Не удалось получить данные с {model}\n Пробую со след модели в списке")
            continue
