from g4f.client import Client
import requests
import os
from g4f import models


def get_context_from_ai(text: str, title: bool = False, image_text: bool = False, prompt: bool = False) -> str:
    """Генерирует заголовок, текст статьи и описание для картинки"""
    model_list = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
    client = Client()
    if title and image_text:
        ask_text = f"Перепиши заголовок другими словами от пяти до 7 слов. Заголовок - {text}"
    elif title:
        ask_text = f"Придумай заголовок для статьи, проанализировав её. Без ковычек. - {text}"
    elif prompt:
        ask_text = (f"Напиши промпт для генерации картинки. Только суть, без фамилий, без каких либо твоих "
                    f"дополнений и лишних вопросов. -"
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


def get_url_image_from_ai(prompt_image: str) -> str:
    """Генерация картинки и возврат урл"""
    client = Client()
    response = client.images.generate(
        model="dall_e_3",
        prompt=prompt_image,
        response_format="url"
    )

    return response.data[0].url


