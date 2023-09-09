from telethon import TelegramClient, events
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

api_id = int(os.environ.get('api_id'))
api_hash = os.environ.get('api_hash')
chat = int(os.environ.get('chat'))
with open('chats.txt', 'r') as f:
    chats = f.readlines()


with TelegramClient('session_name', api_id, api_hash) as client:
    @client.on(events.NewMessage(chats=(chats)))
    async def handler(event):
        message = event.message.to_dict()['message']
        username = (await event.get_sender()).username
        await client.send_message(chat, f'@{username} \n {message}')


    client.run_until_disconnected()
