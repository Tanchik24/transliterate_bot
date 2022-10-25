import asyncio
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.markdown import bold, italic, underline
import transliterate
from string import punctuation
from config_reader import config

# Настраиваем логгер 
logging.basicConfig(
     filename='logfile.log',
     level=logging.INFO, 
     format='[%(asctime)s | %(levelname)s]: %(message)s',
     datefmt='%H:%M:%S'
 )

# Создаем бота
bot = Bot(config.bot_token.get_secret_value())
dp = Dispatcher(bot)

# Фотографии для отправки сообщения
sad_photo = 'AgACAgIAAxkBAAMQY1adKfoYOb19B2DH9JymxYSsSMQAAqe_MRuLhrhKZyGRIQ5x7RABAAMCAAN4AAMqBA'
dm_photo = 'AgACAgIAAxkBAAMgY1alzAlSXQGnwpOvoZjYyVwYrSUAAsK_MRuLhrhK8o2madweKDUBAAMCAAN4AAMqBA'

# id фото для пересылки сообщения
photo = []

# Функция проверяет корректность ввода
def check_messege(message: str) -> bool:
    
    if [s for s in message if s in '12345']:
        return (False, 'В имени или фамилии присутствуют недопустимые символы(')
    
    for char in punctuation:
        if char in message:
            return (False, 'В имени или фамилии присутствуют недопустимые символы(')
        
    if len(message.split(' ')) != 2:
        return(False, 'Вы не ввели имя или фамилию(')
    
    return (True,)
    

# Функция приветствия 
@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = 'Привет, напиши свое имя и фамилию и увидишь, что будет)'
    await bot.send_photo(message.from_user.id, dm_photo)
    await bot.send_message(message.from_user.id, text)
    logging.info(f'{user_name=} {user_id=} sent message: {message.text}')
    

# Если пользователь отправляет фото, бот пересылает это фото
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def resend_photo(message: types.Message):
    if message.photo[-1].file_id not in photo:
        photo.append(message.photo[-1].file_id)
    print(message.photo[-1].file_id)
    await bot.send_photo(message.from_user.id, message.photo[-1].file_id)
   
    
# Функция переводит кириллицу в латиницу
@dp.message_handler()
async def transliterate_func(message: types.Message):
    
    if check_messege(message.text)[0]:
        text = transliterate.translit(message.text, language_code='ru', reversed=True)
        await message.reply(text)
    else:
        text = check_messege(message.text)[1]
        await bot.send_photo(message.from_user.id, sad_photo, caption=text)
    
    user_name = message.from_user.username
    user_id = message.from_user.id
    logging.info(f'{user_name=} {user_id=} received message: {message.text} \nsent message: {text}')
    
async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())
