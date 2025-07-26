from telethon import TelegramClient, events
import os
from groq import Groq

# Your API ID, hash and bot token here
api_id = int(os.environ.get("TELEGRAM_API_ID"))
api_hash = os.environ.get("TELEGRAM_API_HASH")
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
groq_api_key = os.environ.get("GROQ_API_KEY")

client = TelegramClient('session', api_id, api_hash).start(bot_token=bot_token)
groq_client = Groq(api_key=groq_api_key)

@client.on(events.NewMessage)
async def echo(event):
    try:
        chat_id = event.chat_id
        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": event.message.message
                }
            ],
            model="mixtral-8x7b-32768",
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            n=1,
            stream=False,
        ).choices[0].message.content
        await client.send_message(chat_id, response)
    except Exception as e:
        print(e)
        await client.send_message(chat_id, "Error processing your request.")

client.run_until_disconnected()