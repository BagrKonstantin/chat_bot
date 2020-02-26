import telebot
from telebot import types
import sqlite3
from random import choice

bot = telebot.TeleBot('1054926363:AAFIizR6JDjoe4TJtmmocU0zIbiYtLYPWqA')

keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add('Изменить направление')
keyboard_main.add('Показать направление')
keyboard_main.add('Примеры профессий')

keyboard_prof = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_prof.add('Технические профессии')
keyboard_prof.add('Гуманитарные профессии')
keyboard_prof.add('Назад')

keyboard_first = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_first.add('Выбрать направление')

keyboard_with_chose = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_with_chose.add('Техническое')
keyboard_with_chose.add('Гуманитарное')
keyboard_with_chose.add('Гуманитарно-техническое')

keyboard_answer = types.InlineKeyboardMarkup()
key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
keyboard_answer.add(key_yes)
key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
keyboard_answer.add(key_no)

list_pf_spec = ['Гуманитарное', 'Техническое', 'Гуманитарно-техническое']
list_of_gum_prof = ['Юрист', 'Менеджер', 'Маркетолог', 'Дизайнер', 'Экономист', 'Педагог', 'Переводчик', 'Дипломат',
                    'Фотограф', 'Психолог', 'Журналист', 'Видео-оператор', 'Хореограф', 'Кондитер']
list_of_tex_prof = ['Электрик', 'Энергетик', 'Токарь', 'Технолог', 'Строитель', 'Столяр', 'Слесарь-сборщик',
                    'Программист', 'Нанотехнолог', 'Механик', 'Монтажник', 'Бурильщик', 'Архитектор', 'Контролёр ОТК',
                    'Обработчик металла', 'Радиоинженер', 'Связист']
black_list = [799056502]

dictionary_of_users = {}


def dictionary_update():
    global dictionary_of_users
    con = sqlite3.connect("user_names")
    cur = con.cursor()
    result = cur.execute("SELECT id_in_telegram, type_of_news FROM users_id_and_type_of_news").fetchall()

    for info in result:
        dictionary_of_users[info[0]] = [info[1], info[1]]


dictionary_update()


class WrongCategoryName(Exception):
    pass


class PostFormatError(Exception):
    pass


class UserNotInDataBase(Exception):
    pass


bot.send_message(171303452, 'Бот запущен')


@bot.message_handler(commands=['start'])
def start_message(message):
    tel_id = message.from_user.id
    if tel_id in black_list:
        return
    inform = ''
    if message.from_user.first_name:
        inform += message.from_user.first_name + ' '
    if message.from_user.last_name:
        inform += message.from_user.last_name + ' '
    if message.from_user.username:
        inform += message.from_user.username + ' '
    if tel_id not in dictionary_of_users.keys():
        con = sqlite3.connect("user_names")
        cur = con.cursor()
        cur.execute(
            """INSERT INTO users_id_and_type_of_news 
            (id_in_telegram, info) VALUES({},'{}')""".format(
                tel_id, inform))
        con.commit()
        con.close()
        bot.send_message(message.chat.id, 'Мы внесли вас в Базу Данных')
        dictionary_update()
        bot.send_message(message.chat.id,
                         'Привет🌟\nВыбери направление,которое тебе интересно или' +
                         ' которое ты хочешь узнать',
                         reply_markup=keyboard_first)
    else:
        if dictionary_of_users[tel_id][0]:
            bot.send_message(message.chat.id,
                             'Вы уже в нашей базе данных, ваше направление: {}'.format(dictionary_of_users[tel_id][0]),
                             reply_markup=keyboard_main)
        else:
            bot.send_message(message.chat.id, 'У вас нет текущего направления', reply_markup=keyboard_first)


@bot.channel_post_handler(content_types=['text'])
def send_text(message):
    if '/post' in message.text.split('\n')[0]:
        try:
            if len(message.text.split('\n')) == 1:
                raise PostFormatError
            if 'гуманитарно-техническое' in message.text.split('\n')[0].lower():
                for text in dictionary_of_users.keys():
                    if dictionary_of_users[text][0]:
                        bot.send_message(text,
                                         'Новости по направлению {}\n{}'.format(dictionary_of_users[text][0],
                                                                                '\n'.join(
                                                                                    message.text.split('\n')[1:])))
                    else:
                        bot.send_message(text,
                                         'Новости по направлению Гуманитарно-техническое\n{}'.format('\n'.join(
                                             message.text.split('\n')[1:])))
            elif 'техническое' in message.text.split('\n')[0].lower():
                for text in dictionary_of_users.keys():
                    if dictionary_of_users[text][0] and dictionary_of_users[text][0].lower() != 'гуманитарное':
                        bot.send_message(text,
                                         'Новости по направлению {}\n{}'.format(dictionary_of_users[text][0],
                                                                                '\n'.join(
                                                                                    message.text.split('\n')[1:])))
                    else:
                        bot.send_message(text,
                                         'Новости по направлению Техническое\n{}'.format('\n'.join(
                                             message.text.split('\n')[1:])))
            elif 'гуманитарное' in message.text.split('\n')[0].lower():
                for text in dictionary_of_users.keys():
                    if dictionary_of_users[text][0] and dictionary_of_users[text][0].lower() != 'техническое':
                        bot.send_message(text,
                                         'Новости по направлению {}\n{}'.format(dictionary_of_users[text][0],
                                                                                '\n'.join(
                                                                                    message.text.split('\n')[1:])))
                    else:
                        bot.send_message(text,
                                         'Новости по направлению Гуманитарное\n{}'.format('\n'.join(
                                             message.text.split('\n')[1:])))
            else:
                raise WrongCategoryName
        except WrongCategoryName:
            bot.send_message(message.chat.id,
                             'Ошибка: Неверное название направления, доступны:\n{} @working_specialty_bot'.format(
                                 '\n'.join(list_pf_spec)))
        except PostFormatError:
            bot.send_message(message.chat.id, 'Ошибка: Неверный формат')
        except Exception as error:
            bot.send_message(message.chat.id, 'Ошибка: {} @working_specialty_bot'.format(error.__class__.__name__))
    else:
        bot.send_message(message.chat.id, 'Введите /post для отправки новостей @working_specialty_bot')


@bot.channel_post_handler(content_types=['video'])
def send_video(message):
    try:
        if '/post' in message.caption:
            if 'гуманитарно-техническое' in message.caption.lower():
                for text in dictionary_of_users.keys():
                    bot.send_video(text, message.video.file_id)
            elif 'техническое' in message.caption.lower():
                for text in dictionary_of_users.keys():
                    if dictionary_of_users[text][0].lower() != 'гуманитарное':
                        bot.send_video(text, message.video.file_id)
            elif 'гуманитарное' in message.caption.lower():
                for text in dictionary_of_users.keys():
                    if dictionary_of_users[text][0].lower() != 'техническое':
                        bot.send_video(text, message.video.file_id)
            else:
                raise WrongCategoryName
    except WrongCategoryName:
        bot.send_message(message.chat.id,
                         'Ошибка: Неверное название направления, доступны:\n{} @working_specialty_bot'.format(
                             '\n'.join(list_pf_spec)))
    except PostFormatError:
        bot.send_message(message.chat.id, 'Ошибка: Неверный формат')
    except Exception as error:
        bot.send_message(message.chat.id, 'Ошибка: {} @working_specialty_bot'.format(error.__class__.__name__))
    else:
        bot.send_message(message.chat.id, 'Введите /post для отправки новостей @working_specialty_bot')


@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.text, message.from_user.id)
    tel_id = message.from_user.id
    try:
        if tel_id not in dictionary_of_users.keys():
            raise UserNotInDataBase
        if tel_id in black_list:
            return
        if message.text.lower() == 'изменить направление' or message.text.lower() == 'выбрать направление':
            bot.send_message(message.chat.id, 'Какое направление вы хотите выбрать?',
                             reply_markup=keyboard_with_chose)
        elif message.text.lower() == 'примеры профессий':
            bot.send_message(message.chat.id, 'Примеры каких профессий вы хотите увидеть?',
                             reply_markup=keyboard_prof)
        elif message.text.lower() == 'назад':
            bot.send_message(message.chat.id, 'Списки профессий будут пополняться',
                             reply_markup=keyboard_main)
        elif message.text.lower() == 'технические профессии':
            bot.send_message(message.chat.id, '{}'.format(choice(list_of_tex_prof)))
        elif message.text.lower() == 'гуманитарные профессии':
            bot.send_message(message.chat.id, '{}'.format(choice(list_of_gum_prof)))
        elif message.text.lower() == 'гуманитарное':
            dictionary_of_users[tel_id][1] = list_pf_spec[0]
            bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать гуманитарное направление?',
                             reply_markup=keyboard_answer)
        elif message.text.lower() == 'техническое':
            dictionary_of_users[tel_id][1] = list_pf_spec[1]
            bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать техническое направление?',
                             reply_markup=keyboard_answer)
        elif message.text.lower() == 'гуманитарно-техническое':
            dictionary_of_users[tel_id][1] = list_pf_spec[2]
            bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать гуманитарно-техническое направление?',
                             reply_markup=keyboard_answer)
        elif message.text.lower() == 'я тебя люблю':
            bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
        elif message.text.lower() == 'показать направление':
            try:
                if dictionary_of_users[tel_id][0]:
                    bot.send_message(message.chat.id, dictionary_of_users[tel_id][0])
                else:
                    raise KeyError
            except KeyError:
                bot.send_message(message.chat.id, 'У вас нет текущего направления', reply_markup=keyboard_first)
        else:
            bot.send_message(message.chat.id, 'Я вас не понимаю')
    except UserNotInDataBase:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы, нажмите /start')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    tel_id = call.message.chat.id
    try:
        if call.data == "yes":
            flag_prev, flag_new = dictionary_of_users[tel_id]
            if tel_id not in dictionary_of_users.keys():
                raise UserNotInDataBase
            elif flag_new != flag_prev:
                con = sqlite3.connect("user_names")
                cur = con.cursor()
                cur.execute(
                    "UPDATE users_id_and_type_of_news SET type_of_news = '{}' WHERE id_in_telegram = {}".format(
                        flag_new,
                        tel_id))
                con.commit()
                bot.send_message(call.message.chat.id,
                                 'Хорошо, вам будут на техническое'
                                 'приходить новости по направлению {}'.format(flag_new),
                                 reply_markup=keyboard_main)
                if flag_new.lower() != 'гуманитарное':
                    bot.send_message(call.message.chat.id,
                                     'Рекомендуем посмотреть видео по одной из технических профессий')
                    bot.send_video(call.message.chat.id,
                                   'BAACAgIAAx0CVANKZAADoV5Wf_xLLMkF2WLQ5Qkx0IT7b64bAALfBAACNYywSlV9_MST0M9UGAQ')
                con.close()
                dictionary_update()
            else:
                bot.send_message(call.message.chat.id, 'У вас уже выбранно данное направление',
                                 reply_markup=keyboard_main)
        elif call.data == "no":
            bot.send_message(call.message.chat.id, 'Какое направление вы хотите выбрать',
                             reply_markup=keyboard_main)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except UserNotInDataBase:
        bot.send_message(call.message.chat.id, 'Вы не зарегистрированы, нажмите /start')
    except Exception as error:
        bot.send_message(call.message.chat.id,
                         'Что то пошло не так, скорее всего вы не зарегистрированы, нажмите /start')
        print(error.__class__.__name__)


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


try:
    bot.polling(none_stop=True, interval=0)
except Exception as er:
    print(er.__class__.__name__)
