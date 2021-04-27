import sys
import traceback

from db_conn import DBHelper
from utilities import *
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def mk_faculties(db: DBHelper):
    try:
        items = convert_list(db.get_faculties())
        keyboard_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for item in items:
            btn = KeyboardButton(text=item)
            keyboard_markup.add(btn)
        return keyboard_markup
    except Exception as e:
        print(e)


def mk_stages(db: DBHelper, faculty_id):
    try:
        items = convert_list(db.get_stages(faculty_id))  # ----------------------
        keyboard_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        btns = []
        for item in items:
            btns.append(KeyboardButton(text=item))
        while btns:
            if len(btns) > 1:
                keyboard_markup.row(btns.pop(0), btns.pop(0))
            else:
                keyboard_markup.add(btns.pop(0))

        keyboard_markup.add(text_back)
        return keyboard_markup
    except Exception as e:
        print(e)


def mk_directions(db: DBHelper, stage_id, faculty_id):
    try:
        items = convert_list(db.get_directions(stage_id, faculty_id))
        keyboard_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for item in items:
            btn = KeyboardButton(text=item)
            keyboard_markup.add(btn)
        keyboard_markup.add(text_back)
        return keyboard_markup
    except Exception as e:
        print(e)


def mk_groups(db: DBHelper, direction_id):
    try:
        items = convert_list(db.get_groups(direction_id))
        keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btns = []
        for item in items:
            btns.append(KeyboardButton(text=item))
        while btns:
            if len(btns) > 1:
                keyboard_markup.row(btns.pop(0), btns.pop(0))
            else:
                keyboard_markup.add(btns.pop(0))
        keyboard_markup.add(text_back)
        return keyboard_markup
    except Exception as e:
        print(e)


