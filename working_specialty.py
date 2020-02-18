import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('1054926363:AAFIizR6JDjoe4TJtmmocU0zIbiYtLYPWqA')

keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard1.add('Гуманитарное', 'Техническое')
keyboard1.add('Гуманитарно-техническое')
keyboard1.add('Показать направление')
keyboard_answer = types.InlineKeyboardMarkup()
key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
keyboard_answer.add(key_yes)
key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
keyboard_answer.add(key_no)
list_pf_spec = ['Гуманитарное', 'Техническое', 'Гуманитарно-техническое']
flag = list_pf_spec[2]
num = -1


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '1')
    con = sqlite3.connect("user_names")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users_id_and_type_of_news (id_in_telegram,type_of_news) VALUES({},'Гуманитарно-техническое')".format(
            message.from_user.id))
    con.commit()
    con.close()
    bot.send_message(message.chat.id, 'Привет, выбери направление, сейчас: Гуманитарно-техническое',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global num
    if message.text.lower() == 'гуманитарное':
        num = 0
        bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать гуманитарное направление?',
                         reply_markup=keyboard_answer)
    elif message.text.lower() == 'техническое':
        num = 1
        bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать техническое направление?',
                         reply_markup=keyboard_answer)
    elif message.text.lower() == 'гуманитарно-техническое':
        num = 2
        bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать гуманитарно-техническое направление?',
                         reply_markup=keyboard_answer)
    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    elif message.text.lower() == 'показать направление':
        bot.send_message(message.chat.id, flag)
    else:
        bot.send_message(message.chat.id, 'Я вас не понимаю')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global flag
    if call.data == "yes":
        flag = list_pf_spec[num]
        con = sqlite3.connect("user_names")
        cur = con.cursor()
        cur.execute(
            "UPDATE users_id_and_type_of_news SET type_of_news = '{}' WHERE id_in_telegram = {}".format(flag,
                call.message.from_user.id))
        con.commit()
        con.close()
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
