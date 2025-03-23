import requests
import datetime

async def generate_response(message):
    response = requests.post(
        "https://text.pollinations.ai/openai", 
        json={
            "messages": [
                {
                    "role": "system",
                    "content": f'Не используй markdown в своих ответах; Сейчас {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}.'
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "model": "mistral",
        }
    )

    return response.json()["choices"][0]["message"]["content"]
