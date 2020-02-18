import telebot
from telebot import types

bot = telebot.TeleBot('1054926363:AAFIizR6JDjoe4TJtmmocU0zIbiYtLYPWqA')

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Гуманитарное', 'Техническое', 'Не имеет значения')
keyboard_answer = types.InlineKeyboardMarkup()
key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
keyboard_answer.add(key_yes)
key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
keyboard_answer.add(key_no)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, выбери направление', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'гуманитарное':
        bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать гуманитарное направление?',
                         reply_markup=keyboard_answer)
    elif message.text.lower() == 'техническое':
        bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать техническое направление?',
                         reply_markup=keyboard_answer)
    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "Yes":
        bot.send_message(call.message.chat.id, 'Хорошо, вам будут приходить новости по вашему направлению');
    elif call.data == "No":
        bot.send_message(call.message.chat.id, 'Какое направление вы хотите выбрать',
                         reply_markup=keyboard1)


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


try:
    bot.polling(none_stop=True, interval=0)
except Exception:
    pass
