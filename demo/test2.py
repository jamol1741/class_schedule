from datetime import datetime, timedelta

t = [(1, '8:30'), (2, '10:00'), (3, '12:00'), (4, '13:30')]
delta_time = [10, 5, 2, 1]


def convert_dict(a):
    try:
        times_dict = {}
        if type(a) == list:
            for i in range(len(a)):
                temp_time = a[i][1]
                temp = []
                for dt in delta_time:
                    tm = datetime.strptime(temp_time, '%H:%M')
                    delta = timedelta(minutes=dt)
                    ret = tm - delta
                    temp.append(ret.strftime('%H:%M'))
                times_dict[a[i][0]] = temp
        return times_dict
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # print(convert_dict(t))
    print(datetime.now().weekday() + 1)

