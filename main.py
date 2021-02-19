from extensions import APIException, CryptoConverter, values
from config import TOKEN
import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def get_info(message: telebot.types.Message):
    info_text = 'Для работы бота введите:\n \
<имя первой валюты> <имя валюты, в которую надо перевести> \
<количество первой валюты>\n \
/values - вывести список доступных валют'
    bot.reply_to(message, info_text)

@bot.message_handler(commands=['values'])
def get_values(message: telebot.types.Message):
    values_text = 'Список доступных денежных валют:\n'
    for val in values.keys():
        values_text += f'\t-{val}\n'
    bot.reply_to(message, values_text)

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        message_values = message.text.split(' ')
        if len(message_values) != 3:
            raise APIException('Неверный ввод! \
(введите /start либо /help для пояснения)')
        base, quote, amount = message_values
    except APIException as e:
        bot.send_message(message.chat.id, f'{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду: {e}')

    else:
        res = CryptoConverter.get_price(base, quote, amount)
        bot.reply_to(message, res)


bot.polling(none_stop=True)