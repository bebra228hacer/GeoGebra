import openai
import json
import os
import time 
import random
import asyncio
import time
import openai
import httpx
with open("config.json", "r+", encoding = "utf-8") as config_open:
    CONFIG_JSON = json.load(config_open)
openai.api_key = CONFIG_JSON["CHATGPT_TOKEN"]



def user_get_thread():
    thread = openai.beta.threads.create()
    return thread.id

def new_assist():
    assistant = openai.beta.assistants.create(
    name="RELOAD_GRAF",
    instructions="""
    тут писать
    """,
    model="gpt-4-1106-preview"
)
    return assistant


async def chat_gpt(thread, text: str, assist_id="1"):
    assist_id = assist_id
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                f"https://api.openai.com/v1/threads/{thread}/messages",
                headers={"Authorization": f"Bearer {openai.api_key}", "OpenAI-Beta": "threads=v1"},
                json={"role": "user", "content": text},
                timeout=30
            )
            try:
                response = await client.post(
                    f"https://api.openai.com/v1/threads/{thread}/runs",
                    headers={"Authorization": f"Bearer {openai.api_key}", "OpenAI-Beta": "threads=v1"},
                    json={"assistant_id": assist_id},
                    timeout=30
                )
                response.raise_for_status()
                run_data = response.json()
                run_id = run_data["id"]
            except httpx.HTTPStatusError as e:
                print(f"Ошибка при создании run: {e}")
                if e.response.status_code == 429: 
                    await asyncio.sleep(3)
                    response = await client.post(
                        f"https://api.openai.com/v1/threads/{thread}/runs",
                        headers={"Authorization": f"Bearer {openai.api_key}", "OpenAI-Beta": "threads=v1"},
                        json={"assistant_id": assist_id},
                        timeout=30
                    )
                    response.raise_for_status()
                    run_data = response.json()
                    run_id = run_data["id"]
                else:
                    return None 
            while True:
                try:
                    response = await client.get(
                        f"https://api.openai.com/v1/threads/{thread}/runs/{run_id}",
                        headers={"Authorization": f"Bearer {openai.api_key}", "OpenAI-Beta": "threads=v1"},
                        timeout=30
                    )
                    response.raise_for_status()
                    run_status = response.json()["status"]
                except httpx.HTTPStatusError as e:
                    print(f"Ошибка при получении статуса run: {e}")
                    return "failed" 

                if run_status == "completed":
                    break
                elif run_status == "failed":
                    return "failed"
                await asyncio.sleep(1)
            try:
                response = await client.get(
                    f"https://api.openai.com/v1/threads/{thread}/messages?order=desc&limit=1",
                    headers={"Authorization": f"Bearer {openai.api_key}", "OpenAI-Beta": "threads=v1"},
                    timeout=30
                )
                response.raise_for_status()
                messages = response.json()
                if messages["data"]:
                    last_message = messages["data"][0]
                    if last_message["role"] == "assistant":
                        for content_item in last_message["content"]:
                            if content_item["type"] == "text":
                                return content_item["text"]["value"]
            except httpx.HTTPStatusError as e:
                print(f"Ошибка при получении сообщения ассистента: {e}")
                return None

        except Exception as e:
            print(f"Общая ошибка: {e}")
            return None


if __name__ == "__main__":
    pass   