import logging 
import asyncio 

from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery,  ReplyKeyboardRemove
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from films import films
from commands import (
    FILMS_COMMAND,
    START_COMMAND,
    FILM_CREATE_COMMAND,
    BOT_COMMANDS
)

TOKEN = '8084647023:AAEAe_KuOcV1TVuxYeM_qj6k4LUUimkjK7w'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN) 
dp = Dispatcher(storage=MemoryStorage()) 

ADMINS = [1299079607] 

async def on_startup(dp):
    logging.info('Bot started') 





@dp.message(START_COMMAND)
async def start(message: Message) -> None:
    await message.answer(
        f"Вітаю, {message.from_user.full_name}!\n"\
        "Я перший бот Python розробника Скрипця Данила."
    )



@dp.message(FILMS_COMMAND)
async def films_search(message: Message) -> None: 
    film_choice = InlineKeyboardMarkup(inline_keyboard = [  ]) 
    for f in films:
        button = InlineKeyboardButton(text=f, callback_data=f) 
        film_choice.inline_keyboard.append([button]) 
    await message.answer(text='Choose film', reply_markup=film_choice)



class StateForm(StatesGroup):
   name = State()
   description = State()
   rating = State()
   genre = State()
   actors = State()
   poster = State()
   
   
   
@dp.message(FILM_CREATE_COMMAND)
async def film_create(message: Message, state: FSMContext) -> None:
   await state.set_state(StateForm.name)
   await message.answer(
       f"Введіть назву фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )
@dp.message(StateForm.name)
async def film_name(message: Message, state: FSMContext) -> None:
   await state.update_data(name=message.text)
   await state.set_state(StateForm.name)




@dp.message(StateForm.description)
async def film_name(message: Message, state: FSMContext) -> None:
   await state.update_data(name=message.text)
   await state.set_state(StateForm.description)
   await message.answer(
       f"Введіть опис фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )




@dp.message(StateForm.rating)
async def film_description(message: Message, state: FSMContext) -> None:
   await state.update_data(description=message.text)
   await state.set_state(StateForm.rating)
   await message.answer(
       f"Вкажіть рейтинг фільму від 0 до 10.",
       reply_markup=ReplyKeyboardRemove(),
   )




@dp.message(StateForm.genre)
async def film_rating(message: Message, state: FSMContext) -> None:
   await state.update_data(rating=float(message.text))
   await state.set_state(StateForm.genre)
   await message.answer(
       f"Введіть жанр фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )




@dp.message(StateForm.actors)
async def film_genre(message: Message, state: FSMContext) -> None:
   await state.update_data(genre=message.text)
   await state.set_state(StateForm.actors)
   await message.answer(
       text=f"Введіть акторів фільму через роздільник ', '\n"
       + html.bold("Обов'язкова кома та відступ після неї."),
       reply_markup=ReplyKeyboardRemove(),
   )




@dp.message(StateForm.poster)
async def film_actors(message: Message, state: FSMContext) -> None:
   await state.update_data(actors=[x for x in message.text.split(", ")])
   await state.set_state(StateForm.poster)
   await message.answer(
       f"Введіть посилання на постер фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )




@dp.message(StateForm.poster)
async def film_poster(message: Message, state: FSMContext) -> None:
   data = await state.update_data(poster=message.text)
   film = films[film_name]
   films[film]
   await state.clear()
   await message.answer(
       f"Фільм {film.name} успішно додано!",
       reply_markup=ReplyKeyboardRemove(),
   )

@dp.callback_query()
async def film_info_handler(callback:CallbackQuery):
    film_name = callback.data
    film_data = films[film_name]
    film_photo = film_data.get('photo', 'No photo')
    film_description = film_data.get('description', 'No description')
    film_year = film_data.get('year', 'Not known')
    film_genre = ' , '.join(film_data.get('genre', []))
    film_rating = film_data.get('rating', 'Not known')
    film_director = film_data.get('director', 'Not known')
    
    


    film_message = (
     f'📽️Назва: <b> {str(film_name)} </b>\n'
     f'📆Рік: {str(film_year)}\n'
     f'🎭Жанр: {str(film_genre)}\n'
     f'🌟Рейтинг: {str(film_rating)}\n'
     f'✍️Автор: {str(film_director)}\n'
     f'📑Опис: {str(film_description)}\n'
    )
    

    await bot.send_photo(chat_id=callback.message.chat.id, photo = film_photo, caption = str(film_message), parse_mode = 'HTML')






async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await bot.set_my_commands(BOT_COMMANDS)
    await dp.start_polling(bot) 

    

if __name__ == '__main__':
    asyncio.run(main()) 