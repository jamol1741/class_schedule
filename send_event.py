import logging
import sys
import traceback

from db_conn import DBHelper
from utilities import *
from telebot.types import Message
from telebot import TeleBot


def ev_add_user(bot: TeleBot, db: DBHelper, user_id):
    try:
        admins_id = db.get_general_admin_id()
        print(admins_id)   #-----------------
        info = db.get_user_info(user_id)
        msg_txt = f" 🆕 Yangi foydalanuvchi qo`shildi!\n" \
                  f"     <b>Ismi:</b> {info['name']}\n" \
                  f"     <b>Foydalanuvchi nomi:</b> {info['user_name']}\n" \
                  f"     <b>ID:</b> {info['user_id']}\n" \
                  f"     <b>Guruhi:</b> {info['group']}"
        for id in admins_id:
            bot.send_message(id, msg_txt, parse_mode='HTML')
    except:
        writer_log(sys.exc_info())


