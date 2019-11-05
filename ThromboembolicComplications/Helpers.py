import datetime


def calculate_age(born):
    try:
        born_time_obj = datetime.datetime.strptime(str(born), '%Y%m%d')
        today = datetime.date.today()
        return today.year - born_time_obj.year - ((today.month, today.day) < (born_time_obj.month, born_time_obj.day))
    except ValueError:
        return -1
