import config
from datetime import datetime, timedelta, time, date
import psycopg2

conn = psycopg2.connect(database=config.db_connect['database'],
                        user=config.db_connect['user'],
                        password=config.db_connect['password'],
                        host=config.db_connect['host'],
                        port=config.db_connect['port'])
cursor = conn.cursor()


def odd_date_check():
    now = datetime.now()
    sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
    d1 = sep - timedelta(days=sep.weekday())
    d2 = now - timedelta(days=now.weekday())
    parity = not bool(((d2 - d1).days // 7) % 2)
    return parity

def now_date():
    return datetime.today().isoweekday() - 1

def now_data(time_delta = 0):
    odd = odd_date_check() # чётно нечётно
    day = now_date() # день недели
    day += time_delta
    if time_delta == 7:
        time_delta = 0
        odd = not odd
    return odd, day

def timedelta_to_str(td):
    return ':'.join(str(td).split(':')[:2])

def map_rasp(dataset):
    def f_map_rasp(data):
        p = list()
        lesson_delta = timedelta(hours=1, minutes=40)
        data_timedelta = datetime.combine(date.min, data[4]) - datetime.min
        timedelta_to_str(data_timedelta)
        p.append('*' + str(['9:30', '11:20', '13:10', '15:25', '17:15'].index(timedelta_to_str(data_timedelta)) + 1) + ')' + '*')
        p.append('('+str(timedelta_to_str(data[4]))+'-'+ str(timedelta_to_str(data_timedelta + lesson_delta))+')')
        p.append(data[2])
        p.append('\n')
        #p.append(str(data[4]))
        if data[3] == None:
            p.append('аудитория нн')
        else:
            p.append(data[3])
        if data[6] == None:
            p.append('преподаватель нн')
        else:
            p.append(data[6])
        return ' '.join(p)
    #print(dataset)
    return map(f_map_rasp, dataset)

def get_rasp(is_even = None, day = None):
    #print(day, is_even)
    if is_even == None or day == None:
        is_even, day = now_data()
    cursor.execute('''
        SELECT timetable.*, teacher.full_name
        FROM bin2001.timetable timetable
        LEFT JOIN bin2001.teacher teacher
        ON teacher.subject = timetable.subject
        WHERE day = %s AND is_even = %s
        ORDER BY start_time
        ''', (int(day), bool(is_even)))
    rt = ['*' + config.buttons['day_menu'][day] + ' ' + ("чётная" if is_even else "нечётная") + '*']
    rt.extend(list(map_rasp(cursor.fetchall())))
    return '\n'.join(rt)