import logging
import sys
import traceback
from datetime import datetime, timedelta

from db_conn import DBHelper


text_back = "⬅️ Orqaga"


def convert_list(a):
    try:
        if type(a) == list:
            for i in range(len(a)):
                a[i] = a[i][0]
        return a
    except Exception as e:
        print(e)


def convert_matrix(a):
    l = []
    try:
        if type(a) == list:
            for i in range(len(a)):
                temp = list(a[i])
                l.append(temp)
        return l
    except Exception as e:
        print(e)


def get_all_remind_times(db: DBHelper, section_id):
    try:
        #  [[1, 10], [2, 5], [3, 2], [4, 1]]
        delta_time = convert_matrix(db.get_delta_times())
        re_times = db.get_start_times(section_id)
        times_dict = {}
        if type(re_times) == list:
            for i in range(len(re_times)):
                temp_time = re_times[i][1]
                temp = []
                for dt in delta_time:
                    tm = datetime.strptime(temp_time, '%H:%M')
                    delta = timedelta(minutes=dt[1])
                    ret = tm - delta
                    ret_time = ret.strftime('%H:%M')
                    ret_method = dt[0]
                    temp.append([ret_method, ret_time])
                times_dict[re_times[i][0]] = temp
        return times_dict
    except Exception:
        writer_log(sys.exc_info())


def get_times(db: DBHelper):
    try:
        methods = convert_list(db.get_methods())
        return methods
    except Exception:
        writer_log(sys.exc_info())


def get_schedule_times(db: DBHelper):
    try:
        lesson_start_times = db.get_start_times()
        print(lesson_start_times)  # -----------------------
    except Exception:
        writer_log(sys.exc_info())


def writer_log(info):
    try:
        exc_type, exc_value, exc_traceback = info
        log_text = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        line = '-' * 120 + '\n'
        logging.basicConfig(filename='app.log', filemode='a',
                            format=line + '%(asctime)s : %(name)s - %(levelname)s - %(message)s' + line,
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.warning(log_text)
    except Exception as e:
        print(e)



