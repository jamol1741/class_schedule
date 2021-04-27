import logging
import os
import sys
import traceback
from datetime import datetime, timedelta
from reprlib import Repr, aRepr


def time_sub(main_time, delta_time):
    t = datetime.strptime(main_time, '%H:%M')
    delta = timedelta(minutes=delta_time)
    ret = t - delta
    print(ret.strftime('%H:%M'))
    # print(time_sub.__name__)


if __name__ == '__main__':
    time_sub('08:30', 10)
    try:
        print(2 / 0)
    except Exception as e:
        # print('__file__ = ', __file__)
        # print('__name__ = ', __name__)
        # print('file name = ', os.path.basename(__file__))
        # print('\n', e)
        # print(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        # print(traceback.format_exception(exc_type, exc_value, exc_traceback))

        # logging.exception("message")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log_text = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        line = '-' * 120 + '\n'
        logging.basicConfig(filename='app.log', filemode='a',
                            format=line + '%(asctime)s : %(name)s - %(levelname)s - %(message)s' + line,
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.warning(log_text)
        # traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
