from g4f.client import Client


def get_context_from_ai(text: str, title: bool = False, image_text: bool = False) -> str:
    model_list = ["gpt-4o-mini", "gpt-3.5-turbo"]
    client = Client()
    if title and image_text:
        ask_text = f"Перепиши заголовок другими словами от четырех до 6 слов. Заголовок - {text}"
    elif title:
        ask_text = f"Придумай заголовок для статьи, проанализировав её. Без ковычек. - {text}"
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

    print(response.choices[0].message.content)
    return response.choices[0].message.content


def get_url_image_from_ai():
    client = Client()
    response = client.images.generate(
        model="flux",
        prompt="a white siamese man",
        response_format="url"
    )

    return response.data[0].url
