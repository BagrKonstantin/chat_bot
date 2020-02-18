import telebot
from telebot import types

bot = telebot.TeleBot('1054926363:AAFIizR6JDjoe4TJtmmocU0zIbiYtLYPWqA')

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.add('Гуманитарное', 'Техническое', 'Гум-тех', 'Показать направление')
keyboard_answer = types.InlineKeyboardMarkup()
key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
keyboard_answer.add(key_yes)
key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
keyboard_answer.add(key_no)
list_pf_spec = ['Гуманитарное', 'Техническое', 'Гум-тех']
flag = list_pf_spec[2]
num = -1


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, выбери направление', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global num
    global flag
    if message.text.lower() == 'гуманитарное':
        num = 0
        bot.send_message(message.chat.id, '1',
                         reply_markup=keyboard_answer)
    elif message.text.lower() == 'техническое':
        num = 1
        bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать техническое направление?',
                         reply_markup=keyboard_answer)
    elif message.text.lower() == 'гум-тех':
        flag = list_pf_spec[2]
        bot.send_message(message.chat.id, 'Хорошо, вам будут приходить новости по направлению {}'.format(flag))
    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    elif message.text.lower() == 'показать направление':
        bot.send_message(message.chat.id, flag)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global flag
    if call.data == "yes":
        flag = list_pf_spec[num]
        bot.send_message(call.message.chat.id, 'Хорошо, вам будут приходить новости по направлению {}'.format(flag))
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Какое направление вы хотите выбрать',
                         reply_markup=keyboard1)
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


try:
    bot.polling(none_stop=True, interval=0)
except Exception as er:
    print(er)
