from g4f.client import Client


def get_ask_text(title: bool = False, image_text: bool = False, prompt: bool = False) -> str:
    if title and image_text:
        ask_text = (f"Представь, что ты профессиональный журналист. Перепиши заголовок другими словами от пяти до 7 слов. Только один заголовок, без вариантов "
                    f"выбора. Заголовок - ")
    elif title:
        ask_text = (f"Представь, что ты профессиональный журналист. Придумай заголовок для статьи, проанализировав её. Без ковычек. Только один заголовок, "
                    f"без вариантов выбора. - ")
    elif prompt:
        ask_text = (f"Напиши промпт для генерации картинки. Только суть, без фамилий, без каких либо твоих "
                    f"дополнений и лишних вопросов. максимум 480 символов. Если тема запрещенная, то опиши не "
                    f"запрещенными словами для Bing.com - ")
    else:
        ask_text = (f"Представь, что ты профессиональный журналист. Перепиши статью другими словами всего должно быть 480 символов, убрав все упоминания nur.kz, "
                    f"Акорды, телеграмм каналов и т.д. Статья: ")

    return ask_text

def get_context_from_ai(text: str, title: bool = False, image_text: bool = False, prompt: bool = False) -> str:
    """Генерирует заголовок, текст статьи и описание для картинки"""

    model_list = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
    client = Client()
    # Получаем промпт для нейронки
    ask_text = get_ask_text(title, image_text, prompt) + text

    for model in model_list:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user",
                           "content": ask_text
                           }],
                web_search=False
            )
            break
        except Exception as e:
            print(e)
            print(f"Не удалось получить данные с {model}\n Пробую со след модели в списке")
            continue

    return response.choices[0].message.content
