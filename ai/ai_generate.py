from g4f.client import Client
import requests
import os
from g4f import models


def get_context_from_ai(text: str, title: bool = False, image_text: bool = False, prompt: bool = False) -> str:
    """Генерирует заголовок, текст статьи и описание для картинки"""
    model_list = ["gpt-4o-mini", "gpt-3.5-turbo"]
    client = Client()
    if title and image_text:
        ask_text = f"Перепиши заголовок другими словами от пяти до 7 слов. Заголовок - {text}"
    elif title:
        ask_text = f"Придумай заголовок для статьи, проанализировав её. Без ковычек. - {text}"
    elif prompt:
        ask_text = (f"Напиши промпт для генерации картинки. Только тезесы, без фамилий. -"
                    f" {text}")
    else:
        ask_text = (f"Перепиши статью другими словами всего должно быть 480 символов, убрав все упоминания nur.kz, "
                    f"Акорды, телеграмм каналов и т.д. Статья: {text}")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": ask_text
                   }],
        web_search=False
    )

    return response.choices[0].message.content


def get_url_image_from_ai(prompt_image: str) -> str:
    """Генерация картинки и возврат урл"""
    client = Client()
    response = client.images.generate(
        model="flux",
        prompt=prompt_image,
        response_format="url"
    )

    return response.data[0].url


