from telethon import TelegramClient, events
import os
from dotenv import load_dotenv, find_dotenv
from discorg_bot import send_message

load_dotenv(find_dotenv())

api_id = int(os.environ.get('api_id'))
api_hash = os.environ.get('api_hash')
chat = int(os.environ.get('chat'))
client = TelegramClient('session_name', api_id, api_hash)
client.start()
with open('chats.txt', 'r') as f:
    chats = f.readlines()


@client.on(events.NewMessage(chats=(chats)))
async def handler(event):
    message = event.message.to_dict()['message']
    if 'wtb' in message.lower():
        username = (await event.get_sender()).username
        await client.send_message(chat, f'@{username} \n {message}')
        send_message(f'@{username} \n {message}')


client.run_until_disconnected()
