import os
import time
import threading
import schedule
from send_event import *

import telebot
from telebot.types import Message, ReplyKeyboardRemove
import db_conn
from utilities import *
import configs
import reg_markups

API_TOKEN = configs.API_TOKEN_test_1

bot = telebot.TeleBot(API_TOKEN)

db = db_conn.DBHelper()


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    try:
        user_id = message.chat.id
        if message.text in configs.commands:
            command(message.text, user_id)
        users_id = db.get_users_id()
        bot.clear_step_handler_by_chat_id(user_id)  # ----------------------
        first_name = message.chat.first_name if message.chat.first_name else ''
        last_name = message.chat.last_name if message.chat.last_name else ''
        user_name = message.from_user.username
        full_name = first_name + " " + last_name
        if user_id not in users_id:
            db.add_user(user_id, name=full_name, user_name=user_name)
            bot.reply_to(message, f"""Assalomu Alaykum, {full_name}""")
        iden_faculty(message)
    except Exception as e:
        writer_log(sys.exc_info())


def iden_faculty(message: Message):
    try:
        if message.text == '/stop':
            bot.clear_step_handler_by_chat_id(message.chat.id)
            return
        user_id = message.chat.id
        if not db.is_group_iden(user_id):
            text = "Fakultetlar:"
            msg = bot.send_message(user_id, text, reply_markup=reg_markups.mk_faculties(db))
            bot.register_next_step_handler(msg, iden_stages)
    except:
        writer_log(sys.exc_info())


def iden_stages(message: Message):
    try:
        if message.text == '/stop':
            bot.clear_step_handler_by_chat_id(message.chat.id)
            return
        faculty_name = message.text
        faculty_id = db.get_faculty_id(faculty_name)
        user_id = message.chat.id
        faculties = convert_list(db.get_faculties())
        if message.text == text_back:
            text = "Fakultetlar:"
            msg = bot.send_message(user_id, text, reply_markup=reg_markups.mk_faculties(db))
            bot.register_next_step_handler(msg, iden_stages)
            return
        if not convert_list(db.get_stages(faculty_id)):
            msg = bot.send_message(user_id, "Hozircha bosqichlar mavjud emas!")
            bot.register_next_step_handler(msg, iden_stages)
            return
        if faculty_name not in faculties:
            msg = bot.send_message(user_id, "Bunday fakultet mavjud emas!")
            bot.register_next_step_handler(msg, iden_stages)
        else:
            text = "Bosqichlar:"
            msg = bot.send_message(user_id, text, reply_markup=reg_markups.mk_stages(db, faculty_id))
            bot.register_next_step_handler(msg, iden_directions, faculty_id=faculty_id)
    except Exception as e:
        writer_log(sys.exc_info())


def iden_directions(message: Message, faculty_id):
    try:
        if message.text == '/stop':
            bot.clear_step_handler_by_chat_id(message.chat.id)
            return
        stage_name = message.text
        stage_id = db.get_stage_id(stage_name)
        user_id = message.chat.id
        stages = convert_list(db.get_stages(faculty_id))
        if message.text == text_back:
            text = "Fakultetlar:"
            msg = bot.send_message(user_id, text, reply_markup=reg_markups.mk_faculties(db))
            bot.register_next_step_handler(msg, iden_stages)
            return
        if not convert_list(db.get_directions(stage_id, faculty_id)):
            msg = bot.send_message(user_id, "Hozircha yo`nalishlar mavjud emas!")
            bot.register_next_step_handler(msg, iden_directions, faculty_id=faculty_id)
            return
        if stage_name not in stages:
            msg = bot.send_message(user_id, "Bunday bosqich mavjud emas!")
            bot.register_next_step_handler(msg, iden_directions, faculty_id=faculty_id)
        else:
            text = "Yo`nalishlar:"
            msg = bot.send_message(user_id, text, reply_markup=reg_markups.mk_directions(db, stage_id, faculty_id))
            bot.register_next_step_handler(msg, iden_groups, stage_id=stage_id, faculty_id=faculty_id)
    except Exception:
        writer_log(sys.exc_info())


def iden_groups(message: Message, stage_id, faculty_id):
    try:
        if message.text == '/stop':
            bot.clear_step_handler_by_chat_id(message.chat.id)
            return
        direction_name = message.text
        direction_id = db.get_direction_id(direction_name)
        user_id = message.chat.id

        directions = convert_list(db.get_directions(stage_id, faculty_id))
        # print(direction_name, directions)
        if message.text == text_back:
            text = "Bosqichlar:"
            msg = bot.send_message(user_id, text, reply_markup=reg_markups.mk_stages(db, faculty_id))
            bot.register_next_step_handler(msg, iden_directions, faculty_id=faculty_id)
            return
        if not convert_list(db.get_groups(direction_id)):
            msg = bot.send_message(user_id, "Hozircha guruhlar mavjud emas!")
            bot.register_next_step_handler(msg, iden_groups, stage_id=stage_id, faculty_id=faculty_id)
            return
        if direction_name not in directions:
            msg = bot.send_message(user_id, "Bunday yo'nalish mavjud emas!")
            bot.register_next_step_handler(msg, iden_groups, stage_id=stage_id, faculty_id=faculty_id)
        else:
            text = "Guruhlar:"
            msg = bot.send_message(user_id, text, reply_markup=reg_markups.mk_groups(db, direction_id))
            bot.register_next_step_handler(msg, get_groups, direction_id=direction_id,
                                           faculty_id=faculty_id, stage_id=stage_id)
    except Exception:
        writer_log(sys.exc_info())


def get_groups(message: Message, direction_id, faculty_id, stage_id):
    try:
        if message.text == '/stop':
            bot.clear_step_handler_by_chat_id(message.chat.id)
            send_welcome(message)
            return
        group_name = message.text
        group_id = db.get_group_id(group_name)
        user_id = message.chat.id

        groups = convert_list(db.get_groups(direction_id))
        if message.text == text_back:
            text = "Yo`nalishlar:"
            msg = bot.send_message(user_id, text, reply_markup=reg_markups.mk_directions(db, stage_id, faculty_id))
            bot.register_next_step_handler(msg, iden_groups, stage_id=stage_id, faculty_id=faculty_id)
            return
        if group_name not in groups:
            msg = bot.send_message(user_id, "Bunday guruh mavjud emas!")
            bot.register_next_step_handler(msg, get_groups, direction_id=direction_id)
        else:
            db.set_group_id(user_id, group_id)
            bot.send_message(user_id, "Siz ro'yhatdan o'tdingiz!",
                             reply_markup=ReplyKeyboardRemove())
            ev_add_user(bot, db, user_id)
    except Exception:
        writer_log(sys.exc_info())


@bot.message_handler(commands=['get'])
def send_welcome(message: Message):
    try:
        text = message.text
        if len(text.split()) == 3:
            cmd, day, part = text.split()
            user_id = message.chat.id
            name, classroom, teacher_name = db.get_items(user_id, day, part)
            bot.reply_to(message, f"Dars: <b>{name}\n</b>"
                                  f"Xona: <b>{classroom}</b>\n"
                                  f"O`qituvchi: <b>{teacher_name}</b>",
                         parse_mode='HTML')
    except Exception:
        writer_log(sys.exc_info())


@bot.message_handler(commands=['cmd'])
def cmd(message: Message):
    try:
        text = message.text
        user_id = message.chat.id
        items = text.split()
        if len(items) >= 3:
            if items[1] == configs.password:
                if items[2] == 'delete_my_account':
                    db.cmd_delete_my_account(user_id)
                    bot.send_message(user_id, 'Sizning profilingiz o`chirildi!', reply_markup=ReplyKeyboardRemove())
                elif items[2] == 'get_methods':
                    methods = get_times(db)
                    bot.send_message(user_id, str(methods), reply_markup=ReplyKeyboardRemove())
                elif items[2] == 'test_new_user':
                    ev_add_user(bot, db, '252199508')
        elif len(items) == 2:
            if items[1] == 'test':
                bot.send_message(user_id, 'pss', reply_markup=ReplyKeyboardRemove())  # --------------------------
            if items[1] == 'Today':
                pass

    except:
        writer_log(sys.exc_info())


@bot.message_handler(commands=['delete_my_account'])
def delete_my_account(user_id):
    try:
        db.cmd_delete_my_account(user_id)
        bot.send_message(user_id, 'Sizning profilingiz o`chirildi!', reply_markup=ReplyKeyboardRemove())
    except:
        writer_log(sys.exc_info())


def send_remind(section_id, part, method_id):
    try:
        day_id = datetime.now().weekday() + 1
        identified_users = convert_list(db.get_identified_user(section_id, part, method_id, day_id))
        for user_id in identified_users:
            science, classroom, teacher = db.get_items(user_id, day_id, part)
            msg_text = f"Dars: <b>{science}\n</b>" \
                       f"Xona: <b>{classroom}</b>\n" \
                       f"O`qituvchi: <b>{teacher}</b>"
            bot.send_message(user_id, msg_text, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
    except Exception:
        writer_log(sys.exc_info())


def command(cmd, user_id):
    try:
        if cmd == 'today':
            pass
    except:
        writer_log(sys.exc_info())


def work_timer():
    try:
        section_id = 1
        remind_times = get_all_remind_times(db, section_id)

        """
                part =  1
                tm =  [1, '08:20']
                tm =  [2, '08:25']
                tm =  [3, '08:28']
                tm =  [4, '08:29']
            part =  2
                tm =  [1, '09:50']
                tm =  [2, '09:55']
                tm =  [3, '09:58']
                tm =  [4, '09:59']
            part =  3
                tm =  [1, '11:50']
                tm =  [2, '11:55']
                tm =  [3, '11:58']
                tm =  [4, '11:59']
            part =  4
                tm =  [1, '13:20']
                tm =  [2, '13:25']
                tm =  [3, '13:28']
                tm =  [4, '13:29']
        """
        for part in remind_times.keys():
            for tm in remind_times[part]:
                schedule.every().day.at(tm[1]).do(send_remind, section_id, part, tm[0])
        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        writer_log(sys.exc_info())


def work_polling():
    while True:
        try:
            print("Bot start")
            bot.enable_save_next_step_handlers(delay=2)
            bot.load_next_step_handlers()
            bot.polling(none_stop=True)
        except Exception as e:
            writer_log(sys.exc_info())
            time.sleep(15)


if __name__ == '__main__':
    try:
        os.environ["TZ"] = "Asia/Tashkent"
        time.tzset()

    except Exception as e:
        logging.warning(e)
    finally:
        print(datetime.now())

    #  ----- TEST  -------

    # print(db.get_user_info('252199508'))

    #  ----- TEST END  -------

    try:
        t = threading.Thread(target=work_polling)
        t2 = threading.Thread(target=work_timer)
        t.start()
        t2.start()
    except Exception as e:
        writer_log(sys.exc_info())
