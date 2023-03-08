import requests
from bs4 import BeautifulSoup
import lxml
import telebot

# функция для парсинга списка фильмов определенного жанра
def film_scrab(link):
    list_of_films = []
    res = requests.get(link)
    html = BeautifulSoup(res.text, 'lxml')
    data = html.find_all(class_='nbl-slimPosterBlock__titleText')
    n = len(data)

    for i in range(n):
        list_of_films.append(data[i].text)
    list_of_films = '\n'.join(list_of_films)
    return list_of_films


token = '5837182018:AAElJ11ZSSevaQ06S8Q6vcFrWSWVTGEJmps'
bot = telebot.TeleBot(token)

# словарь жанров фильмов и ссылок на категории этих жанров сайта Иви (будут использоваться в функции парсинга фильмов)
links = {'Мелодрамы': 'https://www.ivi.ru/movies/melodramy/page2',
         'Криминал': 'https://www.ivi.ru/movies/crime',
         'Комедии': 'https://www.ivi.ru/movies/comedy',
         'Приключения': 'https://www.ivi.ru/movies/adventures',
         'Ужасы': 'https://www.ivi.ru/movies/horror',
         'Боевики': 'https://www.ivi.ru/movies/boeviki',
         'Детективы': 'https://www.ivi.ru/movies/detective',
         'Драмы': 'https://www.ivi.ru/movies/drama',
         'Фэнтези': 'https://www.ivi.ru/movies/fentezi',
         'Зарубежные': 'https://www.ivi.ru/movies/foreign',
         'Триллеры': 'https://www.ivi.ru/movies/thriller',
         'Новинки': 'https://www.ivi.ru/new/movie-new'}

# ответ на команду start
@bot.message_handler(commands=['start'])
def send_welc(message):
    welc_txt = 'Привет! Я помогу тебе выбрать фильм:) Выбери интересующий жанр!'
    # создаем поле с кнопками (клавиатуру)
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=False)
    # создаем список кнопок
    buttons = [telebot.types.KeyboardButton('Мелодрамы'),
               telebot.types.KeyboardButton('Криминал'),
               telebot.types.KeyboardButton('Комедии'),
               telebot.types.KeyboardButton('Приключения'),
               telebot.types.KeyboardButton('Ужасы'),
               telebot.types.KeyboardButton('Боевики'),
               telebot.types.KeyboardButton('Детективы'),
               telebot.types.KeyboardButton('Драмы'),
               telebot.types.KeyboardButton('Фэнтези'),
               telebot.types.KeyboardButton('Зарубежные'),
               telebot.types.KeyboardButton('Триллеры'),
               telebot.types.KeyboardButton('Новинки')
               ]
    # размещаем кнопки на клавиатуре
    keyboard.add(*buttons)
    # вывод сообщения в тг
    bot.send_message(message.chat.id, welc_txt, reply_markup=keyboard)

# бот использует ссылку нужного жанра, исходя из текста пользователя
@bot.message_handler(content_types=['text'])
def send_film(message):
    txt = film_scrab(links[message.text.strip()])
    # вывод сообщения в тг
    bot.send_message(message.chat.id, txt)

bot.polling()
