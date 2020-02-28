import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('1054926363:AAFIizR6JDjoe4TJtmmocU0zIbiYtLYPWqA')

keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add('Изменить направление')
keyboard_main.add('Показать направление')

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
list_of_gum_tex_prof = ['Юрист', 'Программист', 'Дизайнер', 'Радиоинженер', 'Педагог', 'Архитектор', 'Переводчик',
                        'Связист', 'Фотограф', 'Психолог', 'Журналист', 'Видео-оператор', 'Нанотехнолог', 'Кондитер']
black_list = [799056502]

dictionary_of_users = {}

ban_count = 15


class User:
    def __init__(self, specialization, name):
        self.specialization = specialization
        self.change = False
        self.name = name
        self.ban = False
        self.messages = 0

    def swap(self):
        self.specialization = self.change
        self.change = False

    def update_ban(self):
        if self.messages > ban_count:
            self.ban = True
        else:
            self.messages += 1


def dictionary_update():
    global dictionary_of_users
    con = sqlite3.connect("user_names")
    cur = con.cursor()
    result = cur.execute("SELECT id_in_telegram, type_of_news, info FROM users_id_and_type_of_news").fetchall()

    for info in result:
        if info[0] not in dictionary_of_users.keys():
            dictionary_of_users[info[0]] = User(info[1], info[2])
    con.close()


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
    try:
        tel_id = message.from_user.id
        if tel_id in dictionary_of_users.keys():
            if dictionary_of_users[tel_id].ban:
                return
            else:
                dictionary_of_users[tel_id].update_ban()
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
            if dictionary_of_users[tel_id].specialization:
                bot.send_message(message.chat.id,
                                 'Вы уже в нашей базе данных, ваше направление: {}'.format(
                                     dictionary_of_users[tel_id].specialization),
                                 reply_markup=keyboard_main)
            else:
                bot.send_message(message.chat.id, 'У вас нет текущего направления', reply_markup=keyboard_first)
    except Exception as error:
        print(error.__class__.__name__)


@bot.channel_post_handler(content_types=['text'])
def send_text(message):
    try:
        if '/post' in message.text.split('\n')[0]:
            if len(message.text.split('\n')) == 1:
                raise PostFormatError
            if 'гуманитарно-техническое' in message.text.split('\n')[0].lower():
                for text in dictionary_of_users.keys():
                    if dictionary_of_users[text].specialization:
                        bot.send_message(text,
                                         'Новости по направлению {}\n{}'.format(
                                             dictionary_of_users[text].specialization,
                                             '\n'.join(
                                                 message.text.split('\n')[1:])))
                    else:
                        bot.send_message(text,
                                         'Новости по направлению Гуманитарно-техническое\n{}'.format('\n'.join(
                                             message.text.split('\n')[1:])))
            elif 'техническое' in message.text.split('\n')[0].lower():
                for text in dictionary_of_users.keys():
                    if dictionary_of_users[text].specialization and \
                            dictionary_of_users[text].specialization.lower() != 'гуманитарное':
                        bot.send_message(text,
                                         'Новости по направлению {}\n{}'.format(
                                             dictionary_of_users[text].specialization,
                                             '\n'.join(
                                                 message.text.split('\n')[1:])))
                    else:
                        bot.send_message(text,
                                         'Новости по направлению Техническое\n{}'.format('\n'.join(
                                             message.text.split('\n')[1:])))
            elif 'гуманитарное' in message.text.split('\n')[0].lower():
                for text in dictionary_of_users.keys():
                    if dictionary_of_users[text].specialization and \
                            dictionary_of_users[text].specialization.lower() != 'техническое':
                        bot.send_message(text,
                                         'Новости по направлению {}\n{}'.format(
                                             dictionary_of_users[text].specialization,
                                             '\n'.join(
                                                 message.text.split('\n')[1:])))
                    else:
                        bot.send_message(text,
                                         'Новости по направлению Гуманитарное\n{}'.format('\n'.join(
                                             message.text.split('\n')[1:])))
            else:
                raise WrongCategoryName

        elif '/prof' in message.text:
            for text in dictionary_of_users.keys():
                if dictionary_of_users[text].specialization == 'Гуманитарное':
                    bot.send_message(text, '\n'.join(list_of_gum_prof))
                elif dictionary_of_users[text].specialization == 'Техническое':
                    bot.send_message(text, '\n'.join(list_of_tex_prof))
                else:
                    bot.send_message(text, '\n'.join(list_of_gum_tex_prof))
        else:
            bot.send_message(message.chat.id, 'Введите /post для отправки новостей @working_specialty_bot')
    except WrongCategoryName:
        bot.send_message(message.chat.id,
                         'Ошибка: Неверное название направления, доступны:\n{} @working_specialty_bot'.format(
                             '\n'.join(list_pf_spec)))
    except PostFormatError:
        bot.send_message(message.chat.id, 'Ошибка: Неверный формат')
    except Exception as error:
        bot.send_message(message.chat.id, 'Ошибка: {} @working_specialty_bot'.format(error.__class__.__name__))


@bot.channel_post_handler(content_types=['video'])
def send_video(message):
    try:
        if '/post' in message.caption:
            if 'гуманитарно-техническое' in message.caption.lower():
                for text in dictionary_of_users.keys():
                    bot.send_video(text, message.video.file_id)
            elif 'техническое' in message.caption.lower():
                for text in dictionary_of_users.keys():
                    if dictionary_of_users[text].specialization.lower() != 'гуманитарное':
                        bot.send_video(text, message.video.file_id)
            elif 'гуманитарное' in message.caption.lower():
                for text in dictionary_of_users.keys():
                    if dictionary_of_users[text].specialization.lower() != 'техническое':
                        bot.send_video(text, message.video.file_id)
            else:
                raise WrongCategoryName
        else:
            bot.send_message(message.chat.id, 'Введите /post для отправки новостей @working_specialty_bot')
    except WrongCategoryName:
        bot.send_message(message.chat.id,
                         'Ошибка: Неверное название направления, доступны:\n{} @working_specialty_bot'.format(
                             '\n'.join(list_pf_spec)))
    except PostFormatError:
        bot.send_message(message.chat.id, 'Ошибка: Неверный формат')
    except Exception as error:
        bot.send_message(message.chat.id, 'Ошибка: {} @working_specialty_bot'.format(error.__class__.__name__))


@bot.message_handler(content_types=['text'])
def send_text(message):
    tel_id = message.from_user.id
    try:
        if tel_id not in dictionary_of_users.keys():
            raise UserNotInDataBase
        if dictionary_of_users[tel_id].ban:
            return
        else:
            dictionary_of_users[tel_id].update_ban()
        print(message.text, dictionary_of_users[tel_id].name, dictionary_of_users[tel_id].messages)
        if message.text.lower() == 'изменить направление' or message.text.lower() == 'выбрать направление':
            bot.send_message(message.chat.id, 'Какое направление вы хотите выбрать?',
                             reply_markup=keyboard_with_chose)
        elif message.text.lower() == 'гуманитарное':
            dictionary_of_users[tel_id].change = list_pf_spec[0]
            bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать гуманитарное направление?',
                             reply_markup=keyboard_answer)
        elif message.text.lower() == 'техническое':
            dictionary_of_users[tel_id].change = list_pf_spec[1]
            bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать техническое направление?',
                             reply_markup=keyboard_answer)
        elif message.text.lower() == 'гуманитарно-техническое':
            dictionary_of_users[tel_id].change = list_pf_spec[2]
            bot.send_message(message.chat.id, 'Вы уверены что хотите выбрать гуманитарно-техническое направление?',
                             reply_markup=keyboard_answer)
        elif message.text.lower() == 'я тебя люблю':
            bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
        elif message.text.lower() == 'показать направление':
            try:
                if dictionary_of_users[tel_id].specialization:
                    bot.send_message(message.chat.id, dictionary_of_users[tel_id].specialization)
                else:
                    raise KeyError
            except KeyError:
                bot.send_message(message.chat.id, 'У вас нет текущего направления', reply_markup=keyboard_first)
        else:
            bot.send_message(message.chat.id, 'Я вас не понимаю')
    except UserNotInDataBase:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы, нажмите /start')
    except Exception as error:
        print(error.__class__.__name__)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    tel_id = call.message.chat.id
    try:
        if call.data == "yes":
            if tel_id not in dictionary_of_users.keys():
                raise UserNotInDataBase
            elif dictionary_of_users[tel_id].change != dictionary_of_users[tel_id].specialization:
                con = sqlite3.connect("user_names")
                cur = con.cursor()
                cur.execute(
                    "UPDATE users_id_and_type_of_news SET type_of_news = '{}' WHERE id_in_telegram = {}".format(
                        dictionary_of_users[tel_id].change, tel_id))
                dictionary_of_users[tel_id].swap()
                con.commit()
                con.close()
                bot.send_message(call.message.chat.id,
                                 'Хорошо, вам будут приходить новости по направлению {}'.format(
                                     dictionary_of_users[tel_id].specialization),
                                 reply_markup=keyboard_main)
                if dictionary_of_users[tel_id].specialization.lower() != 'гуманитарное':
                    bot.send_message(call.message.chat.id,
                                     'Рекомендуем посмотреть видео по одной из технических профессий')
                    bot.send_video(call.message.chat.id,
                                   'BAACAgIAAx0CVANKZAADoV5Wf_xLLMkF2WLQ5Qkx0IT7b64bAALfBAACNYywSlV9_MST0M9UGAQ')
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
