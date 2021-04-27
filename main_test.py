import time
from datetime import datetime
import threading
import schedule

import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import db_conn
from utilities import *
import configs

API_TOKEN = configs.API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

db = db_conn.DBHelper()

remind_times = {
    1: '08:25',
    2: '09:47',
    3: '11:17'  # ,
    # 4: '13:17'
}


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    try:
        users_id = db.get_users_id()
        user_id = int(message.chat.id)
        bot.clear_step_handler_by_chat_id(user_id)  # ----------------------
        first_name = message.chat.first_name if message.chat.first_name else ''
        last_name = message.chat.last_name if message.chat.last_name else ''
        user_name = message.from_user.username
        full_name = first_name + " " + last_name
        if user_id not in users_id:
            db.add_user(user_id, name=full_name, user_name=user_name)
            bot.reply_to(message, f"""Assalomu Alaykum, {full_name}""")
        if not db.is_group_iden(user_id):
            faculties = convert_list(db.get_faculty())
            keyboard_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            for item in faculties:
                btn = KeyboardButton(text=item)
                keyboard_markup.add(btn)
            text = "Fakultetlar:"
            msg = bot.send_message(user_id, text, reply_markup=keyboard_markup)
            bot.register_next_step_handler(msg, iden_directions)
    except Exception as e:
        print(e)


def iden_directions(message: Message):
    try:
        faculty_name = message.text
        faculty_id = db.get_faculty_id(faculty_name)
        user_id = message.chat.id
        directions = convert_list(db.get_directions(faculty_id))
        faculties = convert_list(db.get_faculty())
        if faculty_name not in faculties:
            msg = bot.send_message(user_id, "Bunday fakultet mavjud emas!")
            bot.register_next_step_handler(msg, iden_directions)
        else:
            keyboard_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            for name in directions:
                btn = KeyboardButton(text=name)
                keyboard_markup.add(btn)
            text = "Yo`nalishlar:"
            msg = bot.send_message(user_id, text, reply_markup=keyboard_markup)
            bot.register_next_step_handler(msg, iden_groups, faculty_id=faculty_id)
    except Exception as e:
        print(e)


def iden_groups(message: Message, faculty_id):
    try:
        direction_name = message.text
        direction_id = db.get_direction_id(direction_name)
        user_id = message.chat.id

        directions = convert_list(db.get_directions(faculty_id))
        print(direction_name, directions)
        if direction_name not in directions:
            msg = bot.send_message(user_id, "Bunday yo'nalish mavjud emas!")
            bot.register_next_step_handler(msg, iden_groups, faculty_id=faculty_id)
        else:
            groups = convert_list(db.get_groups(direction_id))
            keyboard_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            for item in groups:
                btn = KeyboardButton(text=item)
                keyboard_markup.add(btn)
            text = "Guruhlar:"
            msg = bot.send_message(user_id, text, reply_markup=keyboard_markup)
            bot.register_next_step_handler(msg, get_groups, direction_id=direction_id)
    except Exception as e:
        # bot.clear_step_handler_by_chat_id(message.chat.id)  #-----------------------------
        print(e)


# def get_groups(message: Message, direction_id):
#     try:
#         group_name = message.text
#         group_id = db.get_group_id(group_name)
#         user_id = message.chat.id
#
#         groups = convert_list(db.get_groups(direction_id))
#         if group_name not in groups:
#             msg = bot.send_message(user_id, "Bunday guruh mavjud emas!")
#             bot.register_next_step_handler(msg, get_groups, direction_id=direction_id)
#         else:
#             db.set_group_id(user_id, group_id)
#             bot.send_message(user_id, "Siz ro'yhatdan o'tdingiz!",
#                              reply_markup=ReplyKeyboardRemove())
#     except Exception as e:
#         print(e)


# @bot.message_handler(commands=['get'])
# def send_welcome(message):
#     name, classroom, teacher_name = db.get_items(1, 1)
#     bot.reply_to(message, f"Dars: <b>{name}\n</b>"
#                           f"Xona: <b>{classroom}</b>\n"
#                           f"O`qituvchi: <b>{teacher_name}</b>",
#                  parse_mode='HTML')


# def send_schedule(unit):
#     users_id = db.get_users_id()
#     day_id = datetime.weekday(datetime.now()) + 1
#
#     name, classroom, teacher_name = db.get_items(day_id, unit)
#     msg_text = f"Dars: <b>{name}\n</b>" \
#                f"Xona: <b>{classroom}</b>\n" \
#                f"O`qituvchi: <b>{teacher_name}</b>"
#     for chat_id in users_id:
#         bot.send_message(chat_id, msg_text,
#                          parse_mode='HTML')


# send_schedule()  # ----------------------------


# def work_timer():
#     for i in remind_times.keys():
#         schedule.every().day.at(remind_times[i]).do(send_schedule, i)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


def work_polling():
    while True:
        try:
            print("Bot start")
            bot.enable_save_next_step_handlers(delay=2)
            bot.load_next_step_handlers()
            bot.polling(none_stop=True)
        except Exception as e:
            telebot.logger.error(e)
            print(f"TIME:\n"
                  f"    {datetime.now()}\n"
                  f"ERROR:"
                  f"    {e}\n"
                  f"SLEEP:"
                  f"    15 sec\n")
            time.sleep(15)


if __name__ == '__main__':
    t = threading.Thread(target=work_polling)
    # t2 = threading.Thread(target=work_timer)
    t.start()
    # t2.start()
