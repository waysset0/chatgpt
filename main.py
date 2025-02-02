import logging
import asyncio
import nest_asyncio
import os
from g4f.client import Client
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ["TOKEN"])
dp = Dispatcher()

nest_asyncio.apply()

user_choices = {}

@dp.message(CommandStart())
async def cmd_start(message: Message):
    text = f"Привет, @{message.from_user.username}! Выбери модель, которую ты хочешь использовать:"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Gemini 1.5 flash', callback_data='gemini'),
            InlineKeyboardButton(text='Claude 3.5 Sonnet', callback_data='claude-3.5-sonnet'),
            InlineKeyboardButton(text='ChatGPT 4o', callback_data='gpt-4o')
        ]
    ])
    await message.answer(text, parse_mode="Markdown", reply_markup=kb)
    user_choices[message.from_user.id] = None 

@dp.callback_query(lambda c: c.data in ['gemini', 'claude-3.5-sonnet', 'gpt-4o'])
async def process_callback(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_choices[user_id] = callback_query.data
    if callback_query.data == 'gemini':
        await callback_query.message.answer("Вы успешно выбрали модель: Gemini 1.5 flash")
    elif callback_query.data == 'claude-3.5-sonnet':
        await callback_query.message.answer("Вы успешно выбрали модель: Claude 3.5 Sonnet")
    elif callback_query.data == 'gpt-4o':
        await callback_query.message.answer("Вы успешно выбрали модель: ChatGPT 4o")
    await callback_query.answer()

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    choice = user_choices.get(user_id)
    
    if choice == 'gemini':
        client = Client()
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(response.choices[0].message.content)   
    elif choice == 'claude-3.5-sonnet':
        client = Client()
        response = client.chat.completions.create(
            model="claude-3.5-sonnet",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(response.choices[0].message.content)
    elif choice == 'gpt-4o':
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(response.choices[0].message.content)
    else:
        await message.answer("Сначала выбери модель!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
