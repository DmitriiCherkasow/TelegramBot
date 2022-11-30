import telebot
from datetime import datetime
from extensions import APIException, Convertor, a, b
import traceback
from config import TOKEN, exchanges


current_usd = a
current_eur = b


bot = telebot.TeleBot(TOKEN)

current_datetime = datetime.now().strftime("%d.%m.%y %H:%M:%S")


@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):
    text = (f'Добро пожаловать в бот калькулятор валют,{message.chat.username},'f' для получения всей инофрмации '
            'пользуйтесь командой /help')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message):
    text = ('/values - доступные валюты для расчета'
            '\n/info - инструкция по работе')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values_message(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(commands=['info'])
def info_message(message: telebot.types.Message):
    text = ('для расчет валюты введите данные в формате:'
            '\n<валюта за какую покупаете> <Валюта которую покупаете> <колличество первой валюты>'
            '\nвсе через пробел, должно быть 3 значения '
            '\nобразец(доллар рубль 100)'
            f'\nкурс валют ЦБ РФ на {current_datetime} '
            f'\nUSD - {current_usd}'
            f'\nEUR - {current_eur}'
        '\nприятного пользования ботом')
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling(none_stop=True)

