from g4f.client import Client


def get_context_from_ai(text: str, title: bool = False, image_text: bool = False, prompt: bool = False) -> str:
    """Генерирует заголовок, текст статьи и описание для картинки"""

    model_list = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
    client = Client()

    if title and image_text:
        ask_text = (f"Перепиши заголовок другими словами от пяти до 7 слов. Только один заголовок, без вариантов "
                    f"выбора. Заголовок - {text}")
    elif title:
        ask_text = (f"Придумай заголовок для статьи, проанализировав её. Без ковычек. Только один заголовок, "
                    f"без вариантов выбора. - {text}")
    elif prompt:
        ask_text = (f"Напиши промпт для генерации картинки. Только суть, без фамилий, без каких либо твоих "
                    f"дополнений и лишних вопросов. максимум 480 символов. Без запрещенных описаний для Bing-"
                    f" {text}")
    else:
        ask_text = (f"Перепиши статью другими словами всего должно быть 480 символов, убрав все упоминания nur.kz, "
                    f"Акорды, телеграмм каналов и т.д. Статья: {text}")

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
